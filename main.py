from flask import Flask, Response, render_template, request
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
    global user
    try:
        if user:
            return Response(gen(VideoCamera()),
                            mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        return 404


@app.route('/', methods=['GET', 'POST'])
def index():
    unsuccessful = 'Please check your credentials'
    if request.method == 'POST':
        email = request.form['name']
        password = request.form['pass']
        try:
            global user
            user = auth.sign_in_with_email_and_password(email, password)
            if user:
                return render_template('index.html')
            else:
                return render_template('login.html', us=unsuccessful)
        except:
            return render_template('login.html', us=unsuccessful)

    return render_template('login.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2000, debug=True)
