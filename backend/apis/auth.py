from flask import Blueprint, request, jsonify
from backend.main import db
from backend.app.models import *
import hashlib


auth_bp = Blueprint('auth', __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=['POST'])
def login():

    username = request.form["username"]
    password = request.form["password"]
    password = hashlib.sha256(password.encode()).hexdigest()
    su = UserModel(email=username, hash_pwd=password)

    user = UserModel.query.filter_by(email=username).first()

    if user:
        out = (user.hash_pwd == password)
    else:
        return "Fail"
    if (out):
        return jsonify(user.id)
    else:
        return "Fail"


@auth_bp.route("/signup", methods=['POST'])
def signup():
    username = request.form["username"]
    password = request.form["password"]
    password = hashlib.sha256(
        password.encode() + username.encode()).hexdigest()

    user = UserModel.query.filter_by(email=username).first()

    if user:
        return "Fail"

    su = UserModel(email=username, hash_pwd=password)
    db.session.add(su)
    db.session.commit()
    return "True"
