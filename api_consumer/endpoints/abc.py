import abc
from marshmallow import EXCLUDE
from urllib.parse import quote_plus
from cachetools import cached, TTLCache

from api_consumer.requester import APIRequester
from api_consumer.response import EndpointResponse
from api_consumer import settings


class APIEndpoint(abc.ABC):
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
    @cached(
        cache=TTLCache(
            maxsize=settings.CACHED_LIST_MAX_ITEMS, ttl=settings.CACHED_LIST_ENDPOINTS
        )
    )
    def list(cls, **params):
        url = cls.type_url()
        requester = cls.api_requester()
        response = requester.request("get", url, params)
        return cls.convert_response(response)

    @classmethod
    @cached(
        cache=TTLCache(
            maxsize=settings.CACHED_RETRIEVE_MAX_ITEMS,
            ttl=settings.CACHED_RETRIEVE_ENDPOINTS,
        )
    )
    def retrieve(cls, _id, **params):
        requester = cls.api_requester()
        url = cls.instance_url(_id)
        response = requester.request("get", url, params)
        return cls.convert_response(response)

    @classmethod
    def convert_response(cls, response):
        """Flattening response and calling validator inside `construct_from`."""
        if isinstance(response, EndpointResponse):
            _resp = response
            response = _resp.data

        if isinstance(response, list):
            return [cls.convert_response(item) for item in response]
        elif isinstance(response, dict):
            return cls.construct_from(response)
        else:
            return response

    @classmethod
    @abc.abstractmethod
    def construct_from(cls, resp):
        raise NotImplemented(
            "APIEndpoint children must implement `construct_from` method!"
        )


class APIEndpointSchemaConverter:
    @classmethod
    def construct_from(cls, response):
        return cls.schema().load(response, unknown=EXCLUDE)
