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

    def add_new_block(self, miner_address):
        """
        the function adds new block to the chain
        and rewards the miner
        :param miner_address: the miner address
        to reward
        """
        number = len(self.chain)

        # handle genesis block
        if number == 0:
            prev = '0'*32
        else:
            prev = self.chain[-1].hash_code

        # transaction that rewards the miner
        # the input proof is arbitrary
        transaction_input = Input(str(len(self.chain)), -1, [miner_address, ''])
        transaction_output = Output(REWORD, miner_address)
        new_transaction = Transaction([transaction_input],
                                      [transaction_output])
        self.add_transaction(new_transaction)

        # create the block
        block = Block(number, prev, self.transactions_pool)
        self.logger.info('Mining new block')
        block.mine_block()

        # set the block chain
        self.chain.append(block)
        self.transactions_pool = []
        self.logger.info('The new block was added to the block chain')