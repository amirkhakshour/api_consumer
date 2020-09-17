import json
from api_consumer.endpoints.abc import APIEndpoint


class TestAPIEndpoint(object):
    class MyAPIEndpoint(APIEndpoint):
        obj_name = "people"

    def test_is_listable(self, request_mock):
        expected_response = [{"field": "value"}]
        request_mock.stub_request(
            "get",
            "people",
            expected_response,
        )
        resources = self.MyAPIEndpoint.list()
        assert isinstance(resources, str)
        assert resources == json.dumps(expected_response)
        request_mock.assert_requested("get", "people")
