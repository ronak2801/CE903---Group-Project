from backend.main import db


class CartModel(db.Model):
    __tablename__ = 'carts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        "products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.TIMESTAMP(timezone=False), default=db.func.now())
    updated_at = db.Column(db.TIMESTAMP(
        timezone=False), default=db.func.now(), onupdate=db.func.current_timestamp())

    users = db.relationship("UserModel", back_populates="carts")
    products = db.relationship("ProductModel", back_populates="carts")
