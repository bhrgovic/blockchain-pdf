from flask import Blueprint, jsonify, request
from bson.json_util import dumps
from databse import blocks_collection
from extensions import file_blockchain
import traceback

transactions_blueprint = Blueprint('transactions_blueprint', __name__)

@transactions_blueprint.route('/transactions', methods=['GET'])
def get_all_transactions():
    try:
        # Get all blocks from the blockchain
        blocks = blocks_collection.find()

        # Convert the blocks to JSON
        blocks_json = dumps(blocks)

        return jsonify({"status": "success", "blocks": blocks_json}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500

@transactions_blueprint.route('/search', methods=['GET'])
def search_blockchain():
    try:
        pdf_name = request.args.get('pdf_name')
        if not pdf_name:
            return jsonify({"status": "failure", "message": "pdf_name is required"}), 400
        if not pdf_name.strip():
            return jsonify({"status": "failure", "message": "pdf_name cannot be empty or only whitespace"}), 400

        # Use the search_pdf method to search for the PDF
        pdf_data = file_blockchain.search_pdf(pdf_name)
        if pdf_data is None:
            return jsonify({"status": "not found", "message": f"PDF with name '{pdf_name}' not found in the blockchain or transaction pool."}), 404

        return jsonify({"status": "found", "pdf_data": pdf_data})
    except Exception as e:
        print("Exception occurred: ", e)
        traceback.print_exc()