from logic.blockchain import FileBlockchain
import json
from .complex_encoder import ComplexEncoder

def load_blockchain_from_file(filename):
    with open(filename, 'r') as f:
        blockchain_dict = json.load(f)
    if not blockchain_dict:
        return FileBlockchain()
    blockchain = FileBlockchain()
    blockchain.chain = blockchain_dict['chain']
    blockchain.transaction_pool = blockchain_dict['transaction_pool']
    return blockchain

def save_blockchain(file_blockchain, filename='blockchain.json'):
    blockchain_dict = {
        'chain': file_blockchain.chain,
        'transaction_pool': file_blockchain.transaction_pool
    }
    with open(filename, 'w') as f:
        json.dump(blockchain_dict, f, cls=ComplexEncoder, indent=4)
