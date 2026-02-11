from flask import Blueprint, request, jsonify
from backend.app.models import *
from backend.main import db

products_bp = Blueprint('products', __name__, url_prefix="/products")


@products_bp.route("/create", methods=['POST'])
def create_product():

    name = request.form["name"]
    price = request.form["price"]
    image = request.form["image"]
    meta = request.form["meta_data"]

    model = ProductModel(name=name, price=price, image=image, meta_deta=meta)
    db.session.add(model)
    db.session.commit()

    return "Success"


@products_bp.route("/<int:product_id>", methods=['PATCH'])
def update_product(product_id):

    model = ProductModel.query.filter_by(id=product_id).first()

    name = request.form["name"]
    price = request.form["price"]
    image = request.form["image"]
    meta = request.form["meta_data"]

    other_model = ProductModel(
        id=product_id, name=name, price=price, image=image, meta_deta=meta)

    if model:

        db.session.delete(model)
        db.session.commit()
        db.session.add(other_model)
        db.session.commit()
        return "Success"

    return "Fail"


@products_bp.route("/<int:product_id>", methods=['DELETE'])
def delete_product(product_id):

    model = ProductModel.query.filter_by(id=product_id).first()
    if model:
        db.session.delete(model)
        db.session.commit()
        return "Success"

    return "Fail"


@products_bp.route("/<int:product_id>", methods=['GET'])
def show_product(product_id):

    model = ProductModel.query.filter_by(id=product_id).first()
    if model:
        return jsonify(model.serialize)

    return "Fail"


@products_bp.route("/", methods=['GET'])
def list_products():
    products = ProductModel.query.all()
    return jsonify({
        "result": [p.serialize for p in products]
    })
