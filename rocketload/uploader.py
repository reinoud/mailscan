import requests
import os
from urllib.parse import urljoin, urlparse, urlunparse, ParseResult
from .util import error

def upload(conf: dict, attachements: dict) -> None:
    url = conf['webdav']['url']
    auth = (conf['webdav']['username'], conf['webdav']['password'])

    try:
        for att in attachements:
            # Prepare request
            parsed = urlparse(url)
            path = os.path.join(parsed.path, att['filename'])
            newUrl = ParseResult(parsed.scheme, parsed.netloc, path, parsed.params, parsed.query, parsed.fragment)
            finalUrl = urlunparse(newUrl)
            file = open(att['path'])

            # Upload file
            resp = requests.put(url=finalUrl, data=file, auth=auth)

            if not resp.ok:
                error("HTTP Failure while uploading files to WebDav server: HTTP Status Code %i" % resp.status_code)

            # Clean file
            try:
                os.remove(att['path'])
            except OSError:
                pass # Don't care if file doesn't exist anymore

    except Exception as e:
        error("There was an error while uploading the attachements: " + str(e))

    print("Successfully uploaded %i files" % len(attachements))
    