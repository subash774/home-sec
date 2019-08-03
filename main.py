from flask import Flask, Response, render_template
import pyrebase
import firebase
from camera import VideoCamera

app = Flask(__name__, template_folder="templates")

config = firebase.get_credentials()
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


def gen(feed):
    while True:
        frame = feed.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        feed.record()


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return render_template('index.html')
    # return "Hello world"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2000, debug=True)
