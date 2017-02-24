from collections import OrderedDict

from flask import Flask
from werkzeug.utils import import_string, find_modules
from werkzeug.wsgi import DispatcherMiddleware
import redis

from views.api import json_api
from ext import Ext


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    app.config.from_object('config')

    Ext.cache = redis.StrictRedis()

    register_blueprints('views', app)

    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, OrderedDict((
        ('/api', json_api),
    )))

    return app


def register_blueprints(root, app):
    for name in find_modules(root, recursive=True):
        mod = import_string(name)

        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)


if __name__ == '__main__':
    app = create_app()

    app.run(host='0.0.0.0', port=8000)
