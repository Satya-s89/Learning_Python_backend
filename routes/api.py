from flask import Blueprint, request

api_bp = Blueprint('api', __name__)

@api_bp.route('/')
def home():
    return "Hello, This is my python Backend."

@api_bp.route('/api/greet/<username>')
def greet_user(username):
    return {"message": f"Hello, {username}! Welcome to my python backend"}

@api_bp.route("/api/echo", methods=["POST"])
def echo():
    data = request.get_json()
    return {"You_sent": data}
