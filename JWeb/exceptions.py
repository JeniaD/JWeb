from .response import Response

class HTTPException(Response, Exception):
    def __init__(self, statusCode, name):
        self.statusCode = statusCode
        self.name = name
