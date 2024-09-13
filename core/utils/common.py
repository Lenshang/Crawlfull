import re
import threading
import os
from hashlib import md5


def clean_url(origin_url):
    try:
        return re.search("^.*?\:\/\/(((?!#).)+)", origin_url)[1]
    except:
        return None


def md5hex(value):
    return md5(value.encode()).hexdigest()


def get_pid_tid():
    pid = str(os.getpid())
    tid = str(threading.current_thread().ident)
    return ":".join([pid, tid])
