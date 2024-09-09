import re
from hashlib import md5


def clean_url(origin_url):
    try:
        return re.search("^.*?\:\/\/(((?!#).)+)", origin_url)[1]
    except:
        return None


def md5hex(value):
    return md5(value.encode()).hexdigest()
