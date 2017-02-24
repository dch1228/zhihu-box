from utils import failure


class ApiException(Exception):
    def __init__(self, msg, code=400):
        self.msg = msg
        self.code = code

    def to_resp(self):
        return failure(self.msg, self.code)
