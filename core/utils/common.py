import re
import threading
import os
from hashlib import md5
from croniter import croniter
from datetime import datetime


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


def now():
    return datetime.now()


def now_ts():
    """获得当前时间13位时间戳"""
    return int(now().timestamp() * 1000)


def get_next_runtime(cron, start):
    cr = croniter(cron)
    r = cr.get_next(start_time=start / 1000)
    _now = now().timestamp()
    while r < _now:
        r = cr.get_next(start_time=r)
    return int(r * 1000)
