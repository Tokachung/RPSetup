from picamera2 import Picamera2, Preview
from flask import Flask, Response
import cv2
import time

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

app = Flask(__name__)

def gen_frames():
    while True:
        frame = picam2.capture_array()
        ret, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

@app.route('/video')
def video():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Create a new route that returns a single snapshot (in-memory JPEG)
@app.route('/snapshot')
def snapshot():
    # Capture a single frame as a numpy array
    frame = picam2.capture_array()

    # Encode to JPEG in memory
    ret, jpeg = cv2.imencode('.jpg', frame)
    if not ret:
        return Response('Failed to capture image', status=500)

    # Return the JPEG bytes directly without saving to disk
    return Response(jpeg.tobytes(), mimetype='image/jpeg')

app.run(host='0.0.0.0', port=8080, threaded=True)

