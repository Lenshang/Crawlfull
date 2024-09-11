from collections.abc import MutableMapping
from dataclasses import dataclass, asdict, astuple
import json
from pprint import pformat
from typing import Any, Dict, Iterator, KeysView


class CrawlfItem:
    def to_dict(self) -> Dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def to_tuple(self) -> tuple:
        return astuple(self)
