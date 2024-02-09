import requests


class PeerNetwork:
    def __init__(self):
        self.peers = []

    def register_peer(self, address):
        self.peers.append(address)

    def broadcast_pre_prepare(self, block, pbft_instance, file_blockchain):
        for peer in self.peers:
            #print('broadcast_pre_prepare')

            # Ensure the peer address is correctly formatted as "IP:Port"
            if isinstance(peer, list):
                peer_address = f"{peer[0]}:{peer[1]}"
            else:
                peer_address = peer

            response = requests.post(f"http://{peer_address}/pre_prepare", json=block.to_dict())
            if response.status_code == 200:
                #print("response ok")
                if pbft_instance.pre_prepare(block, file_blockchain):
                    return True
                else:
                    return False

    def broadcast_prepare(self, block, pbft_instance, file_blockchain):
        for peer in self.peers:
            #print('broadcast_prepare')
            if isinstance(peer, list):
                peer_address = f"{peer[0]}:{peer[1]}"
            else:
                peer_address = peer
            response = requests.post(f"http://{peer_address}/prepare", json=block.to_dict())
            if response.status_code == 200:
                if pbft_instance.prepare(block, file_blockchain):
                    return True
                else:
                    return False

    def broadcast_commit(self, block,pbft_instance, file_blockchain):
        for peer in self.peers:
            #print('broadcast_commit')
            if isinstance(peer, list):
                peer_address = f"{peer[0]}:{peer[1]}"
            else:
                peer_address = peer
            response = requests.post(f"http://{peer_address}/commit", json=block.to_dict())
            if response.status_code == 200:
                if pbft_instance.commit(block,file_blockchain):
                    return True
                else:
                    return False
