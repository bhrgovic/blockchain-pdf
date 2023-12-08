from flask import Flask, request, jsonify
# Make sure the import statement aligns with your project structure
from logic import blockchain,transaction_pool
import traceback

app = Flask(__name__)

file_blockchain = blockchain.FileBlockchain(is_primary=True)
pool = transaction_pool.TransactionPool(file_blockchain)

@app.route('/search', methods=['GET'])
def search_blockchain():
    try:
        pdf_name = request.args.get('pdf_name')
        if pdf_name is None:
            return jsonify({"status": "failure", "message": "pdf_name is required"}), 400

        # Search for the PDF in the blockchain
        for block in file_blockchain.chain:
            for tx in block.get("transactions", []):
                if tx.get("pdf_name") == pdf_name:
                    return jsonify({"status": "found", "pdf_data": tx.get("pdf_data")})

        # Search for the PDF in the transaction pool
        for tx in file_blockchain.transaction_pool:
            if tx.get("pdf_name") == pdf_name:
                return jsonify({"status": "found", "pdf_data": tx.get("pdf_data")})

        # If pdf_name is not found, return a user-friendly error message
        return jsonify({"status": "not found", "message": f"PDF with name '{pdf_name}' not found in the blockchain or transaction pool."}), 404
    except Exception as e:
        # Print the full stack trace to the console
        traceback.print_exc()
        return jsonify({"status": "error", "message": "An unexpected error occurred."}), 500

@app.route('/add', methods=['POST'])
def add_pdf():
    try:
        # Get the PDF data from the request
        pdf_data = request.json.get('pdf_data')
        if pdf_data is None:
            return jsonify({"status": "failure", "message": "pdf_data is required"}), 400

        # Add the PDF to the blockchain
        file_blockchain.add_pdf(pdf_data)

        # Return a successful response
        return jsonify({"status": "success", "message": "PDF added to the blockchain."}), 200
    except Exception as e:
        # Print the full stack trace to the console
        traceback.print_exc()
        # Return an error response
        return jsonify({"status": "error", "message": "An unexpected error occurred."}), 500

@app.route('/transactions', methods=['GET'])
def get_all_transactions():
    try:
        transactions = []

        # Add transactions from the blockchain
        for block in file_blockchain.chain:
            for tx in block.get("transactions", []):
                transactions.append(tx)

        # Add transactions from the transaction pool
        for tx in file_blockchain.transaction_pool:
            transactions.append(tx)

        return jsonify({"status": "success", "transactions": transactions}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500