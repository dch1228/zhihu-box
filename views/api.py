from flask import Flask

from utils import ApiResult, failure
from exceptions import ApiException


class ApiFlask(Flask):
    def make_response(self, rv):
        if isinstance(rv, ApiResult):
            return rv.to_resp()

        Flask.make_response(self, rv)

json_api = ApiFlask(__name__)


@json_api.errorhandler(ApiException)
def handler_api_error(error):
    return error.to_resp()


@json_api.errorhandler(403)
@json_api.errorhandler(404)
@json_api.errorhandler(500)
def handler_error(error):
    if hasattr(error, 'name'):
        msg = error.name
        code = error.code
    else:
        msg = error.message
        code = 500

    return failure(msg, code)
