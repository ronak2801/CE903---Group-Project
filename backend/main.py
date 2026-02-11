import os
import csv
import json
from tqdm import tqdm
import hashlib
import numpy as np
from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, downgrade

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")

db = SQLAlchemy()
migrate = Migrate()

from backend.app.models import *

db.init_app(app)
migrate.init_app(app, db)

from backend.apis.auth import auth_bp
from backend.apis.carts import carts_bp
from backend.apis.users import users_bp
from backend.apis.payment import payments_bp
from backend.apis.products import products_bp
from backend.apis.interactions import interactions_bp
from backend.apis.recommendations import recommendations_bp

# register api routes
app.register_blueprint(auth_bp)
app.register_blueprint(carts_bp)
app.register_blueprint(users_bp)
app.register_blueprint(payments_bp)
app.register_blueprint(products_bp)
app.register_blueprint(interactions_bp)
app.register_blueprint(recommendations_bp)


@app.cli.command('db_seed')
def db_seed():

    print("-- seeding products")
    with open('seed/products.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=",")
        for row in reader:
            meta_data = row.copy()
            del meta_data['product_id']
            del meta_data['product']
            del meta_data['image']

            meta_data = json.dumps(meta_data)
            meta_data = json.loads(meta_data)

            p = ProductModel(
                id=row['product_id'],
                name=row['product'],
                image=row['image'],
                price=np.random.uniform(0, 100),
                meta_deta=meta_data,
            )

            db.session.add(p)

    print("-- seeding users")
    with open('seed/users.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for row in reader:
            meta_deta = row.copy()
            del meta_deta['user_id']
            del meta_deta['email']

            meta_deta = json.dumps(meta_deta)
            meta_deta = json.loads(meta_deta)

            password = hashlib.sha256("super".encode()).hexdigest()
            su = UserModel(
                id=row['user_id'],
                email=row['email'],
                hash_pwd=password,
                meta_deta=meta_deta,
            )
            db.session.add(su)

    print("-- seeding interaction")
    with open('seed/interactions.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for i, row in tqdm(enumerate(reader)):
            su = InteractionModel(
                id=i,
                type="purchase",
                user_id=row['user_id'],
                product_id=row['product_id'],
                session_id=row['session_id'],
            )
            db.session.add(su)

    db.session.commit()
    print("-- database seeded")


@app.cli.command('db_drop')
def db_drop():
    downgrade(revision='base')
    print("Database Dropped!")


if __name__ == '__main__':
    app.run()
