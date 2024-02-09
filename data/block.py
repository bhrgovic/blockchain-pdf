import time
import hashlib
import json

class Block:
    def __init__(self, index, data, email,previous_hash,hash=None):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.email = email
        self.previous_hash = previous_hash
        self.hash = hash or self.calculate_hash()

    def calculate_hash(self):
        # Calculate and return the hash of the block
        block_contents = f"{self.index}{self.timestamp}{self.data}{self.email}{self.previous_hash}"
        return hashlib.sha256(block_contents.encode()).hexdigest()

    @classmethod
    def from_dict(cls, block_data):
        # Convert a dictionary to a Block instance
        return cls(
            index=block_data['index'],
            data=block_data['data'],
            email=block_data['email'],
            hash = block_data['hash'],
            previous_hash=block_data['previous_hash']
        )

    def to_dict(self):
        # Convert a Block instance to a dictionary
        return {
            'index': self.index,
            'data': self.data,
            'email': self.email,
            'previous_hash': self.previous_hash,
            'hash': self.hash
        }
    
    def validate(self, previous_block):
        # Special case for the genesis block
        if self.index == 0:  # Assuming genesis block has index 0
            # Validation logic for genesis block
            # Typically, you might check its structure, predefined values, etc.
            return True

        # For non-genesis blocks:
        
        # Check if the block's index is correct
        if self.index != previous_block.index + 1:
            return False

        # Check if the block's previous_hash is correct
        if self.previous_hash != previous_block.hash:
            return False

        # Check if the block's timestamp is valid
        if self.timestamp <= previous_block.timestamp:
            return False

        # Check if the block's hash is correct
        if self.hash != self.calculate_hash():
            return False

        return True

    # Getter methods
    def get_index(self):
        return self.index

    def get_timestamp(self):
        return self.timestamp

    def get_data(self):
        return self.data

    def get_email(self):
        return self.email

    def get_previous_hash(self):
        return self.previous_hash

    def get_hash(self):
        return self.hash

    # Setter methods
    def set_index(self, index):
        self.index = index

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def set_data(self, data):
        self.data = data

    def set_email(self, email):
        self.email = email

    def set_previous_hash(self, previous_hash):
        self.previous_hash = previous_hash

    def set_hash(self, hash):
        self.hash = hash
    
    @staticmethod
    def get_block_by_chain_id(chain, chain_id):
        # Iterate through the chain and find the block with the given chain_id
        for block in chain:
            if block.get_index() == chain_id:
                return block
        return None
    
    