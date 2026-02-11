import os
import json
import numpy as np
from flask import Blueprint, request, jsonify, make_response
from backend.main import db
from backend.main import app
from backend.app.models import *
# from rs-engine import FeatureFaking as ff
import random
import operator
import pandas as pd

recommendations_bp = Blueprint(
    'recommendations', __name__, url_prefix="/recommendations")


@recommendations_bp.route("/frequently_bought_together", methods=['GET'])
def frequently_bought_together():
    product_id = request.args['product_id']
    interactions = InteractionModel.query.filter_by(
        product_id=product_id).all()
    products_bought = {}
    # Loop through all sessions and add items bought together with the item_id received
    for i in interactions:
        products_bought_same_session = InteractionModel.query.filter_by(
            session_id=i.session_id).all()
        for p in products_bought_same_session:
            p_id = p.product_id
            if p_id in products_bought:
                products_bought[p_id] += 1
            else:
                products_bought[p_id] = 0

    suggestions = dict(sorted(products_bought.items(),
                       key=operator.itemgetter(1), reverse=True))
    num_suggestions = min(2, len(suggestions) - 1)
    output = ""
    for key in suggestions:
        if num_suggestions <= 0:
            break
        if str(key) == str(product_id):
            continue
        else:
            num_suggestions -= 1
        output += str(key) + " "

    return output


@recommendations_bp.route("/similar_products", methods=['GET'])
def similar_products():
    product_id = request.args['product_id']
    num_recommend = request.args['n'] if 'n' in request.args else 10

    product_embeddings = pd.read_csv(os.path.join(
        app.root_path, 'models', 'product_embedding.csv'), header=None)

    idx = product_embeddings.iloc[:, 0].astype(
        int).astype(str).to_list().index(product_id)

    current_product_embedding = np.expand_dims(
        product_embeddings.iloc[idx, 1:].to_numpy(), axis=0)

    other_products = product_embeddings.drop(idx)

    other_products_ids = other_products.iloc[:, 0].astype(
        int).astype(str).to_numpy()

    op_emb = other_products.iloc[:, 1:].to_numpy()

    dot_prod = np.dot(current_product_embedding, op_emb.T)
    norm_p1 = np.linalg.norm(current_product_embedding, axis=1)
    norm_p2 = np.linalg.norm(op_emb, axis=1)
    cosine_sim = dot_prod / np.outer(norm_p1, norm_p2)

    rec = list(other_products_ids[np.argsort(-1 *
                                             cosine_sim, axis=-1)[0]][:num_recommend].astype(int))

    products = [(p.serialize, rec.index(p.id))
                for p in ProductModel.query.all() if p.id in rec]
    products = [p for (p, _) in sorted(products, key=lambda x: x[1])]

    return jsonify({
        "result": products,
    })


@recommendations_bp.route("/others_also_bought", methods=['GET'])
def others_also_bought():
    user_id = request.args['user_id']
    num_recommend = request.args['n'] if 'n' in request.args else 10

    user_embeddings = pd.read_csv(os.path.join(
        app.root_path, 'models', 'user_embedding.csv'), header=None)
    product_embeddings = pd.read_csv(os.path.join(
        app.root_path, 'models', 'product_embedding.csv'), header=None)

    print(user_embeddings.iloc[:, 0])
    idx = user_embeddings.iloc[:, 0].astype(
        int).astype(str).to_list().index(user_id)

    current_user_embedding = np.expand_dims(
        user_embeddings.iloc[idx, 1:].to_numpy(), axis=0)

    products_ids = product_embeddings.iloc[:, 0].astype(
        int).astype(str).to_numpy()

    prod_emb = product_embeddings.iloc[:, 1:].to_numpy()

    dot_prod = np.dot(current_user_embedding, prod_emb.T)
    norm_user = np.linalg.norm(product_embeddings, axis=1)
    norm_product = np.linalg.norm(prod_emb, axis=1)
    cosine_sim = dot_prod / np.outer(norm_user, norm_product)

    rec = list(products_ids[np.argsort(-1 *
                                       cosine_sim, axis=-1)[0]][:num_recommend].astype(int))

    products = [(p.serialize, rec.index(p.id))
                for p in ProductModel.query.all() if p.id in rec]
    products = [p for (p, _) in sorted(products, key=lambda x: x[1])]

    return jsonify({
        "result": products,
    })
