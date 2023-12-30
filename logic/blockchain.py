
from .validators import Validators
from .pbft import PBFT
from .networking import PeerNetwork
import time
import hashlib
import json


class FileBlockchain:
    def __init__(self, is_primary=False):
        self.chain = []
        self.is_primary = is_primary
        self.transaction_pool = []
        self.pbft = PBFT()
        self.network = PeerNetwork()
        self.current_phase = None
        self.prepare_count = 0
        self.commit_count = 0
        self.validator = Validators()

    def set_primary(self, is_primary):
        self.is_primary = is_primary

    def add_transaction(self, transaction):
        self.transaction_pool.append(transaction)

    def reply(self,data):
        if self.commit_count == 1:
            self.current_phase = "reply"
            self.chain.append({"index": len(self.chain), "data": data})
            print("Added block to the blockchain")
            return True
        return False

    def search_pdf(self, pdf_name):
        # Search for the PDF in the blockchain
        for block in self.chain:
            if block.get("data") == pdf_name:
                return block.get("data")

        # Search for the PDF in the transaction pool
        for tx in self.transaction_pool:
            if tx.get("data") == pdf_name:
                return tx.get("data")

        # If pdf_name is not found, return None
        return None

    
    def add_pdf(self, pdf):
        # Add the PDF to the blockchain or transaction pool
        # This is just a placeholder implementation. You'll need to replace it with your actual implementation.
        self.chain.append({"transactions": [{"pdf_name": pdf["pdf_name"], "pdf_data": pdf["pdf_data"]}]})


    def create_new_block(self, data):
        # check if it's the genesis block
        if len(self.chain) == 0:
            previous_hash = None
        else:
            # get the last block in the blockchain
            last_block = self.chain[-1]
            previous_hash = last_block['hash']

        # create a new block with the given data
        new_block = {
            'index': len(self.chain),
            'timestamp': time.time(),
            'data': data,
            'previous_hash': previous_hash,
        }

        # calculate the hash of the new block
        new_block['hash'] = self.calculate_hash(new_block)

        return new_block
    
    def calculate_hash(self, block):
        # create a string representation of the block
        block_string = json.dumps(block, sort_keys=True)

        # calculate the SHA-256 hash of the block string
        return hashlib.sha256(block_string.encode()).hexdigest()
