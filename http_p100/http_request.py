import time


class HttpRequest:

    def __init__(self, method: str, module: str, params=None):
        self.method = method
        self.module = module
        self.params = params

    def gen_msg(self):
        msg = {'method': self.method}
        msg[self.module] = {}
        if self.params is not None:
            msg[self.module] = self.params
        print(msg)
        return msg

    def get_payload(self):
        return self.gen_msg()

    def parse_response(self, resp):
        raise NotImplementedError('Must be implemented in sub class.')
