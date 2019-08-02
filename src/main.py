from flask import Flask
import pyrebase
from src import firebase

app = Flask(__name__)

config = firebase.get_credentials()
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


@app.route('/')
def index():
    return "Hello world!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)