# Rocketload

Rocketload is a simple and dockerized commandline application written in python. The goal of this application is it to download attachements of an IMAP email account and upload them on to a WebDav server. This application was developed to solve the problem that it is currently not possible to upload [Rocketbook](https://getrocketbook.co.uk/) files to a WebDav server. It is possible to send Files to an email address though. So rocketload can be used to upload Rocketbook Files to a WebDav server. Although rocketload was developed for this particular use-case it can be used for non-Rocketbook use-cases.

## Installation

It is possible to run rocketload without [Docker](https://www.docker.com/). This is not recommended and not supported though. So this installation guide requires you to have docker installed. You don't have to build the docker image yourself. You can use the prebuilt images from [Dockerhub](https://hub.docker.com/r/aagreb/rocketload).

### Preparation

Create a new directory where all rocketload stuff shall be stored.

```bash
mkdir rocketload
```

Change into the directory

```bash
cd rocketload
```

Create empty config file. Rocketload configuration is discussed later.

```bash
touch rocketload.json
```

Create `docker-compose.yml` with following contents:

```yml
version: '3.5'

services:
    rocketload:
        restart: always
        image: aagreb/rocketload
        volumes:
            - ./rocketload.json:/rocketload.json

```

### Configuration

The configuration cosist of a JSON file called `rocketload.json`. It has following keys:

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
        "url": "https://my.webdav.server/mydata/rocketload/uploads",
        "username": "john",
        "password": "passwordSecret"
    }
}

```

### Running

Now you can run rocketload with `docker-compose up -d`.

## Contributing

Feel free to create an issue or open a merge request.

