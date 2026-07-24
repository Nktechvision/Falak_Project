from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from flask import Blueprint, jsonify
from flask import request
from models import db, User
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Blueprint("api", __name__)


@api.route("/api/hello")
def hello():

    return jsonify({
        "message": "Hello World",
        "status": "success"
    })

@api.route("/api/users")
def get_users():

    users = User.query.all()

    data = []

    for user in users:

        data.append({
            "id": user.id,
            "username": user.username,
            "created_at": user.created_at,
            "photo": user.photo
        })

    return jsonify(data)
@api.route("/api/users", methods=["POST"])
def create_user():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")
    if not username:
      return jsonify({
        "error": "Username is required"
    }), 400

    if not password:
      return jsonify({
        "error": "Password is required"
    }), 400

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
      return jsonify({
        "error": "Username already exists"
    }), 409

    hashed_password = generate_password_hash(password)

    user = User(
        username=username,
        password=hashed_password,
        created_at="01-07-2026",
        photo=None
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User Created Successfully"
    }), 201
@api.route("/api/login", methods=["POST"])
def login_user():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username:
        return jsonify({
            "error": "Username is required"
        }), 400

    if not password:
        return jsonify({
            "error": "Password is required"
        }), 400

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({
            "error": "Invalid Username or Password"
        }), 401

    if not check_password_hash(user.password, password):
        return jsonify({
            "error": "Invalid Username or Password"
        }), 401
    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "message": "Login Successful",
        "access_token": access_token
    }), 200

@api.route("/api/profile")
@jwt_required()
def api_profile():

    user_id = int(get_jwt_identity())

    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "created_at": user.created_at,
        "photo": user.photo
    }), 200
