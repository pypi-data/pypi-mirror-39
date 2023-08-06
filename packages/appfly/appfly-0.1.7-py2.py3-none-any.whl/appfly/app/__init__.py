import json
from flask import Flask
from flask_cors import CORS, cross_origin
from appfly.app.routes import ping

cors_default = {
        "api/ping": {"origins": "*"}
}

app = None

def add_url(url, route, method):
    global app
    len_urls = len(list(app.url_map.iter_rules()))
    app.add_url_rule("/api"+url, "url_{}".format(len_urls), route, methods=[method])

def factory(fn, name, cors=None):
    global app
    app = Flask(name, root_path='/api')
    CORS(app, resources={json.dumps(cors_default)})
    if cors:
        CORS(app, resources=json.dumps({**cors, **cors_default})) 

    add_url("/ping", ping.route, "GET")    
    fn(app)
    
print('API is running...')
