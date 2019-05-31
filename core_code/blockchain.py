# -*- coding: utf-8 -*-
from core_code.block import Block
from core_code.transaction import Transaction, Input, Output


BLOCK_HASH_SIZE = 256
REWORD = 50


class BlockChain(object):
    def __init__(self, chain, logger):
        """
        constructor
        """
        self.chain = chain
        self.transactions_pool = []
        self.logger = logger

    def add_transaction(self, transaction):
        """
        the function adds new transaction
        to the transactions pool
        :param transaction: new transaction to add
        """
        self.transactions_pool.append(transaction)