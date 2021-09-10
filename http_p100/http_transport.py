import requests
import uuid
import hashlib
import json
from base64 import b64decode
from Crypto.Cipher import PKCS1_v1_5
from . import tp_link_cipher
from Crypto.PublicKey import RSA
from .http_request import HttpRequest
from .req_handshake import RequestHandshake
from .req_login import RequestLogin

ERROR_CODES = {
    '0':     "Success",
    '-1010': "Invalid Public Key Length",
    '-1012': "Invalid terminalUUID",
    '-1501': "Invalid Request or Credentials",
    '1002':  "Incorrect Request",
    '-1003': "JSON formatting error"
}


class HttpTransport:

    def __init__(self, ip_address: str, email: str, password: str):
        self.ipAddress = ip_address
        self.terminalUUID = str(uuid.uuid4())

        self.email = email
        self.password = password

        self.errorCodes = ERROR_CODES

        self.encodedPassword = None
        self.encodedEmail = None
        self.keys = None
        self.publicKey = None
        self.privateKey = None
        self.tpLinkCipher = None
        self.cookie = None
        self.token = None

        self.encryptCredentials(email, password)
        self.createKeyPair()

        self.handshake()
        self.login()

        print(self.token)

    def encryptCredentials(self, email, password):
        # Password Encoding
        self.encodedPassword = tp_link_cipher.TpLinkCipher.mime_encoder(password.encode("utf-8"))

        # Email Encoding
        self.encodedEmail = self.sha_digest_username(email)
        self.encodedEmail = tp_link_cipher.TpLinkCipher.mime_encoder(self.encodedEmail.encode("utf-8"))

    def createKeyPair(self):
        self.keys = RSA.generate(1024)
        self.privateKey = self.keys.exportKey('PEM')
        self.publicKey = self.keys.publickey().exportKey('PEM')

    def decode_handshake_key(self, key):
        decode: bytes = b64decode(key.encode("UTF-8"))
        decode2: bytes = self.privateKey

        cipher = PKCS1_v1_5.new(RSA.importKey(decode2))
        do_final = cipher.decrypt(decode, None)
        if do_final is None:
            raise ValueError("Decryption failed!")

        b_arr: bytearray = bytearray()
        b_arr2: bytearray = bytearray()

        for i in range(0, 16):
            b_arr.insert(i, do_final[i])
        for i in range(0, 16):
            b_arr2.insert(i, do_final[i + 16])

        return tp_link_cipher.TpLinkCipher(b_arr, b_arr2)

    def sha_digest_username(self, data):
        b_arr = data.encode('UTF-8')
        digest = hashlib.sha1(b_arr).digest()

        sb = ''
        for i in range(0, len(digest)):
            b = digest[i]
            hex_string = hex(b & 255).replace('0x', '')
            if len(hex_string) == 1:
                sb += '0'
                sb += hex_string
            else:
                sb += hex_string

        return sb

    def handshake(self):
        req = RequestHandshake(self.publicKey)

        # Do not use request() since we need the header for cookie and we
        # don't want to send an encrypted message.
        url = f'http://{self.ipAddress}/app'
        r = requests.post(url, json=req.get_payload(), verify=False)

        presp = req.parse_response(r.content)
        encrypted_key = presp.get_key()
        self.tpLinkCipher = self.decode_handshake_key(encrypted_key)

        try:
            self.cookie = r.headers["Set-Cookie"][:-13]
        except:
            error_code = r.json()["error_code"]
            error_message = self.errorCodes[str(error_code)]
            raise Exception(f"Error Code: {error_code}, {error_message}")

    def login(self):
        req = RequestLogin(self.encodedEmail, self.encodedPassword)
        resp = self.request(req)
        self.token = resp.get_token()

    def request(self, request: HttpRequest):
        url = f'http://{self.ipAddress}/app'

        if self.token:
            url += f'?token={self.token}'

        enc_payload = self.tpLinkCipher.encrypt(json.dumps(request.get_payload()))
        secure_pass = {
            "method": "securePassthrough",
            "params": {
                "request": enc_payload
            }
        }

        headers = {
            'Cookie': self.cookie
        }

        resp = requests.post(url, json=secure_pass, headers=headers, verify=False)

        try:
            resp_payload = resp.json()["result"]["response"]
        except:
            error_code = resp.json()["error_code"]
            error_message = self.errorCodes[str(error_code)]
            raise Exception(f"Error Code: {error_code}, {error_message}")

        dec_payload = self.tpLinkCipher.decrypt(resp_payload)

        dec_payload_dict = json.loads(dec_payload)
        if dec_payload_dict['error_code'] != 0:
            error_code = dec_payload_dict["error_code"]
            error_message = self.errorCodes[str(error_code)]
            raise Exception(f"Error Code: {error_code}, {error_message}")

        return request.parse_response(dec_payload)
