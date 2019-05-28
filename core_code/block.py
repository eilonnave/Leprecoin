# -*- coding: utf-8 -*-
import hashlib
import time


STARTER_NONCE = 0
DIFFICULTY = 1
BLOCK_STRUCTURE = '(number integer, ' \
                  'nonce integer, ' \
                  'prev text, ' \
                  'difficulty integer, ' \
                  'time_stamp integer)'
BLOCKS_TABLE_NAME = 'blocks'
BLOCK_KEY = 'block'
TRANSACTIONS_KEY = 'transactions'


class Block(object):
    def __init__(self,
                 number,
                 prev,
                 transactions,
                 nonce=STARTER_NONCE,
                 difficulty=DIFFICULTY,
                 time_stamp=time.time()):
        """
        constructor
        """
        self.number = number
        self.nonce = nonce
        self.prev = prev
        self.difficulty = difficulty
        self.transactions = transactions
        self.time_stamp = time_stamp
        self.hash_code = ''
        self.hash_block()

    def __str__(self):
        """
        the function converts the block to a string for
        the hash function
        :returns: the block's string
        """
        # the hash function is not including
        # the time_stamp
        block_string = str(self.serialize()[:-1])+self.hash_transactions()
        return block_string

    def hash_block(self):
        """
        the function hashes the block data
        """
        self.hash_code = hashlib.sha256(
            self.__str__().encode(
                'utf-8')).hexdigest()

    def hash_transactions(self):
        """
        the function hashes all the transactions
        together
        :returns: the hash code of all the transactions
        """
        if len(self.transactions) == 0:
            return ''
        transactions_hash = self.transactions[0].hash_transaction()
        for transaction in self.transactions[1:]:
            transaction_hash = transaction.hash_transaction()
            transactions_hash = hashlib.sha256(
                (transactions_hash+transaction_hash))\
                .hexdigest()
        return transactions_hash

    def add_transaction(self, transaction):
        """
        the function adds the transaction
        to the list in the block
        :param transaction: a transaction to add
        """
        self.transactions.append(transaction)

    def mine_block(self):
        """
        the function mines the block
        """
        self.nonce = STARTER_NONCE
        while not self.is_valid_proof():
            self.nonce += 1
            self.hash_block()
        self.time_stamp = time.time()

    def is_valid_proof(self):
        """
        check if the block hash is valid
        :returns: whether the proof of work
        on the block is valid
        """
        return self.hash_code[0:self.difficulty] == '0'*self.difficulty

    def serialize(self):
        """
        the function serializes the block
        :returns: the serialized block
        """
        return self.number, self.nonce, self.prev, self.difficulty, self.time_stamp

    @classmethod
    def deserialize(cls, serialized_block, transactions):
        """
        the function deserializes the block
        from the serialized block and the transactions
        :param serialized_block: the serialized block
        :param transactions: the block's transactions
        :returns: the deserialized block
        """
        number = serialized_block[0]
        nonce = serialized_block[1]
        prev = str(serialized_block[2])
        difficulty = serialized_block[3]
        time_stamp = serialized_block[4]
        transactions = transactions
        return cls(number,
                   prev,
                   transactions,
                   nonce,
                   difficulty,
                   time_stamp)
