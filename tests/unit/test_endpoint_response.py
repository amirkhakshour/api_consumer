import json
from collections import OrderedDict

from api_consumer.response import EndpointResponse


class TestEndpointResponse(object):
    @staticmethod
    def mock_endpoint_response(status_code=200):
        headers = TestEndpointResponse.mock_headers()
        body = TestEndpointResponse.mock_body()
        response = EndpointResponse(body, status_code, headers)
        return response, headers, body, status_code

    @staticmethod
    def mock_headers():
        return {"example-header-1": "val1", "example-header-2": "val-2"}

    @staticmethod
    def mock_body():
        return """{
            "id": "598f7048-74ff-41e0-92ef-87dc1ad980a9",
            "name": "Lusheeta Toel Ul Laputa",
            "gender": "Female",
            "age": "13",
            "eye_color": "Black",
            "hair_color": "Black",
            "ordered_data": {
                "item1": "val1",
                "item2": "val2",
                "item3": "val3",
                "item4": "val4",
                "item5": "val5"
            }
        }
        """

    def test_code(self):
        response, _, _, status_code = self.mock_endpoint_response()
        assert response.status_code == status_code

    def test_headers(self):
        response, headers, _, _ = self.mock_endpoint_response()
        assert response.headers == headers

    def test_body(self):
        response, _, body, _ = self.mock_endpoint_response()
        assert response.body == body

    def test_data(self):
        response, _, body, _ = self.mock_endpoint_response()
        deserialized = json.loads(body, object_pairs_hook=OrderedDict)
        assert response.data == deserialized
        assert response.data["ordered_data"].keys() == deserialized["ordered_data"].keys()
