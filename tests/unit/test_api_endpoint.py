from api_consumer.endpoints.abc import APIEndpoint


class TestAPIEndpoint(object):
    class MyAPIEndpoint(APIEndpoint):
        obj_name = "people"

    def test_list(self):
        res = self.MyAPIEndpoint.list()
        assert isinstance(res, list)
