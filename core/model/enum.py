from enum import Enum


class ArticleState(Enum):
    init = 0
    downloaded = 1
    parsed = 2
    media_downloaded = 3
    processed = 4
    failed = -1
    completed = 100


class ArticleType(Enum):
    html = 1
    pdf = 2
    image = 3
    other = 99


class SpiderState(Enum):
    enable = 1
    disable = 0


class Language(Enum):
    zh_CN = "zh-CHS"
    zh_TW = "zh-CHT"
    zh_HK = "zh-CHT"
    zh_CHS = "zh-CHS"
    zh_CHT = "zh-CHT"
    en = "en"
    ja = "ja"
    ko = "ko"
    ru = "ru"
    vi = "vi"
    th = "th"
    ar = "ar"
    he = "he"
    fa = "fa"
    hi = "hi"
    bn = "bn"
    de = "de"
    fr = "fr"
    it = "it"
    es = "es"
    tr = "tr"
    pt = "pt"
    nl = "nl"
    pl = "pl"
    ro = "ro"
    id = "id"


def get_enum_by_value(enum_class: Enum, value):
    return enum_class._value2member_map_.get(value)


def get_enum_name_by_value(enum_class: Enum, value):
    r = get_enum_by_value(enum_class, value)
    if r:
        return r.name
    else:
        return None
