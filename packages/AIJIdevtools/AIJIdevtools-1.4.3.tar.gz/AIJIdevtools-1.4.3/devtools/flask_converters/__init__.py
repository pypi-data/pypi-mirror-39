from werkzeug.routing import BaseConverter


class ListConverter(BaseConverter):
    def to_python(self, value):
        return value.split(',')

    def to_url(self, values):
        return ','.join(super().to_url(value)
                        for value in values)


class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]


class Converters:

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.url_map.converters['regex'] = RegexConverter
        app.url_map.converters['list'] = ListConverter
