import json
import api_consumer
from api_consumer.response import EndpointResponse


class RequestHandlerStub(object):
    def __init__(self):
        self._lookups = {}

    def register(self, method, url, resp_body=None, resp_code=200, resp_headers=None):
        if resp_body is None:
            resp_body = {}

        if resp_headers is None:
            resp_headers = {}

        self._lookups[(method, url)] = (resp_body, resp_code, resp_headers)

    def get_response(self, method, url):
        if (method, url) in self._lookups:
            resp_body, resp_code, resp_headers = self._lookups.pop((method, url))
            if not isinstance(resp_body, str):
                resp_body = json.dumps(resp_body)
            endpoint_response = EndpointResponse(resp_body, resp_code, resp_headers)
            return endpoint_response

        return None


class RequestMock(object):
    def __init__(self, mocker):
        self._mocker = mocker

        self._request_handler_stub = RequestHandlerStub()

        self.init_patcher = self._mocker.patch(
            "api_consumer.requester.APIRequester.__init__",
            side_effect=api_consumer.requester.APIRequester.__init__,
            autospec=True,
        )

        self.request_patcher = self._mocker.patch(
            "api_consumer.requester.APIRequester.request",
            side_effect=self._patched_request,
            autospec=True,
        )

    def _patched_request(self, requester, method, url, *args, **kwargs):
        return self._request_handler_stub.get_response(method, url)

    def stub_request(self, method, url, resp_body=None, resp_code=200, resp_headers=None):
        if resp_body is None:
            resp_body = {}

        if resp_headers is None:
            resp_headers = {}

        self._request_handler_stub.register(
            method, url, resp_body, resp_code, resp_headers
        )

    def assert_requested(self, method, url, params=None):
        params = params or self._mocker.ANY
        is_called = False
        exception = None

        param_cases = [
            (self._mocker.ANY, method, url),
            (self._mocker.ANY, method, url, params),
        ]

        for args in param_cases:
            try:
                self.request_patcher.assert_called_with(*args)
            except AssertionError as e:
                exception = e
            else:
                is_called = True
                break

        if not is_called:
            raise exception
