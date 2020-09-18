import abc
import requests
from retry import retry

from api_consumer import exceptions
from api_consumer import settings


class RequesterClient(abc.ABC):
    @abc.abstractmethod
    def request(self, method, url, headers=None, **kwargs):
        raise NotImplementedError(
            "RequesterClient children must implement `request` method!"
        )

    @property
    @abc.abstractmethod
    def name(self):
        raise NotImplementedError(
            "RequesterClient children must provide `name` property!"
        )

    @abc.abstractmethod
    def handle_request_error(self, e):
        raise NotImplementedError(
            "RequesterClient children must implement `handle_request_error` method!"
        )

    @retry(
        exceptions.APIConnectionError,
        tries=settings.MAX_NETWORK_RETRIES,
        delay=settings.DELAY_NETWORK_RETRY,
    )
    def retry_request(self, method, url, headers=None, **kwargs):
        return self.request(method, url, headers, **kwargs)


class RequestsRequesterClient(RequesterClient):
    name = "requests"

    def handle_request_error(self, e):
        msg = "Unexpected error happened during communicating with Endpoint."
        if isinstance(
            e, (requests.exceptions.Timeout, requests.exceptions.ConnectionError,)
        ):
            err = "%s: %s" % (type(e).__name__, str(e))
            should_retry = True
        elif isinstance(e, requests.exceptions.RequestException):
            err = "%s: %s" % (type(e).__name__, str(e))
            should_retry = False
        else:
            err = "A %s was raised" % (type(e).__name__,)
            if str(e):
                err += " with error message %s" % (str(e),)
            else:
                err += " with no error message"
            should_retry = False

        msg = msg + "\n\n(Network error: %s)" % (err,)
        raise exceptions.APIConnectionError(msg, should_retry=should_retry)

    def request(self, method, url, headers=None, **kwargs):
        session = requests.Session()
        try:
            result = session.request(method, url)
            content = result.content
            status_code = result.status_code
        except Exception as e:
            self.handle_request_error(e)
        return content, status_code, result.headers
