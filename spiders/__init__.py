import os
import importlib

# 动态加载站点模组
for file in os.listdir(os.path.dirname(__file__)):
    mod_name = file[:-3]  # strip .py at the end
    if mod_name[0] != "_":
        importlib.import_module("." + mod_name, package=__name__)
