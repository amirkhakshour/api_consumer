from urllib.parse import urlencode
from api_consumer import settings

from api_consumer import exceptions
from api_consumer.clients import RequestsRequesterClient
from api_consumer.urls import encode_url_params, build_api_url
from api_consumer.response import EndpointResponse


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
        content, status_code, headers = self._client.retry_request(method, abs_url)
        return self.interpret_response(content, status_code, headers)

    def interpret_response(self, resp_body, resp_code, resp_headers):
        try:
            if hasattr(resp_body, "decode"):
                resp_body = resp_body.decode("utf-8")
            response = EndpointResponse(resp_body, resp_code, resp_headers)
        except Exception:
            raise exceptions.APIError(
                "Invalid response body from API: %s "
                "(HTTP response code was %d)" % (resp_body, resp_code),
                resp_body,
                resp_code,
                resp_headers,
            )
        return response
