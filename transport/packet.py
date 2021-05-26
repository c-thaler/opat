import binascii


class Packet:

    def __init__(self, data):
        self.body = b''
        self.id = b''
        self.len = -1
        self.crc32 = bytearray(b'')
        if isinstance(data, str):
            self.generate_packet(data)
        elif isinstance(data, bytes):
            self.parse_packet(data)

    def generate_packet(self, message: str):
        self.body = message.encode()
        self.id = b'\x01\x01\x05\x00'
        self.len = len(self.body) + 2  # add 2 padding bytes
        self.crc32 = bytearray([0x5A, 0x6B, 0x7C, 0x8D])

    def parse_packet(self, data: bytes):
        self.body = bytes.join(b'', [bytes([b]) for b in data[18:]])
        self.id = bytes.join(b'', [bytes([b]) for b in data[:4]])
        self.len = int.from_bytes(data[5:6], 'big')
        self.crc32 = data[12:16]

    def update_crc32(self, data):
        crc = binascii.crc32(data)
        data = data[:12] + crc.to_bytes(4, 'big') + data[16:]
        return data

    def get_data(self, seq: int):
        # header
        data = self.id
        data += self.len.to_bytes(2, 'big')
        data += b'\x00\x00'  # padding
        data += seq.to_bytes(4, 'big')
        data += self.crc32

        # body
        data += b'\x01\x03'  # padding
        data += bytearray(self.body)

        data = self.update_crc32(data)

        return data

    def get_body(self):
        return self.body
