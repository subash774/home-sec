from flask import Flask, render_template, Response

app = Flask(__name__)

# TODO: Add firebase for auth, used for streaming

@app.route('/')
def index():
    return "Hello world!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)