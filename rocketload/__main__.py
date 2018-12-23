import threading
import sched, time
from .config import get_config
from .util import error

s = sched.scheduler(time.time, time.sleep)

def main():
    try:
        conf = get_config()
    except Exception as e:
        error("Invalid configuration: " + str(e))

    s.enter(0, 1, executor, (conf,))
    s.run()

def executor(conf): 
    print(conf)
    s.enter(3, 1, executor, (conf,))

if __name__ == '__main__':
    main()