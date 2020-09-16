from api_consumer.endpoints.abc import APIEndpoint


class TestAPIEndpoint(object):
    class MyAPIEndpoint(APIEndpoint):
        pass

    def test_list(self):
        pass
