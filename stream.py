from picamera2 import Picamera2
from flask import Flask, Response
import cv2

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

app.run(host='0.0.0.0', port=8080, threaded=True)
