import pytest
from tests.request_mock import RequestMock


@pytest.fixture
def request_mock(mocker):
    return RequestMock(mocker)
