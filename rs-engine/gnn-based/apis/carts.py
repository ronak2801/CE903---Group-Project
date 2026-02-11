from flask import Blueprint, jsonify, request
from backend.main import db
from backend.app.models import * 

carts_bp = Blueprint('carts', __name__, url_prefix="/carts")


# Add item to the cart
@carts_bp.route('/add', methods=['POST'])
def add_to_cart():

    user_id = request.form["user_id"]
    product_id = request.form["product_id"]
    quantity = request.form["quantity"]
    
    cart_item = CartModel.query.filter_by(user_id=user_id, product_id=product_id).first()

    if cart_item is None:
        # If the product is not in the cart, create a new cart item
        cart_item = CartModel(user_id=user_id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    else:
        # If the product is already in the cart, update the quantity of the existing cart item
        cart_item.quantity = int(cart_item.quantity) + int(quantity)
    
    db.session.commit()
    
    return jsonify({'message': 'Item added to cart'})

@carts_bp.route("/<int:cart_id>", methods=['PATCH'])
def update_cart(cart_id):

    user_id = request.form["user_id"]
    product_id = request.form["product_id"]
    quantity = request.form["quantity"]

    cart = CartModel.query.filter_by(id=cart_id).first()

    if cart:
        db.session.delete(cart)
        db.session.commit()

        cart = CartModel(id=cart_id, user_id=user_id, product_id=product_id, quantity=quantity)
        
        db.session.add(cart)
        db.session.commit()
    
    return "Done"


# Remove item from user cart
@carts_bp.route('/delete', methods=['DELETE'])
def remove_from_cart():

    user_id = request.form["user_id"]
    product_id = request.form["product_id"]
    
    cart_item = CartModel.query.filter_by(user_id=user_id, product_id=product_id).first()
    db.session.delete(cart_item)
    db.session.commit()
    
    return jsonify({'message': 'Item removed from cart'})

# List all items in the user cart
@carts_bp.route('/items', methods=['GET'])
def get_cart():

    user_id = request.form["user_id"]
    if not user_id:
        return jsonify({'message': 'User ID is missing'}), 400
    
    cart_items = db.session.query(ProductModel.id, ProductModel.name, ProductModel.price, ProductModel.meta_deta, CartModel.quantity).join(CartModel, CartModel.product_id == ProductModel.id).filter(CartModel.user_id == user_id).all()

    if not cart_items:
        return jsonify({'message': 'No items found in cart'}), 404

    result = []
    for item in cart_items:
        result.append({
            'id': item.id,
            'name': item.name,
            'price': item.price,
            'quantity': item.quantity,
            'meta_deta': item.meta_deta
        })

    return jsonify(result)

# Delete all items in the user Cart
@carts_bp.route('/delete_all', methods=['DELETE'])
def remove_all_from_cart():

    user_id = request.form["user_id"]
    
    cart_items = CartModel.query.filter_by(user_id=user_id).all()
    for cart_item in cart_items:
        db.session.delete(cart_item)
    db.session.commit()
    
    return jsonify({'message': 'All items removed from cart'})
