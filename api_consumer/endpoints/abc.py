import json
import requests

API_BASE_URL = "https://ghibliapi.herokuapp.com/"


class APIEndpoint:

    def __init__(self):
        pass

    @classmethod
    def list(cls, **params):
        session = requests.Session()
        url = '%s%s' % (API_BASE_URL, cls.obj_name)
        result = session.request('get', url)
        result.json()
        return result.json()
