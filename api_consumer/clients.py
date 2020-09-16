import abc
import requests


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


class RequestsRequesterClient(RequesterClient):
    name = "requests"

    def request(self, method, url, headers=None, **kwargs):
        session = requests.Session()
        resp = session.request(method, url)
        content = resp.content
        status_code = resp.status_code
        return content, status_code, resp.headers
