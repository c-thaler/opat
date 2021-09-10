import json


class HttpResponse:
    ERROR_CODES = {
        "-40401": "STok expired.",
        "-64324": "Cannot execute, privacy mode is ON.",
        "-64302": "Preset ID not found.",
        "-64321": "Preset ID no longer exists.",
        "-40106": "Given parameter for get/do does not exist.",
        "-40105": "Method does not exist.",
        "-40101": "Given parameter does not exist.",
    }

    def __init__(self, payload):
        self.error = -1
        self.payload = payload
        self.result = {}
        self.parse_packet()

    def parse_packet(self):
        d = json.loads(self.payload)
        self.error = d['error_code']
        if self.error != 0:
            print(f'Remote device returned error {self.error}: {self.ERROR_CODES[self.error]}')
            return
        self.result = d
        self.parse_result(self.result)

    def parse_result(self, result):
        raise NotImplementedError('Method must be implemented in sub classes.')

    def get_error_code(self):
        return self.error;

    def get_result(self):
        return self.result

    def has_error(self):
        return self.error != 0
