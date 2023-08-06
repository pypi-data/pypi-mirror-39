import json
from flask import Flask
from flask_cors import CORS, cross_origin
from appfly.app.routes import ping

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

    app.add_url_rule("/ping", "ping", ping.route, methods=["GET"])
    fn(app)
    
print('API is running...')
