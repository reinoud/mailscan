import requests
import os
from urllib.parse import urljoin, urlparse, urlunparse, ParseResult
from .util import error

def upload(conf: dict, attachements: list) -> None:
    url = conf['webdav']['url']
    auth = (conf['webdav']['username'], conf['webdav']['password'])

    try:
        for att in attachements:
            # Prepare request
            parsed = urlparse(url)
            path = os.path.join(parsed.path, att['filename'])
            try:
                newUrl = ParseResult(parsed.scheme, parsed.netloc, path, parsed.params, parsed.query, parsed.fragment)
            except Exception as e:
                print(f'problem with Parseresult : {e}')

            finalUrl = urlunparse(newUrl)
            print(f'finalURL is {finalUrl}')
            try:
                file = open(att['path'], 'rb')
            except Exception as e:
                print(f'problem opening file: {e}')

            # Upload file
            try:
                resp = requests.put(url=finalUrl, data=file, auth=auth)
            except Exception as e:
                print(f'exception during upload: {e}')

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
    