import time

from .http_request import HttpRequest
from .http_response import HttpResponse


class RequestLogin(HttpRequest):

    def __init__(self, username: str, password: str):
        super().__init__('login_device', 'params',
                         {
                             'username': username,
                             'password': password,
                         })

    def parse_response(self, resp):
        return ResponseLogin(resp)


class ResponseLogin(HttpResponse):

    def __init__(self, data):
        self.token = None
        super().__init__(data)

    def parse_result(self, result):
        self.token = result['result']['token']

    def get_token(self):
        return self.token
