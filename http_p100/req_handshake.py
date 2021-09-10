import time

from .http_request import HttpRequest
from .http_response import HttpResponse


class RequestHandshake(HttpRequest):

    def __init__(self, key: str):
        super().__init__('handshake', 'params',
                         {
                             'key': key,
                             'requestTimeMils': int(round(time.time() * 1000)),
                         })

    def parse_response(self, resp):
        return ResponseHandshake(resp)


class ResponseHandshake(HttpResponse):

    def __init__(self, data):
        self.key = None
        super().__init__(data)

    def parse_result(self, result):
        self.key = result['result']['key']

    def get_key(self):
        return self.key
