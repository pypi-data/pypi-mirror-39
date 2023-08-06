import json
from traceback import format_exc
from functools import partial
from flask import request, current_app, jsonify
from werkzeug.exceptions import default_exceptions
from devtools.web import merge_fields


def http_exception_handler(error, debug):
    code = getattr(error, 'code', 500)
    if str(code).startswith('5'):
        description = json.dumps(merge_fields(request), indent=4)
        current_app.logger.error(description, exc_info=True)
        if debug:
            print(description)
            print(format_exc())
    return jsonify(
        name=getattr(error, 'name', ''),
        description=getattr(error, 'description', ''),
        path=request.path), code


def common_exception_handler(error, debug):
    req = json.dumps(merge_fields(request), indent=4)
    current_app.logger.error(req, exc_info=True)
    if debug:
        print(req)
        print(format_exc())
    return jsonify(
        message='Something wrong...',
        error=str(error)), 500


class Errors:

    def __init__(self, app=None, debug=False):
        self.debug = debug
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        for code in default_exceptions:
            app.errorhandler(code)(partial(http_exception_handler, debug=self.debug))
        app.errorhandler(Exception)(partial(common_exception_handler, debug=self.debug))
