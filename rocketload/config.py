from .util import error

_config_file = "/rocketload.json"

def get_config() -> dict:
    return _get_file_content()

def _get_file_content() -> str:
    try:
        with open(_config_file, 'r') as content_file:
            content = content_file.read()
    except:
        raise Exception("Rocketload config file at '%s' not found." % _config_file)
    return content
    