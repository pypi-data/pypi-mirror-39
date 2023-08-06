import json
from flask import request, current_app, jsonify
from werkzeug.exceptions import default_exceptions
from devtools.web import merge_fields


def default_http_exception_handler(error):
    code = getattr(error, 'code', 500)
    if str(code).startswith('5'):
        description = json.dumps(merge_fields(request), indent=4)
        current_app.logger.error(description, exc_info=True)
    return jsonify(
        name=getattr(error, 'name', ''),
        description=getattr(error, 'description', ''),
        path=request.path), code


def default_common_exception_handler(error):
    current_app.logger.error(
        json.dumps(merge_fields(request), indent=4), exc_info=True)
    return jsonify(
        message='Something wrong...',
        error=str(error)), 500


class Errors(object):

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        for code in default_exceptions:
            app.errorhandler(code)(default_http_exception_handler)
        app.errorhandler(Exception)(default_common_exception_handler)
