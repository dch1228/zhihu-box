import json

from werkzeug.wrappers import Response


class ApiResult(object):
    def __init__(self, value, code):
        self.value = value
        self.code = code

    def to_resp(self):
        return Response(json.dumps(self.value),
                        status=self.code,
                        mimetype='application/json')


def success(res, code=200):
    res = res or {}

    return ApiResult(res, code)


def failure(msg, code):
    dct = {
        'code': code,
        'msg': msg
    }

    return ApiResult(dct, code)


def bad_request(msg):
    return failure(msg, 400)
