import time

from .http_request import HttpRequest
from .http_response import HttpResponse


class RequestSetDeviceInfo(HttpRequest):

    def __init__(self, enable: bool):
        super().__init__('set_device_info', 'params',
                         {
                             'device_on': enable,
                         })

    def parse_response(self, resp):
        return ResponseSetDeviceInfo(resp)


class ResponseSetDeviceInfo(HttpResponse):

    def __init__(self, data):
        self.key = None
        super().__init__(data)

    def parse_result(self, result):
        pass
