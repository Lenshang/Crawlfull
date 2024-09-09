import requests
import os


class ClientRequest:
    def __init__(self) -> None:
        self.retry = 5
        self.retry_interval = 1
        self.headers = {
            "accept": "*/*",
            "accept-language": "en,zh-CN;q=0.9,zh;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5",
            "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-csrf-protection": "1",
            "Referrer-Policy": "origin-when-cross-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
        }

    def get(self, url, _retry=0, **kwargs):
        try:
            if kwargs.get("d_proxies"):
                if os.environ.get("DEPLOY_ENV") == "develop":
                    kwargs["proxies"] = kwargs["d_proxies"]
                del kwargs["d_proxies"]
            response = requests.get(url, headers=self.headers, **kwargs)
            if response.status_code == 200:
                return response
            elif _retry < self.retry:
                return self.get(url, _retry + 1, **kwargs)
            else:
                return None
        except:
            if _retry < self.retry:
                return self.get(url, _retry + 1, **kwargs)
            else:
                return None

    def post(self, url, body, _retry=0, **kwargs):
        try:
            response = requests.post(url, data=body, headers=self.headers, **kwargs)
            if response.status_code == 200:
                return response
            elif _retry < self.retry:
                return self.post(url, body, _retry + 1, **kwargs)
            else:
                return None
        except:
            if _retry < self.retry:
                return self.post(url, body, _retry + 1, **kwargs)
            else:
                return None
