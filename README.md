# Mailscan

Mailscan is an application built with 2 Dockers to automate ocr-ing pdfs (presumably sent by your scanner by mail to a dedicated mailbox), and uploading them to a webdav server (like Nextcloud).

Basically it is a combination of [Rocketload](https://gitlab.com/aagreb/rocketload/-/tree/master/rocketload), extended with a module to send files to a [ocrmypdf](https://github.com/ocrmypdf/OCRmyPDF) docker to ocr them. After this, the file is uploaded to a webdav server.

The purpose of this is to automate scanning paper mail: the scanner has an email address in the adresbook that where the (pdf) scans are sent. 
The application fetches mail from this addres (and deletes them), and uploads the ocr'ed scans to a webdavserver, so they can be indexed.
## Installation

On a machine that has a recent version of Docker installed (including docker compose):
- copy the `docker-compose.yml` file in a directory
- copy the `mailscan.json.example` file, and rename it to `mailscan.json`
- edit the `mailscan.json` file 
- start the proces with `docker-compose up`
- you can make it a systemd service

Note: this can be any machine, as long as it can reach the mailbox and the webdav server.


### Configuration

The configuration cosist of a JSON file called `mailscan.json`. It has following keys:

**`pollInterval`**: How many seconds between every poll to the email server

**`imap`**: Configuration of IMAP server  
**`imap.host`**: Host of IMAP server  
**`imap.user`**: IMAP username  
**`imap.password`**: IMAP password  
**`imap.folder`**: The IMAP folder to look for mails in  
**`imap.deletefetched`**: Remove fetched mails from mailbox (useful when you have a dedicated mailbox)


**`webdav`**: WebDav configuration  
**`webdav.url`**: URL of WebDav folder to upload files to  
**`webdav.username`**: WebDav username  
**`webdav.password`**: WebDav password  

**`ocr`**: ocr configuration  
**`ocr.containername`**: name of the service in `docker-compose.yml`  
**`ocr.containerport`**: port of the service in `docker-compose.yml`
**`ocr.scanname`**: static name from your scanner; this will be converted to a name with a timestamp


Example of full configuration:

```json
{
    "pollInterval": 3,
    "imap": {
        "host": "imap.gmail.com",
        "user": "john.doe@gmail.com",
        "password": "secretpassword",
	    "folder": "rocketload_mails",
        "deletefetched": true
    },
    "webdav": {
        "url": "https://my.webdav.server/mydata/mailscan/uploads",
        "username": "john",
        "password": "passwordSecret"
    },
    "ocr": {
        "containername": "ocrmypdf-webservice",
        "containerport": 5000,
        "scanname": "scan.pdf"
  }
}

```


## Contributing

Feel free to create an issue or open a merge request.

