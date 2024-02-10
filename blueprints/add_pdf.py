from flask import Blueprint, jsonify, request
from databse import client,blocks_collection
from bson.json_util import dumps
from werkzeug.utils import secure_filename
from extensions import blockchain,network,pbft_instance
from utils.cloud_storage_utils import CloudUtils
from data.block import Block
import traceback
import hashlib
import base64

pdf_blueprint = Blueprint('pdf_blueprint', __name__)

@pdf_blueprint.route('/add_pdf', methods=['POST'])
def add_pdf():
    try:
        file = request.files['file']
        email = request.form.get('email')
        file_path = secure_filename(file.filename)
        file.save(file_path)

        with open(file_path, "rb") as f:
            file_data = f.read()
            base64_encoded_data = base64.b64encode(file_data).decode()
        print(blockchain.chain)
        last_block = blockchain.get_last_block()
        next_index = blockchain.get_next_index()
        if last_block is None:
            # Handle the case where the blockchain is empty
            # For example, you might want to create a genesis block
            genesis_block = Block(0, base64_encoded_data, email, "0")
            print('uhavtio genesis blok')
            last_block = genesis_block
            if network.broadcast_pre_prepare(last_block,pbft_instance, blockchain):
                if network.broadcast_prepare(last_block, pbft_instance,blockchain):
                    if network.broadcast_commit(last_block,pbft_instance, blockchain):
                        blockchain.chain.append(last_block)
                        block_info = last_block.to_dict()
                        blocks_collection.insert_one(block_info)
                        print('genesis inserted into db')
                        # cloud_utils = CloudUtils()
                        # cloud_utils.upload_blob(file_path, file_hash)
                        return jsonify({'message': 'PDF added successfully'}), 200
            else:
                return jsonify({'error': 'Invalid block'}), 400

        else:
            #print(next_index)
            new_block = blockchain.create_new_block(email,base64_encoded_data)
            #print(new_block.to_dict())
            if not new_block.validate(last_block):
                return jsonify({'error': 'Invalid block'}), 400

            if network.broadcast_pre_prepare(new_block,pbft_instance, blockchain):
                if network.broadcast_prepare(new_block, pbft_instance,blockchain):
                    if network.broadcast_commit(new_block,pbft_instance, blockchain):
                        blockchain.chain.append(new_block)
                        print(new_block.previous_hash)
                        block_info = new_block.to_dict()
                        print(block_info['previous_hash'])
                        blocks_collection.insert_one(block_info)
                        # cloud_utils = CloudUtils()
                        # cloud_utils.upload_blob(file_path, file_hash)

                        return jsonify({'message': 'PDF added successfully'}), 200
            else: 
                return jsonify({'error': 'Invalid block'}), 400
    except Exception as e:
        print(f"An error occurred: {e}")
        return 'Failed to add PDF', 500
    


@pdf_blueprint.route('/search_diploma', methods=['GET'])
def search_email():
    try:
        email = request.form.get('email')
        result = blocks_collection.find_one({'email': email})
        if result:
            return jsonify({'exists': True}), 200
        else:
            return jsonify({'does not exist': False}), 200
    except Exception as e:
        print(f"An error occurred: {e}")
        return 'Failed to search email', 500





@pdf_blueprint.route('/get_block/<block_id>', methods=['GET'])
def get_block(block_id):
    try:
        block = blocks_collection.find_one({'_id': block_id})
        if block:
            return jsonify(block), 200
        else:
            return 'Block not found', 404
    except Exception as e:
        print(f"An error occurred: {e}")
        return 'Failed to get block', 500





@pdf_blueprint.route('/delete_block/<block_id>', methods=['DELETE'])
def delete_block(block_id):
    try:
        block = blocks_collection.find_one({'email': block_id})
        if block:
            block['data'] = 'revoked'

            # Calculate the hash of the revoked data
            revoked_hash = hashlib.sha256(block['data'].encode()).hexdigest()
            block['hash'] = revoked_hash

            # Add the previous hash to the block
            previous_block = blockchain.get_previous_block()
            if previous_block:
                block['previous_hash'] = previous_block['hash']

            blocks_collection.insert_one(block)
            
            # Create a new block with the revoked data and add it to the blockchain
            revoked_block = blockchain.create_new_block(block['email'], 'revoked')
            network.broadcast_pre_prepare(revoked_block, pbft_instance, blockchain)
            network.broadcast_prepare(revoked_block, pbft_instance, blockchain)
            network.broadcast_commit(revoked_block, blockchain)
            blockchain.chain.append(revoked_block)
            
            return 'Block revoked successfully', 200
        else:
            return 'Block not found', 404
    except Exception as e:
        print(f"An error occurred: {e}")
        return 'Failed to revoke block', 500


