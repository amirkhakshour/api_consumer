import pytest
import api_consumer


DUMMY_URL = 'https://dummy'


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
        return request_mocks[str(self.REQUESTER_CLIENT.name)]

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


class TestRequestsRequesterClient(TestRequesterClientBase):
    REQUESTER_CLIENT = api_consumer.clients.RequestsRequesterClient

    @pytest.fixture
    def requests_session(self, mocker, request_mocks):
        return mocker.MagicMock()

    @pytest.fixture
    def mock_error(self, mocker, requests_session):
        def mock_error(mock):
            # make isinstance for error handler work
            mock.exceptions.Timeout = Exception
            requests_session.request.side_effect = mock.exceptions.Timeout()
            # override Session of mocked requests in order to be able to trigger side_effect
            mock.Session = mocker.MagicMock(return_value=requests_session)

        return mock_error

    def make_request(self, method, url, headers):
        client = self.REQUESTER_CLIENT()
        return client.request(method, url, headers)

    def test_exception(self, request_mock, mock_error):
        mock_error(request_mock)
        with pytest.raises(api_consumer.exceptions.APIConnectionError):
            self.make_request("get", DUMMY_URL, {})
