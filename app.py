from flask import Flask, request
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route('/')

def home():
    return f"Hello, This is my python Backend. Secret Key: {app.config['SECRET_KEY']}"


@app.route('/api/greet/<username>')
def greet_user(username):
    return {"message": f"Hello, {username}! Welcome to my python backend"}

@app.route("/api/echo", methods=["POST"])
def echo():
    data = request.get_json()
    return {"You_sent": data}


if __name__ == '__main__':
    app.run(debug=True)