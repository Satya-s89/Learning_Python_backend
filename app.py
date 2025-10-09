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

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if username and password:
        return {"message": f"Hello, {username}"}
    else:
        return {"message": "Missing username or password"}
    
@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    
    if not username or not email or not password:
        return {"error": "All fields are required"}
    print(f"New signup: {username}, {email}")

    return {
        "message": f"Signup successful for {username}",
        "user": {
            "username": username,
            "email": email
        }
    }, 201

if __name__ == '__main__':
    app.run(debug=True)