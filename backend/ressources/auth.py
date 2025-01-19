from flask import Blueprint, request, jsonify, current_app
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps

bcrypt = Bcrypt()
auth = Blueprint("auth", __name__)

# Registration route for user
@auth.route("/register", methods=["POST"])
def register():
    """
    Register a new user.
    """
    data = request.json
    if not data or not all(key in data for key in ("username", "password", "role")):
        return jsonify({"message": "Missing required fields"}), 400

    username = data["username"]
    password = data["password"]
    role = data["role"]

    if role not in ["admin", "student"]:
        return jsonify({"message": "Invalid role"}), 400

    try:
        # Check if the user already exists
        if current_app.db["users"].find_one({"username": username}):
            return jsonify({"message": "User already exists"}), 409

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        # Insert the user into the database
        current_app.db["users"].insert_one({"username": username, "password": hashed_password, "role": role})

        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 500


# Login route for user
@auth.route("/login", methods=["POST"])
def login():
    """
    Login a user and return a JWT token.
    """
    data = request.json
    if not data or not all(key in data for key in ("username", "password")):
        return jsonify({"message": "Missing required fields"}), 400

    username = data["username"]
    password = data["password"]

    try:
        # Find the user in the database
        user = current_app.db["users"].find_one({"username": username})
        if not user:
            return jsonify({"message": "Invalid username or password"}), 401

        # Check the password
        if not bcrypt.check_password_hash(user["password"], password):
            return jsonify({"message": "Invalid username or password"}), 401

        # Generate a JWT token
        payload = {
            "username": username,
            "role": user["role"],
            "exp": datetime.now(timezone.utc) + timedelta(hours=1)
        }
        token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

        return jsonify({"token": token}), 200
    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 500


# Decorator to protect routes based on roles
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token is missing"}), 403

        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            current_app.user = data  # Store user info in app context
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 403
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 403

        return f(*args, **kwargs)
    return decorated_function
