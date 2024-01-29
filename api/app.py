from flask import Flask, jsonify, make_response,request
from flask_socketio import SocketIO, emit
from werkzeug.exceptions import HTTPException
from logic.blockchain import FileBlockchain
from logic.transaction_pool import TransactionPool
from logic.node import Node
from logic.networking import PeerNetwork
from logic.pbft import PBFT
from logic.cloud_storage_utils import CloudUtils
from werkzeug.utils import secure_filename
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.json_util import dumps
from dotenv import load_dotenv
from data.block import Block
from logic.complex_encoder import ComplexEncoder
import traceback
import requests
import hashlib
import json
import os


load_dotenv()
mongo_connection_string = os.getenv('MONGO')
app = Flask(__name__)
socketio = SocketIO(app)
network = PeerNetwork()
pbft_instance = PBFT()
client = MongoClient(mongo_connection_string)
db = client['blockchainpdf']

def load_blockchain_from_file(filename):
    with open(filename, 'r') as f:
        blockchain_dict = json.load(f)
    if not blockchain_dict:
        return FileBlockchain()
    blockchain = FileBlockchain()
    blockchain.chain = blockchain_dict['chain']
    blockchain.transaction_pool = blockchain_dict['transaction_pool']
    return blockchain


file_blockchain = load_blockchain_from_file('blockchain.json')
pool = TransactionPool(file_blockchain)


transaction_collection = db['transactions']
blocks_collection = db['blocks']

@socketio.on('connect')
def handle_connect():
    emit('message', {'data': 'Connected'})

@socketio.on('transaction')
def handle_transaction(transaction):
    try:
        if 'pdf_data' not in transaction or 'pdf_name' not in transaction:
            raise ValueError("Invalid transaction format")

        pool.add_transaction_to_pool(transaction)

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
        print("MongoDB connection string:", mongo_connection_string)
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

        block_info = block.to_dict()

        # Save the block to the database
        blocks_collection.insert_one(block_info)

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
        blocks = blocks_collection.find()

        # Convert the blocks to JSON
        blocks_json = dumps(blocks)

        return jsonify({"status": "success", "blocks": blocks_json}), 200
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
    

def save_blockchain():
    blockchain_dict = {
        'chain': file_blockchain.chain,
        'transaction_pool': file_blockchain.transaction_pool
    }
    with open('blockchain.json', 'w') as f:
        json.dump(blockchain_dict, f, cls=ComplexEncoder,indent=4)

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