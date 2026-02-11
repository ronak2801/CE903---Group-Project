from sqlalchemy.dialects.postgresql import JSON

from backend.main import db


class InteractionModel(db.Model):
    __tablename__ = 'interactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        "products.id"), nullable=False)
    type = db.Column(db.String(), nullable=False)
    session_id = db.Column(db.String(), nullable=False)
    meta_deta = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.TIMESTAMP(timezone=False), default=db.func.now())
    updated_at = db.Column(db.TIMESTAMP(
        timezone=False), default=db.func.now(), onupdate=db.func.current_timestamp())

    users = db.relationship("UserModel", back_populates="interactions")
    products = db.relationship("ProductModel", back_populates="interactions")
