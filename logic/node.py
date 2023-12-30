class Node:
    def __init__(self, peers=None, state='idle'):
        self.peers = peers if peers is not None else []
        self.state = state

    def broadcast(self, method):
        for peer in self.peers:
            getattr(peer, method)()

    def pre_prepare(self):
        self.state = 'pre-prepared'
        self.broadcast('prepare')

    def prepare(self):
        if self.state == 'pre-prepared':
            self.state = 'prepared'
            self.broadcast('commit')

    def commit(self):
        if self.state == 'prepared':
            self.state = 'committed'