import requests

class PeerNetwork:
    def __init__(self):
        self.peers = set()

    def register_peer(self, address):
        self.peers.add(address)

    def broadcast_pre_prepare(self, block, pbft_instance, file_blockchain):
        for peer in self.peers:
            response = requests.post(f"http://{peer}/pre_prepare", json=block.to_dict())
            if response.status_code == 200:
                pbft_instance.prepare(block, file_blockchain)

    def broadcast_prepare(self, block, pbft_instance, file_blockchain):
        for peer in self.peers:
            response = requests.post(f"http://{peer}/prepare", json=block.to_dict())
            if response.status_code == 200:
                pbft_instance.commit(block, file_blockchain)

    def broadcast_commit(self, block, file_blockchain):
        for peer in self.peers:
            response = requests.post(f"http://{peer}/commit", json=block.to_dict())
            if response.status_code == 200:
                file_blockchain.add_block_to_chain(block)
