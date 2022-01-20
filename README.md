# Mailscan

Mailscan is an application built with 2 Dockers to automate ocr-ing pdfs (presumably sent by your scanner by mail to a dedicated mailbox), and uploading them to a webdav server (like Nextcloud).

Basically it is a combination of [Rocketload](https://gitlab.com/aagreb/rocketload/-/tree/master/rocketload), extended with a module to send files to a [ocrmypdf](https://github.com/ocrmypdf/OCRmyPDF) docker to ocr them. After this, the file is uploaded to a webdav server.

The purpose of this is to automate scanning paper mail: the scanner has an email address in the adresbook where the (pdf) scans are sent. 
The application fetches mail from this addres (and deletes them), and uploads the ocr'ed scans to a webdavserver, so they can be indexed.

## Installation

On a machine that has a recent version of Docker installed (including docker compose):
- copy the `docker-compose.yml` file in a directory
- copy the `mailscan.json.example` file, and rename it to `mailscan.json`
- edit the `mailscan.json` file 
- start the proces with `docker-compose up`
- you can make it a systemd service

There is no need to build the docker image; a pre-built will be pulled. Unless you want to change any functionality, only `docker-compose.yml` and `mailscan.json` are needed

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
**`ocr.scanname`**: static name from your scanner this will be converted to a name with a timestamp


Example of full configuration:

```json
{
    "pollInterval": 3,
    "imap": {
        "host": "imap.gmail.com",
        "user": "john.doe@gmail.com",
        "password": "secretpassword",
	"folder": "INBOX",
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

## Make it a systemd-service

If you want this to run on a Linux server somewhere, why not make it a systemd service.
prerequisites: make sure Docker and docker-compose are installed

create a file `/etc/systemd/system/mailscan.service` like this:

```
[Unit]
Description=mailscan and ocrmypdf in Docker-compose (/srv/ocrmypdf)
Requires=docker.service
After=docker.service

[Service]
Restart=always
WorkingDirectory=/srv/ocrmypdf
ExecStart=/usr/local/bin/docker-compose -f /srv/ocrmypdf/docker-compose.yml up
ExecStop=/usr/local/bin/docker-compose -f /srv/ocrmypdf/docker-compose.yml stop

[Install]
WantedBy=multi-user.target
```
(assuming everything is in `/srv/ocrmypdf`)

issue these commands:

`systemctl daemon-reload`

`systemctl enable mailscan.service`

`systemctl start mailscan.service`


logfile can be inspected with 

`journalctl -u mailscan.service -f`

## Contributing

Feel free to create an issue or open a merge request.

