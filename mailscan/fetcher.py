from imaplib import IMAP4_SSL
from .util import error
from uuid import uuid4
from email.message import EmailMessage
from email import policy
import pprint, email, os

storage_dir = '/tmp/mailscan/'

def fetch_attachements(conf: dict) -> list:
    mails = _fetch_mails(conf)
    att_files = []
    for mail in mails:
        attachements = _get_attachements(mail)
        for att in attachements:
            att_files += _get_attachement_files(att)
    
    print("Successfully fetched %i attachements" % len(att_files))
    return att_files

def _fetch_mails(conf: dict) -> list:
    imap_host = conf['imap']['host']
    imap_user = conf['imap']['user']
    imap_pass = conf['imap']['password']
    imap_folder = conf['imap']['folder']
    imap_deletefetched = conf['imap']['deletefetched']

    try:
        imap = IMAP4_SSL(imap_host) # connect to server
        imap.login(imap_user, imap_pass)
        imap.select(imap_folder)
        _, data = imap.search(None, '(UNSEEN)') # Search all mails

        emails = []

        for emailid in data[0].split():
            _, maildata = imap.fetch(emailid, '(RFC822)')
            email_body = maildata[0][1]
            emails.append(email.message_from_bytes(email_body))
            if imap_deletefetched:
                imap.store(emailid, '+FLAGS', '\\Deleted')
                print('deleted email after fetching')

        if imap_deletefetched:
            imap.expunge()
        imap.close()
        imap.logout()
        
        return emails

    except IMAP4_SSL.error as e:
        error("An error occurred while fetching mail: " + str(e))

def _get_attachements(mail) -> list:
    atts = []
    for part in mail.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        
        atts.append(part)

    return atts


def decode_mime_words(s):
    return u''.join(
        word.decode(encoding or 'utf8') if isinstance(word, bytes) else word
        for word, encoding in email.header.decode_header(s))


def _get_attachement_files(attachement: object) -> list:
        filename = decode_mime_words(attachement.get_filename())
        path = os.path.join(storage_dir, filename + '_' + uuid4().hex)

        if not os.path.isfile(path):
            # At this point we're sure we can write the attachement to disk
            if not os.path.exists(storage_dir):
                os.makedirs(storage_dir)

            fp = open(path, 'wb')
            fp.write(attachement.get_payload(decode=True))
            fp.close()

            yield {
                'filename': filename,
                'path': path,
            }