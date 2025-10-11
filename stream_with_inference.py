from picamera2 import Picamera2
from flask import Flask, Response
import cv2
import time
import os

# Minimal inference stream using OpenCV Haar cascade (runs on-device)
# This is not production-grade ML; it's a lightweight on-device detector suitable for Raspberry Pi.

# Ensure cascade file exists (download if necessary)
CASCADE_URL = 'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml'
CASCADE_PATH = 'haarcascade_frontalface_default.xml'

if not os.path.exists(CASCADE_PATH):
    try:
        import urllib.request
        print('Downloading Haar cascade...')
        urllib.request.urlretrieve(CASCADE_URL, CASCADE_PATH)
    except Exception as e:
        print('Failed to download cascade:', e)

# Initialize camera
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

# Load cascade
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

app = Flask(__name__)

def gen_inference_frames():
    while True:
        frame = picam2.capture_array()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw overlays for detections
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, 'Face', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

@app.route('/video_infer')
def video_infer():
    return Response(gen_inference_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('INFER_PORT', '8081')), threaded=True)
