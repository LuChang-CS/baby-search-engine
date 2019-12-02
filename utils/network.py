import requests

from utils.config import Configuration


class NetWorkConfiguration(Configuration):
    browser_user_agent = 'Mozilla'
    strict = True
    http_timeout = 30

    def __init__(self, config=None):
        super().__init__(config)


class NetworkError(RuntimeError):

    def __init__(self, status_code, reason):
        self.reason = reason
        self.status_code = status_code


class NetworkFetcher:

    def __init__(self, config=None):
        self.config = NetWorkConfiguration(config)

        self._connection = requests.Session()
        self._connection.headers['User-agent'] = self.config.browser_user_agent

        self._url = None
        self.response = None
        self.headers = None

    def close(self):
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def get_url(self):
        return self._url

    def fetch(self, url):
        try:
            response = self._connection.get(url, timeout=self.config.http_timeout, headers=self.headers)
        except Exception:
            return None
        if response.ok:
            self._url = response.url
            text = response.content.decode('utf-8')
        else:
            self._url = None
            text = None
            if self.config.strict:
                raise NetworkError(response.status_code, response.reason)

        return text
