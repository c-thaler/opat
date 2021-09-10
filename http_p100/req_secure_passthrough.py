import time

from .http_request import HttpRequest
from .http_response import HttpResponse
from .tp_link_cipher import TpLinkCipher


class RequestSecurePassthrough(HttpRequest):

    def __init__(self, cipher: TpLinkCipher, payload: HttpRequest):
        enc_payload = self.tpLinkCipher.encrypt(payload.get_payload())
        super().__init__('securePassthrough', 'params',
                         {
                             'request': payload,
                         })

    def parse_response(self, resp):
        return ResponseSecurePassthrough(resp)


class ResponseSecurePassthrough(HttpResponse):

    def __init__(self, data):
        self.response = None
        super().__init__(data)

    def parse_result(self, result):
        self.response = result['result']['response']

    def get_response(self):
        return self.response
