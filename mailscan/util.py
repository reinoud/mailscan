import sys

def error(message: str):
    print(message, file=sys.stderr)
    sys.exit(1)