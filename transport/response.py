import json
from .packet import Packet


class Response:
    def __init__(self, bytes):
        self.error = -1
        self.packet = Packet(bytes)
        self.result = {}
        self.parse_packet()

    def parse_packet(self):
        d = json.loads(self.packet.get_body().decode())
        self.error = d['error_code']
        if self.error != 0:
            print('Remote device returned error {}'.format(self.error))
            return
        self.result = d['result']
        self.parse_result(self.result)

    def parse_result(self, result):
        raise NotImplementedError('Method must be implemented in sub classes.')

    def get_error_code(self):
        return self.error;

    def get_result(self):
        return self.result

    def has_error(self):
        return self.error != 0
