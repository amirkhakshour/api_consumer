import requests
import json
from api_consumer.clients import RequestsRequesterClient


class APIRequester:
    client = RequestsRequesterClient

    def __init__(self):
        self._client = self.client()

    def request(self, method, url, params=None):
        content, status_code, headers = self._client.request(method, url)
        return self.interpret_response(content, status_code, headers)

    def interpret_response(self, content, status_code, headers):
        if hasattr(content, "decode"):
            content = content.decode("utf-8")
        return json.loads(content)
