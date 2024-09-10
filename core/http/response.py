from typing import Any


class Response(object):
    def __init__(self, code=200, content=None, headers=None, encoding="utf-8"):
        self.code = code
        self.content = content
        self.headers = headers
        self.contentType = ""
        self.encoding = encoding
        self._text = ""
        if headers:
            self.contentType = headers.get("Content-Type")
            if not self.contentType:
                self.contentType = headers.get("content-type")

    def __getattr__(self, name: str) -> Any:
        if name == "text":
            if not self._text:
                self._text = self.content.decode(self.encoding)
            return self._text

    @staticmethod
    def from_pyrequests(resp):
        return Response(
            code=resp.status_code,
            content=resp.content,
            headers=resp.headers,
        )
