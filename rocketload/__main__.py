import threading
import sched, time
from .config import get_config
from .util import error
from .fetcher import fetch_attachements
from .uploader import upload

s = sched.scheduler(time.time, time.sleep)

def main():
    try:
        conf = get_config()
        print("Configuration successfully parsed")
    except Exception as e:
        error("Invalid configuration: " + str(e))

    print("Starting rocketload at poll interval of %i seconds..." % conf['pollInterval'])
    s.enter(0, 1, executor, (conf,))
    s.run()

def executor(conf): 
    attachements = fetch_attachements(conf) # Get attachements
    upload(conf, attachements) # Upload attachements

    s.enter(conf['pollInterval'], 1, executor, (conf,)) # Repeat ...

if __name__ == '__main__':
    main()