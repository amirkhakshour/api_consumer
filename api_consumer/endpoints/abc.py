import json
from api_consumer.requester import APIRequester

API_BASE_URL = "https://ghibliapi.herokuapp.com/"


class APIEndpoint:
    """APIEndpoint base class"""
    api_requester = APIRequester

    def __init__(self):
        pass

    @classmethod
    def type_url(cls):
        base = cls.obj_name.replace(".", "/")
        return "%s" % (base,)

    @classmethod
    def list(cls, **params):
        url = '%s%s' % (API_BASE_URL, cls.type_url())
        requester = cls.api_requester()
        return requester.request("get", url, params)
