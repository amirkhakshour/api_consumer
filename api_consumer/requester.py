import requests


class APIRequester:
    def __init__(self):
        self._client = requests.Session()

    def request(self, method, url, params=None):
        result = self._client.request(method, url)
        return self.convert_response(result)

    def convert_response(self, result):
        return result.json()
