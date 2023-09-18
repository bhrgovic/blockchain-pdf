from flask import Flask, request, jsonify
from blockchain.blockchain import FileBlockchain

app = Flask(__name__)

file_blockchain = FileBlockchain(is_primary=True)

@app.route('/search', methods=['GET'])
def search_blockchain():
    pdf_name = request.args.get('pdf_name')
    print("not loopu")
    for block in file_blockchain.chain:
        print("u loopu")
        for tx in block.get("transactions", []):
            if tx.get("pdf_name") == pdf_name:
                return jsonify({"status": "found", "pdf_data": tx.get("pdf_data")})
    return jsonify({"status": "not found"}), 404


@app.route('/add_pdf', methods=['POST'])
def add_pdf():
    pdf_data = request.json.get('pdf_data')
    pdf_name = request.json.get('pdf_name')
    transaction = {
        "pdf_name": pdf_name,
        "pdf_data": pdf_data
    }
    file_blockchain.add_transaction_to_pool(transaction)
    return jsonify({"status": "added", "pdf_name": pdf_name}), 201
