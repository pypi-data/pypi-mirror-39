import inspect
import sys

from apispec import APISpec
from apispec.ext.bottle import BottlePlugin

IGNORED_TYPES = ['Schema']


def disable_swagger(callback):
    callback.enable_swagger = False
    return callback


class APISpecPlugin(object):
    name = 'apispec'
    api = 2

    def __init__(self, path='/schema.json', scan_package=None, *args, **kwargs):
        kwargs['plugins'] = kwargs.get('plugins', ()) + (BottlePlugin(),)
        self.apispec = APISpec(*args, **kwargs)
        self.scan_package = scan_package
        self.path = path

    def setup(self, app):
        if not app.routes:
            raise Exception('No routes found. Please be sure to install APISpecPlugin after declaring *all* your routes!')

        if self.scan_package:
            self._scan_marshmallow_models(self.scan_package)

        for route in app.routes:
            if hasattr(route.callback, 'enable_swagger') and not route.callback.enable_swagger:
                continue
            self.apispec.add_path(view=route.callback)

        @app.get(self.path)
        def schema():
            return self.apispec.to_dict()

    def apply(self, callback, route):
        return callback

    def _scan_marshmallow_models(self, base_package):
        for name, obj in inspect.getmembers(sys.modules[base_package]):
            if inspect.ismodule(obj) and obj.__package__ == base_package:
                self._scan_marshmallow_models('%s.%s' % (base_package, name))
            elif name not in IGNORED_TYPES and inspect.isclass(obj) and 'marshmallow.schema' in str(obj.__class__.__bases__):
                self.apispec.definition(name, schema=obj)
