import re
from core.model.article_info import ArticleInfo

_parser = {}


def reg_parser(match_url, skip_image_download=False, skip_vertical_crawl=False, max_deep=3):
    def decorator(func):
        key = func.__module__ + "." + func.__name__
        _parser[key] = {
            "match_url": match_url,
            "func": func,
            "skip_image_download": skip_image_download,
            "skip_vertical_crawl": skip_vertical_crawl,
            "max_deep": max_deep,
        }
        return func

    return decorator


def get_parser(articleinfo: ArticleInfo):
    if articleinfo.parser and articleinfo.parser != "default":
        return _parser.get(articleinfo.parser)

    for name, parser_item in _parser.items():
        rg_pt = parser_item.get("match_url")
        if re.search(rg_pt, articleinfo.url):
            return parser_item
    return None
