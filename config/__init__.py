import os
import sys
import configparser


class ConfigModule(object):
    def __init__(self):
        self._config = configparser.ConfigParser()
        file_path = f'config/config.{os.environ.get("ENV")}.ini'
        if not os.path.exists(file_path):
            file_path = f"config.default.ini"
        self._config.read(file_path)

    def __getitem__(self, name):
        return self._config[name]

    def get(self, *args, **kwargs):
        return self._config.get(*args, **kwargs)

    def getint(self, *args, **kwargs):
        return self._config.getint(*args, **kwargs)

    def getfloat(self, *args, **kwargs):
        return self._config.getfloat(*args, **kwargs)

    def getboolean(self, *args, **kwargs):
        return self._config.getboolean(*args, **kwargs)


sys.modules["config"] = ConfigModule()
