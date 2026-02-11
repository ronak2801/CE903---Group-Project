from flask import Blueprint, jsonify, request
from backend.main import db
from backend.app.models import * 

payments_bp = Blueprint('payments', __name__)

@payments_bp.route("/checkout", methods=['POST'])

def checkout():
    user_id = request.form["user_id"]

    # Check if user_id is missing
    if not user_id:
        return jsonify({'message': 'User ID is missing'}), 400

    # Retrieve all items in the user's cart
    cart_items = db.session.query(CartModel).filter_by(user_id=user_id).all()
    if not cart_items:
        return jsonify({'message': 'No items found in cart'}), 404

    # Update the product quantities in the database
    for item in cart_items:
        product = db.session.query(ProductModel).filter_by(id=item.product_id).first()
        if not product:
            return jsonify({'message': 'Product not found'}), 404
        # if product.quantity < item.quantity:
        #     return jsonify({'message': 'Insufficient stock for item "{}"'.format(product.name)}), 400
        # product.quantity -= item.quantity
        # db.session.add(product)

    # Remove items from cart after purchase
    for item in cart_items:
        db.session.delete(item)

    db.session.commit()

    return jsonify({'message': 'Checkout successful'})
