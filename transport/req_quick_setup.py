from .request import Request
from .response import Response


class RequestQuickSetup(Request):

    def __init__(self):
        super().__init__('qs_component_nego')

    def parse_response(self, resp):
        return ResponseQuickSetup(resp)


class ResponseQuickSetup(Response):

    def __init__(self, bytes):
        self.device_type = ''
        self.device_model = ''
        self.components = []
        super().__init__(bytes)

    def parse_result(self, result):
        self.device_type = result['extra_info']['device_type']
        self.device_model = result['extra_info']['device_model']
        self.components = result['component_list']

    def get_model(self):
        return self.device_model

    def get_type(self):
        return self.device_type

    def get_components(self):
        return self.components
