from api_consumer.requester import APIRequester
from urllib.parse import quote_plus


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
    def instance_url(cls, _id):
        base = cls.obj_name.replace(".", "/")
        _id_encoded = quote_plus(_id)
        return "%s/%s" % (base, _id_encoded)

    @classmethod
    def list(cls, **params):
        url = cls.type_url()
        requester = cls.api_requester()
        return requester.request("get", url, params)

    @classmethod
    def retrieve(cls, _id, **params):
        requester = cls.api_requester()
        url = cls.instance_url(_id)
        return requester.request("get", url, params)
