
from .validators import Validators
from .pbft import PBFT
from .networking import PeerNetwork


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

    def reply(self):
        if self.commit_count >= 2:
            self.current_phase = "reply"
            self.chain.append({"index": len(self.chain), "data": "dummy"})
            print("Added block to the blockchain")
            return True
        return False

    def discover_peers(self):
        for peer in list(self.network.peers):  # Assuming 'peers' is a property of PeerNetwork
            host, port = peer
            self.network.connect_to_peer(host, port)


