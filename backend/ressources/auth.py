from flask import Blueprint, request, jsonify, current_app
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps

bcrypt = Bcrypt()
auth = Blueprint("auth", __name__)

LOGGED_OUT_TOKENS = set()

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

        # Insert the user into the users table
        user_id = current_app.db["users"].insert_one({
            "username": username,
            "password": hashed_password,
            "role": role
        }).inserted_id

        # Insert role-specific data (admin or student)
        if role == "admin":
            if not all(key in data for key in ("first_name", "last_name")):
                return jsonify({"message": "Missing required fields for admin"}), 400
            current_app.db["admins"].insert_one({
                "user_id": user_id,
                "first_name": data["first_name"],
                "last_name": data["last_name"]
            })
        elif role == "student":
            if not all(key in data for key in ("first_name", "last_name", "year_of_study", "university")):
                return jsonify({"message": "Missing required fields for student"}), 400
            current_app.db["students"].insert_one({
                "user_id": user_id,
                "first_name": data["first_name"],
                "last_name": data["last_name"],
                "year_of_study": data["year_of_study"],
                "university": data["university"]
            })

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
        # Find the user in the users table
        user = current_app.db["users"].find_one({"username": username})
        if not user:
            return jsonify({"message": "Invalid username or password"}), 401

        # Check the password
        if not bcrypt.check_password_hash(user["password"], password):
            return jsonify({"message": "Invalid username or password"}), 401

        # Prepare the payload for the JWT token
        payload = {
            "username": username,
            "role": user["role"],
            "exp": datetime.now(timezone.utc) + timedelta(hours=1)
        }
        token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

        return jsonify({"token": token}), 200
    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 500


# Decorator to enforce JWT-based authentication
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token is missing"}), 403

        if token in LOGGED_OUT_TOKENS:  # Check if the token has been logged out
            return jsonify({"message": "Token is invalid"}), 403

        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            current_app.user = data  # Store user information in app context
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 403
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 403

        return f(*args, **kwargs)
    return decorated_function


# Logout route
@auth.route("/logout", methods=["POST"])
@token_required
def logout():
    """
    Logout a user by invalidating the JWT token.
    """
    token = request.headers.get("Authorization")
    if token:
        LOGGED_OUT_TOKENS.add(token)
        return jsonify({"message": "Logged out successfully"}), 200
    return jsonify({"message": "Token is missing"}), 400
