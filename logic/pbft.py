class PBFT:
    def __init__(self):
        self.current_phase = None
        self.prepare_count = 0
        self.commit_count = 0

    def pre_prepare(self, block, file_blockchain):
        self.current_phase = "pre_prepare"
        # Assuming pre_prepare logic passed, move to prepare phase
        self.prepare(block, file_blockchain)

    def prepare(self, block, file_blockchain):
        self.current_phase = "prepare"
        self.prepare_count += 1
        # Assuming prepare logic passed, move to commit phase
        if self.prepare_count >= 2:  # You should replace this with more robust logic
            self.commit(block, file_blockchain)

    def commit(self, block, file_blockchain):
        self.current_phase = "commit"
        self.commit_count += 1
        # Assuming commit logic passed, add block to chain
        if self.commit_count >= 2:  # You should replace this with more robust logic
            file_blockchain.add_block_to_chain(block)
