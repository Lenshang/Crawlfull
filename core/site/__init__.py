import re
import os
import importlib
import traceback
import config
from ExObject.ExParsel import ExSelector
from urllib.parse import urljoin

_creator = {}


def reg_creator(domain, language, enable=True, downloader=None, debug=False):
    def decorator(func):
        _creator[domain] = {"domain": domain, "func": func, "language": language, "enable": enable, "debug": debug}
        return func

    return decorator


def get_creator():
    debug_mode = False
    if config.get("COMMON", "ENV") == "develop":
        debug_mode = any(item["debug"] for item in _creator.values())
    for domain in _creator.keys():
        item = _creator[domain]
        if debug_mode and not item["debug"]:
            pass
        elif item["enable"]:
            try:
                for item in item["func"](item):
                    if item:
                        yield item
            except:
                traceback.print_exc()
