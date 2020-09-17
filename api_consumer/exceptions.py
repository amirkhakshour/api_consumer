class APIError(Exception):
    def __init__(
        self, message, http_body=None, http_status=None, code=None,
    ):
        super().__init__(message)
        self.message = message
        self.http_body = http_body
        self.http_status = http_status
        self.code = code


class APIConnectionError(APIError):
    def __init__(self, *args, should_retry=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.should_retry = should_retry
