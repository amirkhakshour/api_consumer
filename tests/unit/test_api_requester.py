import pytest
import api_consumer
from api_consumer import settings


class TestAPIRequester(object):
    @pytest.fixture
    def http_client(self, mocker):
        client = mocker.Mock(api_consumer.clients.RequesterClient)
        client.name = "mockedclient"
        return client

    @pytest.fixture
    def requester(self, http_client):
        requester = api_consumer.requester.APIRequester(client=http_client)
        return requester

    @pytest.fixture
    def mock_response(self, mocker, http_client):
        def mock_response(return_content, return_code, return_headers=None):
            http_client.retry_request = mocker.Mock(
                return_value=(return_content, return_code, return_headers or {})
            )

        return mock_response

    @pytest.fixture
    def check_call(self, http_client):
        def check_call(method, abs_url=settings.API_BASE_URL):
            http_client.retry_request.assert_called_with(
                method, abs_url
            )

        return check_call

    def test_url_construction(self, requester, mock_response, check_call):
        base_url = settings.API_BASE_URL
        cases = (
            (base_url, "", {}),
            ("%sendpoint1" % base_url, "endpoint1", {}),
            ("%sendpoint1?foo=bar" % base_url, "endpoint1", {"foo": "bar"}),
        )
        for expected, url, params in cases:
            mock_response("{}", 200)
            requester.request("get", url, params)
            check_call("get", expected)
