# -*- coding: utf-8 -*-

"""Top-level package for appfly."""

__author__ = """Italo José G. de Oliveira"""
__email__ = 'italo.i@live.com'
__version__ = '0.1.2'

import json
from flask import Flask
from flask_cors import CORS, cross_origin

BASE_URL = '/api/'
cors_default = {
        "api/ping": {"origins": "*"}
}

app = None

def factory(fn, name, cors=None):
    global app
    app = Flask(name)
    CORS(app, resources={json.dumps(cors_default)})
    if cors:
        CORS(app, resources=json.dumps({**cors, **cors_default})) 

    from appfly.routes import ping
    app.add_url_rule(BASE_URL + "ping", "PING", ping.route, methods=["GET"])

    fn(app)
    return app
print('API is running...')
