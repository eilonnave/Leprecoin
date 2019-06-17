# -*- coding: utf-8 -*-
import threading
from core_code.wallet import Wallet
from Crypto.PublicKey import RSA
from core_code.logger import Logging
from core_code.database import BlockChainDB
from core_code.node import Node, WAITING_TIME
import pickle
import os
from core_code.messages import Inv, \
    GetData, \
    BlockMessage, \
    TransactionMessage, \
    Error, \
    GetAddresses
from core_code.blockchain import REWORD
from core_code.block import Block, DIFFICULTY, STARTER_NONCE
import time
from core_code.transaction import Transaction, \
    Input, \
    Output
from core_code.database import KnownNodes


PRIVATE_KEY_FILE = 'private_key.txt'
GENERATE_NUMBER = 2048
MIN_TRANSACTIONS = 1


class Miner(Node):
    """
    Miner node
    """
    def __init__(self):
        """
        constructor
        """
        self.loggers = [Logging('wallet').logger,
                        Logging('network').logger,
                        Logging('block_chain').logger]
        self.block_chain_db = BlockChainDB(self.loggers[2])
        self.global_transaction_pool = self.block_chain_db.transactions_pool
        super(Miner, self).__init__(self.loggers[1], self.block_chain_db)

        self.fail = False
        # open private key file for the address
        if os.path.isfile(PRIVATE_KEY_FILE):
            with open(PRIVATE_KEY_FILE, 'r') as private_key_file:
                private_key = pickle.load(private_key_file)
                private_key = RSA.import_key(private_key)
        else:
            with open(PRIVATE_KEY_FILE, 'w') as private_key_file:
                private_key = RSA.generate(GENERATE_NUMBER)
                pickle.dump(private_key.export_key(),
                            private_key_file)
        self.wallet = Wallet(private_key,
                             self.block_chain_db,
                             self.loggers[0])

    def run(self):
        """
        the function runs the mining and
        the node
        """
        self.find_connections()
        self.update_chain()
        mine_thread = threading.Thread(target=self.mine)
        handle_messages_thread = threading.Thread(target=self.handle_messages)
        handle_messages_thread.start()
        mine_thread.start()

    def mine(self):
        """
        mines new block in the
        block chain
        """
        self.block_chain_db = BlockChainDB(self.loggers[2])
        self.block_chain_db.transactions_pool = self.global_transaction_pool
        while True:
            self.fail = False
            chain = self.block_chain_db.chain
            number = len(chain)
            # transaction that rewards the miner
            # the input proof is arbitrary
            transaction_input = Input(str(len(chain)),
                                      -1,
                                      [self.wallet.address, ''])
            transaction_output = Output(REWORD, self.wallet.address)
            new_transaction = Transaction([transaction_input],
                                          [transaction_output])

            # wait until there are enough transactions in the pool
            while len(self.block_chain_db.transactions_pool) < MIN_TRANSACTIONS:
                pass
            self.block_chain_db.add_transaction(new_transaction)

            transactions_to_mine = []
            for transaction in self.block_chain_db.transactions_pool:
                transactions_to_mine.append(transaction)

            # create the block
            block = Block(number, chain[-1].hash_code,
                          transactions_to_mine)
            self.logger.info('Mining new block')
            block.nonce = STARTER_NONCE
            while (not block.is_valid_proof()) and (not self.fail):
                block.nonce += 1
                block.hash_block()

            if self.fail:
                self.block_chain_db.transactions_pool.remove(new_transaction)
                self.logger.info('Failed in mining the block')

            else:
                block.time_stamp = time.time()
                # set the block chain
                self.block_chain_db.add_block(block)
                inv = Inv(self.address, 'block', [block.hash_code])
                self.msg_handler.change_message(inv, False)
                self.msg_handler.pack()
                self.client.send_to_all(self.msg_handler.message)
                for transaction in block.transactions:
                    i = 0
                    for transaction_in_pool in self.block_chain_db.transactions_pool:
                        if transaction_in_pool.transaction_id == transaction.transaction_id:
                            self.block_chain_db.transactions_pool.pop(i)
                            break
                        i += 1
                self.logger.info('Succeed in mining block')

    def handle_messages(self):
        """
        the function handles received messages
        from the server if those are necessary
        to the miner
        """
        self.block_chain_db = BlockChainDB(self.loggers[2])
        self.block_chain_db.transactions_pool = self.global_transaction_pool
        self.known_nodes_db = KnownNodes(self.logger)
        while True:
            messages_list = self.server.get_received_messages()
            for message_tup in messages_list:
                self.server.remove_message(message_tup)
                message = message_tup[0]
                address = message_tup[1]
                self.msg_handler.change_message(message,
                                                True)
                self.msg_handler.unpack_message()
                if type(self.msg_handler.message) is Error:
                    self.logger.info('Wrong data received')
                else:
                    self.msg_handler.message.address_from = address
                    if self.msg_handler.message.address_from not in self.known_nodes:
                        self.known_nodes.append(self.msg_handler.message.address_from)
                        self.known_nodes_db.insert_address(
                            self.msg_handler.message.address_from)
                    if type(self.msg_handler.message) is Inv:
                        if self.msg_handler.message.address_from not in self.known_nodes:
                            self.known_nodes.append(self.msg_handler.message.address_from)
                        self.handle_inv(self.msg_handler.message)
                    elif type(self.msg_handler.message) is GetData:
                        if self.msg_handler.message.address_from not in self.known_nodes:
                            self.known_nodes.append(self.msg_handler.message.address_from)
                        self.handle_get_data(self.msg_handler.message)
                    elif type(self.msg_handler.message) is GetAddresses:
                        if self.msg_handler.message.address_from not in self.known_nodes:
                            self.known_nodes.append(self.msg_handler.message.address_from)
                        self.handle_get_addresses(self.msg_handler.message)

    def handle_inv(self, inv_message):
        """
        handles inv message
        :param inv_message: the inv message
        """
        self.logger.info('Handle inv message from ' +
                         inv_message.address_from)
        if len(inv_message.hash_codes) != 0:
            if inv_message.data_type == 'transaction':
                self.handle_transaction_inv(inv_message)
            elif inv_message.data_type == 'block':
                self.handle_block_inv(inv_message)

    def handle_block_inv(self, inv_message):
        """
        the function handles inv message of a block type
        :param inv_message: the block inv message
        """
        is_found = False
        is_legal = False
        hash_code = inv_message.hash_codes[0]
        if hash_code[0:DIFFICULTY] == '0'*DIFFICULTY:
            is_legal = True
        if is_legal:
            # check if the block is already found
            for block in self.block_chain_db.chain:
                if hash_code == block.hash_code:
                    is_found = True
                    break
        else:
            self.logger.info('block hash is not legal')

        if not is_found and is_legal:
            # request the block from the node
            get_data_message = GetData(self.address,
                                       'block',
                                       hash_code)
            self.msg_handler.change_message(
                get_data_message, False)
            self.msg_handler.pack()
            self.client.send(self.msg_handler.message,
                             inv_message.address_from)

            # wait for respond
            time.sleep(WAITING_TIME)

            # handle the responds
            messages_list = self.server.get_received_messages()
            for message_tup in messages_list:
                message = message_tup[0]
                address = message[1]
                self.msg_handler.change_message(
                    message, True)
                self.msg_handler.unpack_message()
                if type(self.msg_handler.message) is BlockMessage:
                    self.msg_handler.message.address_from = address
                    self.logger.info('Handle block message')
                    self.server.remove_message(message_tup)
                    if self.msg_handler.message.address_from == \
                            inv_message.address_from:
                        block = self.msg_handler.message.block
                        if block.hash_code == hash_code:
                            if self.verify_block(block):
                                self.block_chain_db.add_block(block)
                                for transaction in block.transactions:
                                    i = 0
                                    for transaction_in_pool in self.block_chain_db.transactions_pool:
                                        if transaction_in_pool.transaction_id == transaction.transaction_id:
                                            self.block_chain_db.transactions_pool.pop(i)
                                            break
                                        i += 1
                                self.fail = True
                            break

    def handle_transaction_inv(self, inv_message):
        """
        handles transaction inv message
        :param inv_message: the inv message
        """
        is_found = False
        hash_code = inv_message.hash_codes[0]

        # check if the transaction is already found
        for transaction in self.block_chain_db.transactions_pool:
            if hash_code == transaction.transaction_id:
                is_found = True
                break

        if not is_found:
            # request the transaction from the node
            get_data_message = GetData(self.address,
                                       'transaction',
                                       hash_code)
            self.msg_handler.change_message(
                get_data_message, False)
            self.msg_handler.pack()
            self.client.send(self.msg_handler.message,
                             inv_message.address_from)

            # wait for respond
            time.sleep(WAITING_TIME)
            messages_list = self.server.get_received_messages()

            # handle the responds
            for message_tup in messages_list:
                message = message_tup[0]
                address = message_tup[1]
                self.msg_handler.change_message(message, True)
                self.msg_handler.unpack_message()
                if type(self.msg_handler.message) is TransactionMessage:
                    self.msg_handler.message.address_from = address
                    self.logger.info('Handle transaction message')
                    self.server.remove_message(message_tup)
                    if self.msg_handler.message.address_from == \
                            inv_message.address_from:
                        transaction = self.msg_handler.message.transaction
                        if transaction.transaction_id == hash_code:
                            if self.verify_transaction(transaction):
                                self.block_chain_db.add_transaction(transaction)
                            break


if __name__ == '__main__':
    Miner().run()
