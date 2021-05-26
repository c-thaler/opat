import base64
from .response import Response
from .request import Request


class RequestWifiScanInfo(Request):

    data = {
        "method": "get_wireless_scan_info",
        "params": {
            "start_index": 0
        },
        "requestTimeMils": 1619885487256,
        "terminalUUID": "8C-B8-4A-A4-D1-FA"
    }

    def __init__(self, index=0):
        super().__init__('get_wireless_scan_info', {'start_index': index})

    def parse_response(self, resp):
        return ResponseWifiScanInfo(resp)


# Note that the response is limited to 10 AP entries. Use another request
# with an increased 'index' to get the remaining ones.
# Total number of APs discovered by the device is given in 'sum'
class ResponseWifiScanInfo(Response):

    def __init__(self, data):
        self.ap_list = {}
        self.count = 0
        self.total_count = 0
        self.index = 0
        super().__init__(data)

    def parse_result(self, result):
        self.ap_list = result['ap_list']

        for i in range(len(self.ap_list)):
            self.ap_list[i]['ssid'] = base64.b64decode(self.ap_list[i]['ssid'].encode()).decode()

        self.total_count = result['sum']
        self.count = len(self.ap_list)
        self.index = result['start_index']

    def get_ap_list(self):
        return self.ap_list

    def is_complete(self):
        return self.total_count <= self.count + self.index

    def get_next_index(self):
        return self.index + self.count
