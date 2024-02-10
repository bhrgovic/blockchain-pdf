from .pbft import PBFT
from .networking import PeerNetwork
import time
import hashlib
import json
from data.block import Block
from databse import blocks_collection


class FileBlockchain:
    def __init__(self):
        self.chain = []


    def get_chain(self):
        # Return the blockchain as a list of dictionaries
        return [block.to_dict() for block in self.chain]

    @classmethod   
    def load_blockchain_from_mongodb(self):

        blockchain = FileBlockchain()
        # Load and add blocks to the blockchain
        for block_data in blocks_collection.find().sort("index", 1):
            #print(block_data)
            block_data.pop('_id', None)
            # Assuming you have a method to convert dict to a Block object
            block = Block.from_dict(block_data)
            blockchain.chain.append(block)

        print(blockchain.to_dict())
        return blockchain

    def search_pdf(self, email):
        # Search for the email in the blockchain
        for block in self.chain:
            if block.email == email:
                return True

        # If email is not found, return False
        return False
    
    
    def create_new_block(self,email, data):
        # check if it's the genesis block
        if len(self.chain) == 0:
            previous_hash = None
        else:
            # get the last block in the blockchain
            last_block = self.chain[-1]
            previous_hash = last_block.hash
        print('prije konstruktora,prev hash: ', previous_hash)
        # create a new block with the given data
        new_block = Block(len(self.chain), data,email, previous_hash)
        
        print('poslije konstruktora,previous hash:' , new_block.previous_hash)
        # calculate the hash of the new block
        new_block.calculate_hash()
        return new_block

    def to_dict(self):
        return {
            'chain': self.chain
        }

    def get_last_block(self):
        if len(self.chain) > 0:
            # Return the last block in the chain
            return self.chain[len(self.chain)-1]
        else:
            return None
        
    def get_next_index(self):
        if len(self.chain) > 0:
            return self.chain[-1].index + 1
        else:
            return 0
