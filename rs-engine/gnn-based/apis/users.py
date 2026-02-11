from flask import Blueprint, request
from backend.main import db
from backend.app.models import * 
import hashlib

users_bp = Blueprint('users', __name__, url_prefix="/users")

@users_bp.route("/create", methods=['POST'])
def create_user():
    
    username = request.form["username"]
    password = request.form["password"]
    password = hashlib.sha256(password.encode() + username.encode()).hexdigest()

    su = UserModel(email=username , hash_pwd=password)
    db.session.add(su)
    db.session.commit()

    return "<p> user created </p>"

@users_bp.route("/<int:user_id>", methods=['PATCH'])
def update_user(user_id):
    
    user = UserModel.query.filter_by(id = user_id).first()

    if user:
        db.session.delete(user)
        db.session.commit()

        email = request.form['username']
        password = request.form['password']
        meta = request.form['meta']
        password = hashlib.sha256(password.encode() + email.encode()).hexdigest()
        user = UserModel(id = user_id, email=email , hash_pwd=password, meta_deta = meta)
        
        db.session.add(user)
        db.session.commit()
    else:
        return "404 User Not Found"
    return "<p>update_user</p>"

@users_bp.route("/<int:user_id>", methods=['DELETE'])
def delete_user(user_id):
    user = UserModel.query.filter_by(id = user_id).first()

    if user:
        db.session.delete(user)
        db.session.commit()
        return "Deleted"

    return "404 User Not Found"

@users_bp.route("/<int:user_id>", methods=['GET'])
def show_user(user_id):
    user = UserModel.query.filter_by(id = user_id).first()
    if user:
        return user.email
    return "404 user missing"

@users_bp.route("/", methods=['GET'])
def list_users():
    #users = db.session.execute(db.select(UserModel).order_by(UserModel.email)).scalars()
    users = UserModel.query.all()
    output = ""

    for user in users:
        output += user.email
        output += " "

    return output
