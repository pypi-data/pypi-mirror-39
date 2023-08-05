import os

debug_flag = "_DEBUG"

def debug(obj, title = None):
    if os.environ.get(debug_flag):
        if title:
            print("%s:%s" %( title, obj))
        else:
            print(obj)

    return obj

def debug_on():
    os.environ[debug_flag] = "debug"


def debug_off():
    os.environ[debug_flag] = None
