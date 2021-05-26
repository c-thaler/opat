import json
from transport.packet import Packet


class Request:

    def __init__(self, method, params=None):
        self.method = method
        self.params = params

    def gen_msg(self):
        msg = {'method': self.method}
        if self.params is not None:
            msg['params'] = self.params
        msg['requestTimeMils'] = 1619885487256
        msg['terminalUUID'] = '8C-B8-4A-A4-D1-FA'
        return msg

    def get_json(self):
        return json.dumps(self.gen_msg())

    def get_packet(self):
        p = Packet(self.get_json())
        return p

    def parse_response(self, resp):
        raise NotImplementedError('Must be implemented in sub lass.')
