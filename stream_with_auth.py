from flask import Flask, Response, request
from functools import wraps

def check_auth(username, password):
    return username == 'user' and password == 'pass'

def authenticate():
    return Response('Could not verify your access level.', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/video')
@requires_auth
def video():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')