from flask import Blueprint,jsonify,request
from logic.pbft import PBFT
from data.block import Block
from extensions import blockchain,pbft_instance

view_pbft = Blueprint('view_pbft',__name__)

@view_pbft.route('/pre_prepare',methods=['POST'])
def pre_prepare():
    block_data = request.get_json()
    block = Block.from_dict(block_data)  # Assuming you have a method to reconstruct a block from JSON data
    print(f"Received pre_prepare with block: {block}")
    # Validate the block
    last_block = blockchain.get_last_block()
    if Block.validate(block,last_block):  # Assuming you have a validate_block method
        print('validating in pre preapare')
        pbft_instance.pre_prepare(block, blockchain)
    return jsonify({"status": "success"}), 200

@view_pbft.route('/prepare',methods=['POST'])
def prepare():
    block_data = request.get_json()
    block = Block.from_dict(block_data)
    # Here, you should also check whether the node is in the pre_prepare phase for this block
    pbft_instance.prepare(block, blockchain)
    return jsonify({"status": "success"}), 200


@view_pbft.route('/commit',methods=['POST'])
def commit():
    block_data = request.get_json()
    block = Block.from_dict(block_data)
    # Similar to prepare, ensure the node is ready to commit this block
    pbft_instance.commit(block, blockchain)
    return jsonify({"status": "success"}), 200

    