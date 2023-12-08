from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import hashlib
import json
import base64

class Validators:

    def __init__(self, custom_config=None):
        self.custom_config = custom_config


    @staticmethod
    def hash_block(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def validate_block(self, new_block, prev_block):
        # Check index to make sure it's incremented by 1
        if new_block['index'] != prev_block['index'] + 1:
            return False

        # Check if previous_hash matches the hash of the previous block
        if new_block['previous_hash'] != self.hash_block(prev_block):
            return False

        # Check the integrity of the block data (You may have more validations)
        # Assuming transactions are part of the block
        if not all(self.validate_transaction(tx) for tx in new_block['transactions']):
            return False

        return True

    def validate_transaction(self, transaction):
        required_fields = ["sender", "receiver", "amount", "signature"]

        # Check if all fields are present
        if not all(key in transaction for key in required_fields):
            return False

        # Check if amount is positive
        if transaction["amount"] <= 0:
            return False

        # Verify the signature
        public_key = serialization.load_pem_public_key(
            transaction['sender'].encode(),
            backend=default_backend()
        )
        message = json.dumps({
            "sender": transaction['sender'],
            "receiver": transaction['receiver'],
            "amount": transaction['amount']
        }).encode()
        signature = base64.b64decode(transaction['signature'])
        try:
            public_key.verify(
                signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
        except:
            return False

        return True

    def validate_pre_prepare(self, pre_prepare_msg):
        required_fields = ["phase", "block", "sender", "signature"]

        # Check if all fields are present
        if not all(key in pre_prepare_msg for key in required_fields):
            return False

        # Check if the phase is 'pre-prepare'
        if pre_prepare_msg["phase"] != "pre-prepare":
            return False

        # Here you can add a check to see if the 'sender' is a valid node
        # For example:
        # if not is_valid_node(pre_prepare_msg["sender"]):
        #     return False

        # Validate the block included in the pre-prepare message
        # Assuming the block needs to be hashed to verify
        # if not self.validate_block(pre_prepare_msg['block']):
        #     return False

        return True







