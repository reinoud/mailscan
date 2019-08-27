from .util import error
from json import loads

_config_file = "/rocketload.json"

def get_config() -> dict:
    # Get and parse config file
    rawConfig = _get_file_content()
    parsed = loads(rawConfig)

    # Validate config
    if 'pollInterval' not in parsed:
        raise Exception("Key 'pollInterval' not found in config.")

    if 'imap' not in parsed:
        raise Exception("Key 'imap' not found in config.")
    
    if 'host' not in parsed['imap']:
        raise Exception("Key 'imap.host' not found in config.")

    if 'user' not in parsed['imap']:
        raise Exception("Key 'imap.user' not found in config.")

    if 'password' not in parsed['imap']:
        raise Exception("Key 'imap.password' not found in config.")

    if 'folder' not in parsed['imap']:
        raise Exception("Key 'imap.folder' not found in config.")

    if 'deletefetched' not in parsed['imap']:
        raise Exception("Key 'imap.deletefetched' not found in config.")

    if 'webdav' not in parsed:
        raise Exception("Key 'webdav' not found in config.")

    if 'url' not in parsed['webdav']:
        raise Exception("Key 'webdav.url' not found in config.")

    if 'username' not in parsed['webdav']:
        raise Exception("Key 'webdav.username' not found in config.")

    if 'password' not in parsed['webdav']:
        raise Exception("Key 'webdav.password' not found in config.")

    return parsed

def _get_file_content() -> str:
    try:
        with open(_config_file, 'r') as content_file:
            content = content_file.read()
    except:
        raise Exception("Rocketload config file at '%s' not found." % _config_file)
    return content
    