from flask import Flask, Response, render_template, request, session
import pyrebase
import firebase
from camera import VideoCamera
import os
from threading import Thread
import datetime
import time
import sys

app = Flask(__name__, template_folder="templates")
app.secret_key = os.urandom(24)

config = firebase.get_credentials()
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
video = VideoCamera()
threads = []


def gen(feed):
    while True:
        try:
            frame = feed.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        except Exception as e:
            print(str(e))


@app.route('/video_feed')
def video_feed():
    try:
        print(session['usr'])
        return Response(gen(video),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    except KeyError:
        print("Wrong id")
        return render_template('login.html', us="Unauthorised")


@app.route('/', methods=['GET', 'POST'])
def index():
    unsuccessful = 'Please check your credentials'
    if request.method == 'POST':
        email = request.form['name']
        password = request.form['pass']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['usr'] = user.get('idToken')
            return render_template('index.html')
        except Exception as e:
            print(str(e))
            return render_template('login.html', us=unsuccessful)

    return render_template('login.html')


def test():
    global video
    t_end = time.time() + 30
    while time.time() < t_end:
        video.record()
    video.save()


def stream():
    global video
    t_end = time.time() + 30
    while time.time() < t_end:
        app.run(host='0.0.0.0', port=2000, debug=True, use_reloader=False)


def shutdown_server():
    # func = request.environ.get('werkzeug.server.shutdown')
    # if func is None:
    #     raise RuntimeError('Not running with the Werkzeug Server')
    # func()
    sys.exit(0)


def start():
    t1 = Thread(target=stream)
    t1.setDaemon(True)
    t2 = Thread(target=test)
    t1.start()
    t2.start()
    # shutdown_server()

start()
