from backend.main import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), unique=True, nullable=False)
    hash_pwd = db.Column(db.String(), nullable=False)
    meta_deta = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.TIMESTAMP(timezone=False), default=db.func.now())
    updated_at = db.Column(db.TIMESTAMP(
        timezone=False), default=db.func.now(), onupdate=db.func.current_timestamp())

    interactions = db.relationship("InteractionModel", back_populates="users")
    carts = db.relationship("CartModel", back_populates="users")
