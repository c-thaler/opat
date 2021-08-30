import base64
from .response import Response
from .request import Request

# {"method":"set_qs_info",
# "params":{
#   "account":{"password":"Xy9qUmRJNGo=","username":"YnVtbWJlcnVtbUBnbWFpbC5jb20="},
#   "time":{"latitude":535630,"longitude":100482,"region":"Europe/Ber@ÌÈlin","time_diff":60,"timestamp":1619885501},
#   "wireless":{"key_type":"wpa2_psk","password":"MzY3NzczNjU2MTQyNTc3OTU1NTg=","ssid":"Qk5E"}
# },
# "requestTimeMils":1619885501746,"terminalUUID":"8C-B8-4A-A4-D1-FA"}


class RequestSetQsInfo(Request):

    def __init__(self, wifi_ssid, wifi_key='', wifi_key_type='wpa2_psk',
                 web_user='edcrfv@edcujm.com', web_password='Passw0rd'):
        web_user = ''
        web_password = ''
        params = {
            'account': {
                'password': self.to_base64(web_password),
                'username': self.to_base64(web_user)
            },
            'time': {
                'latitude': 535630,
                'longitude': 100482,
                'region': 'Europe/Berlin',
                'time_diff': 60,
                'timestamp': 1619885501
            },
            'wireless': {
                'key_type': wifi_key_type,
                'password': self.to_base64(wifi_key),
                'ssid': self.to_base64(wifi_ssid)
            }
        }

        super().__init__('set_qs_info', params)

    def to_base64(self, s):
        return base64.b64encode(s.encode()).decode()

    def parse_response(self, resp):
        return ResponseSetQsInfo(resp)


class ResponseSetQsInfo(Response):

    def __init__(self, data):
        super().__init__(data)
        self.ap_list = {}

    def parse_result(self, result):
        pass

