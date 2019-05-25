# -*- coding: utf-8 -*-
import sqlite3
import os
from core_code.block import BLOCK_STRUCTURE, \
    BLOCKS_TABLE_NAME, \
    Block
from core_code.transaction import *
from core_code.blockchain import BlockChain


DB_DIR = 'database'
BLOCK_CHAIN_DB_FILE = 'block_chain.db'
EXTRACT_ALL_QUERY = 'select * from '


class Table(object):
    def __init__(self, connection, cursor, table_name, structure):
        """
        constructor
        """
        self.connection = connection
        self.cursor = cursor
        self.table_name = table_name
        self.structure = structure
        self.create_table()

    def create_table(self):
        """
        creates the table in the data base
        if it does not exist
        """
        query = 'create table if not exists ' \
                ''+self.table_name+' ' \
                                   ''+self.structure
        self.cursor.execute(query)
        self.connection.commit()

    def insert(self, serialized_obj):
        """
        the function inserts object to the table
        :param serialized_obj: the object to insert
        """
        # building the query
        length = len(serialized_obj)
        query = \
            'insert into '\
            + self.table_name\
            + ' values ('\
            + ('?, '*(length-1))+'?)'
        self.cursor.execute(query, serialized_obj)
        self.connection.commit()


class BlockChainDB(BlockChain):
    def __init__(self, logger, db_name=BLOCK_CHAIN_DB_FILE):
        """
        constructor
        """
        self.logger = logger
        self.connection = None
        self.cursor = None
        default_cwd = os.getcwd()
        parent_path = os.path.dirname(default_cwd)
        if not os.path.isdir(parent_path+'/'+DB_DIR):
            os.mkdir(parent_path+'/'+DB_DIR)
        os.chdir(parent_path+'/'+DB_DIR)
        self.path = parent_path+'/'+DB_DIR+'/'+db_name
        self.create_connection()
        self.blocks_table = Table(self.connection,
                                  self.cursor,
                                  BLOCKS_TABLE_NAME,
                                  BLOCK_STRUCTURE)
        self.transactions_table = Table(self.connection,
                                        self.cursor,
                                        TRANSACTIONS_TABLE_NAME,
                                        TRANSACTION_STRUCTURE
                                        )
        self.inputs_table = Table(self.connection,
                                  self.cursor,
                                  INPUTS_TABLE_NAME,
                                  INPUT_STRUCTURE)
        self.outputs_table = Table(self.connection,
                                   self.cursor,
                                   OUTPUTS_TABLE_NAME,
                                   OUTPUT_STRUCTURE)
        chain = self.extract_chain()
        super(BlockChainDB, self).__init__(chain, logger)
        os.chdir(default_cwd)

    def create_connection(self):
        """
        creates new connection to the data
        base
        """
        self.connection = sqlite3.connect(self.path)
        self.connection.text_factory = bytes
        self.cursor = self.connection.cursor()
        self.logger.info('Connected to the db')

    def close_connection(self):
        """
        closes the connection and the cursor
        """
        self.cursor.close()
        self.connection.close()
        self.logger.info('Connection is closed with the db')

    def insert_block(self, block):
        """
        the function inserts block to the database
        :param block: the block to insert
        """
        # insert the block
        self.blocks_table.insert(block.serialize())

        # insert the transactions
        block_number = block.number
        for transaction in block.transactions:
            self.transactions_table.insert(
                (transaction.transaction_id, block_number))
            transaction_number = transaction.transaction_id
            # insert the inputs
            for transaction_input in transaction.inputs:
                self.inputs_table.insert(
                    transaction_input.serialize()+(transaction_number,))
            # insert the outputs
            for transaction_output in transaction.outputs:
                self.outputs_table.insert(
                    transaction_output.serialize()+(transaction_number,))
        self.logger.info('The new block was inserted to the data base')

    def extract_block(self, line_index):
        """
        the function extracts from the
        data base the block from the given line
        index
        :param line_index: the line index of the
        block extract
        :returns: the extracted block
        """
        query = \
            EXTRACT_ALL_QUERY\
            + self.blocks_table.table_name\
            + ' where number=?'
        self.cursor.execute(query, (line_index,))
        serialized_block = self.cursor.fetchone()
        transactions = self.extract_transactions(line_index)
        self.logger.info('Block number '+str(line_index)+' extracted for the db')
        return Block.deserialize(serialized_block, transactions)

    def extract_inputs(self, transaction_number):
        """
        the function extracts from the database
        all the inputs matching to the transaction
        number
        :param transaction_number: the transaction number
        that the inputs should be belong to
        :returns: the list of the inputs
        """
        inputs = []
        query = \
            EXTRACT_ALL_QUERY\
            + self.inputs_table.table_name\
            + ' where transaction_number=?'
        self.cursor.execute(query, (transaction_number,))
        serialized_inputs = self.cursor.fetchall()
        for serialized_input in serialized_inputs:
            inputs.append(Input.deserialize(serialized_input))
        return inputs

    def extract_outputs(self, transaction_number):
        """
        the function extracts from the database
        all the outputs matching to the transaction
        number
        :param transaction_number: the transaction number
        that the outputs should be belong to
        :returns: the list of the outputs
        """
        outputs = []
        query = \
            EXTRACT_ALL_QUERY\
            + self.outputs_table.table_name\
            + ' where transaction_number=?'
        self.cursor.execute(query, (transaction_number,))
        serialized_outputs = self.cursor.fetchall()
        for serialized_output in serialized_outputs:
            outputs.append(Output.deserialize(serialized_output))
        return outputs

    def extract_transactions(self, block_number):
        """
        the function extracts from the database
        all the transactions matching to the block
        number
        :param block_number: the block number
        that the transactions should be belong to
        :returns: the list of the transactions
        """
        # extract the transactions
        query = \
            EXTRACT_ALL_QUERY\
            + self.transactions_table.table_name\
            + ' where block_number =?'
        self.cursor.execute(query, (block_number,))
        block_transactions = self.cursor.fetchall()

        # build the transactions using the inputs and
        # the outputs
        transactions = []
        for serialized_transaction in block_transactions:
            transaction_number = serialized_transaction[0]
            inputs = self.extract_inputs(transaction_number)
            outputs = self.extract_outputs(transaction_number)
            transactions.append(Transaction.deserialize(inputs, outputs))
        return transactions

    def extract_chain(self):
        """
        the function extracts from the
        data base list of the all blocks
        inside
        :returns: list of the extracted blocks
        """
        # get the blocks table length
        query = 'select count(*) from '+self.blocks_table.table_name
        self.cursor.execute(query)
        count = self.cursor.fetchone()[0]

        chain = []
        for i in range(count):
            chain.append(self.extract_block(i))
        return chain

    def add_new_block_to_db(self, miner_address):
        """
        the function mines the block and adds it to the block
        chain database and to the chain
        :param miner_address: the miner address to reward
        """
        self.add_new_block(miner_address)
        new_block = self.chain[-1]
        self.insert_block(new_block)

    def update_chain(self):
        """
        the function updates the chain using the data
        base
        """
        self.chain = self.extract_chain()

    def add_downloaded_blocks(self, blocks):
        """
        the function adds the given blocks
        to the chain. the blocks are valid
        and were downloaded from other
        nodes.
        :param blocks: the blocks to add
        """
        for block in blocks:
            self.chain.append(block)
            self.insert_block(block)
