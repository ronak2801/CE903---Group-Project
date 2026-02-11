from flask import Blueprint, request
from backend.main import db
from backend.app.models import * 

interactions_bp = Blueprint('interactions', __name__, url_prefix="/interactions")

@interactions_bp.route("/create", methods=['POST'])
def create_interaction():
    
    product_id = request.form["product_id"]
    user_id = request.form["user_id"]
    type = request.form["type"]
    meta = request.form["meta_data"]
    session = request.form["session_id"]
    interaction = InteractionModel(user_id = user_id, product_id = product_id , type=type, meta_deta = meta, session_id = session)
    db.session.add(interaction)
    db.session.commit()

    return "<p>create_interaction</p>"

@interactions_bp.route("/<int:interaction_id>", methods=['PATCH'])
def update_interaction(interaction_id):
    interaction = InteractionModel.query.filter_by(id = interaction_id).first()

    if interaction:
        db.session.delete(interaction)
        db.session.commit()
        
        product_id = request.form["product_id"]
        user_id = request.form["user_id"]
        type = request.form["type"]
        meta = request.form["meta_data"]
        session = request.form["session_id"]
        interaction = InteractionModel(user_id = user_id, product_id = product_id , type=type, meta_deta = meta, session_id = session)
        db.session.add(interaction)
        db.session.commit()

    else:
        return "Interaction Not Found"
    
    return "<p>update_interaction</p>"

@interactions_bp.route("/<int:interaction_id>", methods=['DELETE'])
def delete_interaction(interaction_id):
    interaction = InteractionModel.query.filter_by(id = interaction_id).first()

    if interaction:
        db.session.delete(interaction)
        db.session.commit()
    else:
        return "Interaction Not Found"
     
    return "<p>delete_interaction</p>"

@interactions_bp.route("/<int:interaction_id>", methods=['GET'])
def show_interaction(interaction_id):
    interaction = InteractionModel.query.filter_by(id = interaction_id).first()
    if interaction:
        return interaction.meta_deta
    else:
        return "User Not Found"

@interactions_bp.route("/", methods=['GET'])
def list_interactions():

    interactions = InteractionModel.query.all()
    output = ""

    for interaction in interactions:
        output += interaction.meta_deta 
        output += " "

    return output
