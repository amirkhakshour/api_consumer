import json
from urllib.parse import urlencode
from api_consumer import settings
from api_consumer.clients import RequestsRequesterClient
from api_consumer.urls import encode_url_params, build_api_url


class APIRequester:
    client = RequestsRequesterClient

    def __init__(self, api_base=None, client=None):
        self.api_base = api_base or settings.API_BASE_URL
        self._client = client or self.client()

    def build_url(self, url, params=None):
        abs_url = "%s%s" % (self.api_base, url)
        if params:
            encoded_params = urlencode(list(encode_url_params(params or {})))
            encoded_params = encoded_params.replace("%5B", "[").replace("%5D", "]")
            abs_url = build_api_url(abs_url, encoded_params)
        return abs_url

    def request(self, method, url, params):
        """Sends request and process response.
        :param method: HTTP Methods
        :param url: relative URL to API base url
        :param params: additional params for API request
        :return:
        """
        abs_url = self.build_url(url, params)
        content, status_code, headers = self._client.request(method, abs_url)
        return self.interpret_response(content, status_code, headers)

    def interpret_response(self, content, status_code, headers):
        if hasattr(content, "decode"):
            content = content.decode("utf-8")
        return json.loads(content)
