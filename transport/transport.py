import time
from bluez import Characteristic
from transport.request import Request


class Transport:

    seq = 1

    def __init__(self, char_read: Characteristic, char_write: Characteristic):
        self.read = char_read
        self.write = char_write

        # clean read buffer
        for i in range(0, 15):
            char_read.read_value()

    def recv(self):
        resp = b''
        for i in range(200):
            resp += bytes(self.read.read_value())
            if len(resp) != 0:
                break
            time.sleep(0.1)

        if len(resp) == 0:
            raise TimeoutError('Timeout while waiting for response.')

        for i in range(1, 15):
            resp += bytes(self.read.read_value())
        return bytes.join(b'', [bytes([b]) for b in resp])

    def request(self, request: Request):
        self.write.write_value(request.get_packet().get_data(self.seq))
        self.seq = self.seq + 1

        resp = self.recv()
        return request.parse_response(resp)
