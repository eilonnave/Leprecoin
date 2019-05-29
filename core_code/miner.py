# -*- coding: utf-8 -*-
class Miner:
    def __init__(self):
        """
        constructor
        """
        self.wallet = None
        self.node = None
        self.fail = False

    def mine(self):
        """
        mines new block in the
        block chain
        """
        self.wallet.block_chain_db.\
            add_new_block_to_db(self.wallet.address)

    def handle_received_messages(self):
        """
        the function handles received messages
        from the server if those are necessary
        to the miner
        """
        pass
