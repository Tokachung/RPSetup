from flask import Flask, Response, request
from functools import wraps
from picamera2 import Picamera2
import cv2
import os
from flask_cors import CORS

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def gen_frames():
    while True:
        try:
            frame = picam2.capture_array()
            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
        except Exception as e:
            # Log error and break the stream
            print(f"Error capturing frame: {e}")
            break

def check_auth(username, password):
    # Use environment variables for credentials
    valid_user = os.environ.get('STREAM_USER', 'user')
    valid_pass = os.environ.get('STREAM_PASS', 'pass')
    return username == valid_user and password == valid_pass

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

if __name__ == "__main__":
    host = os.environ.get('STREAM_HOST', '0.0.0.0')
    port = int(os.environ.get('STREAM_PORT', '8080'))
    app.run(host=host, port=port, threaded=True)