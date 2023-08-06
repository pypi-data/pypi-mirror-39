import json
from appfly import app

def factory(
    content, 
    status=200, 
    headers=None,
    mimetype='application/json', 
    content_type='application/json'):

    content = json.dumps(content)
    return app.response_class(
            response = content,
            status= status,
            headers = headers,
            direct_passthrough=False,
            mimetype='application/json',
            content_type='application/json'
        )