import json
from flask import Flask
from flask_cors import CORS, cross_origin
from appfly.app.routes import ping

BASE_URL = '/api/'
cors_default = {
        "api/ping": {"origins": "*"}
}

app = None
# app.add_url_rule(BASE_URL + "ping", "PING", ping.route, methods=["GET"])

def factory(fn, name, cors=None):
    global app
    app = Flask(name)
    CORS(app, resources={json.dumps(cors_default)})
    if cors:
        CORS(app, resources=json.dumps({**cors, **cors_default})) 

    app.add_url_rule(BASE_URL + "ping", "ping", ping.route, methods=["GET"])
    fn(app, BASE_URL)
    
print('API is running...')
