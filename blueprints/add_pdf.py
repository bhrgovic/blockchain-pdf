from flask import Blueprint, jsonify, request
from databse import client,blocks_collection
from bson.json_util import dumps
from werkzeug.utils import secure_filename
from extensions import file_blockchain,network,pbft_instance
from utils.cloud_storage_utils import CloudUtils
import traceback
import hashlib

pdf_blueprint = Blueprint('pdf_blueprint', __name__)

@pdf_blueprint.route('/add_pdf', methods=['POST'])
def add_pdf():
    try:
        print("MongoDB connection string:", client)
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
        print(f"An error occurred: {e}")
        return 'Failed to add PDF', 500
