import json
from api_consumer.requester import APIRequester
from api_consumer import settings


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
        url = cls.type_url()
        requester = cls.api_requester()
        return requester.request("get", url, params)
