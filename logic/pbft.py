class PBFT:
    def __init__(self, total_nodes):
        self.current_phase = None
        self.prepare_count = 0
        self.commit_count = 0
        self.total_nodes = total_nodes

    def pre_prepare(self, block, file_blockchain):
        self.current_phase = "pre_prepare"
        #print("in pbft class pre preapare ***************************************************************************")
        print(self.total_nodes)
        # Assuming pre_prepare logic passed, move to prepare phase
        return True

    def prepare(self, block, file_blockchain):
        self.current_phase = "prepare"
        self.prepare_count += 1
        # Assuming prepare logic passed, move to commit phase
        if self.prepare_count > self.total_nodes / 2:  # More than half of the nodes have prepared
            return True
        else:
            return False

    def commit(self, block, file_blockchain):
        self.current_phase = "commit"
        self.commit_count += 1
        print('commit count:' + str(self.commit_count))
        # Assuming commit logic passed, add block to chain
        if self.commit_count > self.total_nodes / 2:  # More than half of the nodes have committed
            #file_blockchain.create_new_block(block.email,block.data)
            self.reset_counts()
            return True
        else:
            return False

    def reset_counts(self):
        self.prepare_count = 0
        self.commit_count = 0

    def update_total_nodes(self, total_nodes):
        self.total_nodes = total_nodes

    def get_total_nodes(self):
        return self.total_nodes

    
