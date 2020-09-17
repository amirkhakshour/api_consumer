from api_consumer.urls import encode_url_params


def test_dict_list_encoding():
    params = {"foo": {"0": {"bar": "bat"}}}
    encoded = list(encode_url_params(params))
    key, value = encoded[0]

    assert key == "foo[0][bar]"
    assert value == "bat"
