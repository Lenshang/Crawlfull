import re
import os
import importlib
import traceback
import config
from ExObject.ExParsel import ExSelector
from urllib.parse import urljoin

_creator = {}


def reg_creator(domain, cron="", language="zh-Hans", enable=True, debug=False):
    def decorator(func):
        _creator[domain] = {"domain": domain, "func": func, "language": language, "enable": enable, "debug": debug}
        return func

    return decorator


def debug_creator():
    debug_mode = False
    if config.get("COMMON", "ENV") == "dev":
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


# 动态加载模组
for file in os.listdir(os.path.dirname(__file__)):
    mod_name = file[:-3]  # strip .py at the end
    if mod_name[0] != "_":
        importlib.import_module("." + mod_name, package=__name__)
