import config


def test():
    print(config.get("COMMON", "ENV"))
