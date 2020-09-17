import requests
import json
from api_consumer import settings
from api_consumer.clients import RequestsRequesterClient


class APIRequester:
    client = RequestsRequesterClient

    def __init__(self, api_base=None, client=None):
        self.api_base = api_base or settings.API_BASE_URL
        self._client = client or self.client()

    def request(self, method, url, params=None):
        """

        :param method: HTTP Methods
        :param url: relative URL to API base url
        :param params: additional params for API request
        :return:
        """
        abs_url = "%s%s" % (self.api_base, url)
        content, status_code, headers = self._client.request(method, abs_url)
        return self.interpret_response(content, status_code, headers)

    def interpret_response(self, content, status_code, headers):
        if hasattr(content, "decode"):
            content = content.decode("utf-8")
        return json.loads(content)
