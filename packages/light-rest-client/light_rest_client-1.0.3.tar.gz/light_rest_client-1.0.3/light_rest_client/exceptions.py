class HTTPClientException(Exception):
    def __init__(self, message, code):
        super().__init__(message)
        self.code = code


class HTTPServerException(Exception):
    def __init__(self, message, code):
        super().__init__(message)
        self.code = code


def detect_exception(code):
    for target in range(400, 418):
        if target == code:
            raise HTTPClientException(message="HTTP Client Exception", code=code)

    if code == 451:
        raise HTTPClientException(message="HTTP Client Exception", code=code)

    for target in range(500, 511):
        if target == code:
            raise HTTPServerException(message="HTTP Server Exception", code=code)

    pass
