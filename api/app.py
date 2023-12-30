from flask import Flask, jsonify, make_response,request
from flask_socketio import SocketIO, emit
from werkzeug.exceptions import HTTPException
from logic.blockchain import FileBlockchain
from logic.transaction_pool import TransactionPool
from logic.node import Node
from logic.networking import PeerNetwork
from logic.pbft import PBFT
from logic.cloud_storage_utils import CloudUtils
import traceback
import requests
import hashlib
from werkzeug.utils import secure_filename

app = Flask(__name__)
socketio = SocketIO(app)
network = PeerNetwork()
pbft_instance = PBFT()
file_blockchain = FileBlockchain()


file_blockchain = FileBlockchain(is_primary=True)
pool = TransactionPool(file_blockchain)




@socketio.on('connect')
def handle_connect():
    emit('message', {'data': 'Connected'})

@socketio.on('transaction')
def handle_transaction(transaction):
    try:
        # Validate the transaction
        if 'pdf_data' not in transaction or 'pdf_name' not in transaction:
            raise ValueError("Invalid transaction format")

        # Add the transaction to the transaction pool
        pool.add_transaction_to_pool(transaction)

        # Broadcast the transaction to all connected clients
        emit('transaction', transaction, broadcast=True)

    except Exception as e:
        print(f"Error handling transaction: {e}")
        traceback.print_exc()

@socketio.on('request_blockchain')
def handle_request_blockchain():
    emit('response_blockchain', file_blockchain.to_dict())

@app.route('/search', methods=['GET'])
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


@app.route('/add_pdf', methods=['POST'])
def add_pdf():
    try:
        

        file = request.files['file']
        file_path = secure_filename(file.filename)
        file.save(file_path)

        # Calculate the hash of the file
        with open(file_path, "rb") as f:
           file_hash = hashlib.sha256(f.read()).hexdigest()

        # Create a new block with the file hash and add it to the blockchain
        block = file_blockchain.create_new_block(file_hash)
        network.broadcast_pre_prepare(block, pbft_instance, file_blockchain)
        network.broadcast_prepare(block, pbft_instance, file_blockchain)
        network.broadcast_commit(block, file_blockchain)
        file_blockchain.chain.append(block)

        # Upload the file to Azure Blob Storage
        cloud_utils = CloudUtils()
        cloud_utils.upload_blob(file_path, file_hash)

        return 'PDF added successfully', 200
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return 'Failed to add PDF', 500
    

@app.route('/transactions', methods=['GET'])
def get_all_transactions():
    try:
        # Get all blocks from the blockchain
        blocks = file_blockchain.chain

        return jsonify({"status": "success", "blocks": blocks}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500
    

@app.route('/send_request', methods=['POST'])
def send_request():
    try:
        # Create multiple nodes
        nodes = [Node() for _ in range(4)]

        # Each node knows about all other nodes
        for node in nodes:
            node.peers = [peer for peer in nodes if peer is not node]

        # Simulate the PBFT process
        nodes[0].pre_prepare()

        return jsonify({"status": "success"}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    # now you're handling non-HTTP exceptions only
    return make_response(jsonify({'error': 'Unexpected error occurred'}), 500)