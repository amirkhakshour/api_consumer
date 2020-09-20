import json
from api_consumer.endpoints.abc import APIEndpoint
from api_consumer.response import EndpointResponse

TEST_RESOURCE_ID = "people_123"


class TestAPIEndpoint(object):
    class MyAPIEndpoint(APIEndpoint):
        obj_name = "people"

        @classmethod
        def convert_response(cls, response):
            return response

    def test_is_listable(self, request_mock):
        expected_response = [{"field": "value"}]
        request_mock.stub_request(
            "get",
            "people",
            expected_response,
        )
        resources = self.MyAPIEndpoint.list()
        assert isinstance(resources, EndpointResponse)
        assert resources.data == expected_response
        request_mock.assert_requested("get", "people")

    def test_is_retrievable(self, request_mock):
        resources = self.MyAPIEndpoint.retrieve(TEST_RESOURCE_ID)
        request_mock.assert_requested("get", "people/%s" % TEST_RESOURCE_ID)

