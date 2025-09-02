from flask import Flask

app = Flask(__name__)


@app.route("/") 
def welcome_user():
    return "Hello, user!"