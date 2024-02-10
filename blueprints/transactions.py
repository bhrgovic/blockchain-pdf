from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from bson.json_util import dumps
from databse import blocks_collection
from extensions import blockchain
from data.block import Block
import traceback

transactions_blueprint = Blueprint('transactions_blueprint', __name__)

@transactions_blueprint.route('/transactions', methods=['GET'])
@jwt_required()
def get_all_transactions():
    try:
        data = blockchain.get_chain()
        
        return jsonify({"status": "success", "blocks": data}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500

@transactions_blueprint.route('/search', methods=['GET'])
def search_blockchain():
    try:
        email = request.args.get('email')  # Ensure this matches the query parameter name
        if not email:
            return jsonify({"status": "failure", "message": "Email is required"}), 400
        if not email.strip():
            return jsonify({"status": "failure", "message": "Email cannot be empty or only whitespace"}), 400

        # Use the search_pdf method to check if the email is on the blockchain
        is_valid_diploma = blockchain.search_pdf(email)
        if is_valid_diploma:
            return jsonify({"status": "success", "message": "Diploma is valid."})
        else:
            return jsonify({"status": "not found", "message": f"Diploma with email '{email}' not found on the blockchain."}), 404
    except Exception as e:
        print("Exception occurred: ", e)
        traceback.print_exc()
        return jsonify({"status": "error", "message": "An internal error occurred"}), 500


@transactions_blueprint.route('/print_chain', methods=['GET'])
def print_chain():
    # Get the blockchain data
    blockchain_data = blockchain.get_chain()

    # Return the blockchain data as a JSON response
    return jsonify(blockchain_data), 200

@transactions_blueprint.route('/last_hash', methods=['GET'])
def print_last_hash():
    # Get the blockchain data
    blockchain_data = blockchain.get_last_block()
    var = blockchain_data.to_dict()

    # Return the blockchain data as a JSON response
    return jsonify(var), 200


