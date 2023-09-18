

class TransactionPool:

    def add_transaction_to_pool(self, transaction):
        self.transaction_pool.append(transaction)
        if len(self.transaction_pool) >= 3:  # Assume 3 transactions per block
            new_block = self.create_new_block()
            self.network.broadcast_pre_prepare(new_block, self.pbft, self)

    def create_new_block(self):
        new_block = {"index": len(self.chain), "transactions": self.transaction_pool}
        self.transaction_pool = []
        return new_block