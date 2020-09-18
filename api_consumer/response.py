import json
from collections import OrderedDict


class EndpointResponse(object):
    def __init__(self, body, status_code, headers):
        self.body = body
        self.status_code = status_code
        self.headers = headers
        self.data = json.loads(body, object_pairs_hook=OrderedDict)
