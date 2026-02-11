from flask import jsonify
from backend.main import db


class ProductModel(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(), nullable=True)
    meta_deta = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.TIMESTAMP(timezone=False), default=db.func.now())
    updated_at = db.Column(db.TIMESTAMP(
        timezone=False), default=db.func.now(), onupdate=db.func.current_timestamp())

    interactions = db.relationship(
        "InteractionModel", back_populates="products")
    carts = db.relationship("CartModel", back_populates="products")

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'image': self.image,
            'meta_data': self.meta_deta
        }
