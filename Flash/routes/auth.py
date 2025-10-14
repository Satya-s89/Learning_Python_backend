from flask import Blueprint, request
from models.user import User, db
import jwt
from datetime import datetime, timedelta
from config import Config

auth_bp = Blueprint('auth', __name__)

def generate_token(user_id):
    """Generate JWT token for user"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

def verify_token(token):
    """Verify JWT token and return user_id"""
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@auth_bp.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return {"error": "Missing username or password"}, 400
    
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        token = generate_token(user.id)
        return {
            "message": f"Login successful for {username}",
            "token": token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }
    
    return {"error": "Invalid username or password"}, 401

@auth_bp.route("/api/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    
    if not username or not email or not password:
        return {"error": "All fields are required"}, 400
    
    if User.query.filter_by(username=username).first():
        return {"error": "Username already exists"}, 409
    if User.query.filter_by(email=email).first():
        return {"error": "Email already exists"}, 409
    
    new_user = User(username=username, email=email) 
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    
    token = generate_token(new_user.id)
    
    return {
        "message": f"Signup successful for {username}",
        "token": token,
        "user": {
            "id": new_user.id,
            "username": username, 
            "email": email
        }
    }, 201

@auth_bp.route("/api/profile", methods=["GET"])
def profile():
    """Protected route - requires token"""
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return {"error": "No token provided"}, 401
    
    try:
        token = auth_header.split(' ')[1]  # Bearer <token>
    except IndexError:
        return {"error": "Invalid token format"}, 401
    
    user_id = verify_token(token)
    if not user_id:
        return {"error": "Invalid or expired token"}, 401
    
    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}, 404
    
    return {
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }

@auth_bp.route("/api/verify-token", methods=["POST"])
def verify_token_route():
    """Verify if token is valid"""
    data = request.get_json()
    token = data.get("token")
    
    if not token:
        return {"error": "No token provided"}, 400
    
    user_id = verify_token(token)
    if user_id:
        return {"valid": True, "user_id": user_id}
    else:
        return {"valid": False}, 401
