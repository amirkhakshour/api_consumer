import pytest


class TestRequesterClientBase:
    REQUESTER_CLIENTS = ["requests", ]

    @pytest.fixture
    def request_mocks(self, mocker):
        """
        mock external request libs
        :param mocker:
        :return:
        """
        request_mocks = {}
        for lib in self.REQUESTER_CLIENTS:
            request_mocks[lib] = mocker.patch("api_consumer.clients.%s" % (lib,))
        return request_mocks

    @pytest.fixture
    def request_mock(self, request_mocks):
        return request_mocks[self.REQUESTER_CLIENT.name]

    def make_request(self, method, url, headers):
        client = self.REQUESTER_CLIENT()
        return client.request(method, url, headers)

    @pytest.fixture
    def mock_response(self):
        def mock_response(mock, body, code):
            raise NotImplementedError(
                "You must implement this in your test subclass"
            )

        return mock_response

    @pytest.fixture
    def mock_error(self):
        def mock_error(mock, error):
            raise NotImplementedError(
                "You must implement this in your test subclass"
            )

        return mock_error


