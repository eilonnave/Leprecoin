# -*- coding: utf-8 -*-
import os
import re
import threading
import time
from core_code.node_server import NodeServer
from core_code.node_client import NodeClient
from core_code.messages import MessagesHandler, \
    Version, \
    GetBlocks, \
    Inv, \
    GetData, \
    BlockMessage, \
    TransactionMessage, \
    Error, \
    GetAddresses, \
    AddressesMessage
from Crypto.Hash import SHA256
from core_code.logger import Logging
from core_code.database import BlockChainDB
from core_code.block import Block, DIFFICULTY
from core_code.wallet import Wallet
from core_code.crypto_set import CryptoSet
from core_code.transaction import UnspentOutput
from core_code.database import HostNodes, KnownNodes
from core_code.blockchain import REWORD

# ToDo: check connections before downloading
# ToDo: handle possible errors in receiving messages

WAITING_TIME = 2
WALLET_ADDRESS_LENGTH = 40
HEX_DIGEST = '0123456789abcdef'
MAX_HASHES_IN_INV = 500


class Node(object):
    """
    p2p node which acts both as a client
    and a server
    """
    def __init__(self, logger, block_chain_db):
        """
        constructor
        """
        self.logger = logger
        self.block_chain_db = block_chain_db

        # find the node local address
        addresses = os.popen('IPCONFIG | FINDSTR /R '
                             '"Ethernet adapter Local '
                             'Area Connection .* Address.'
                             '*[0-9][0-9]*/.[0-9][0-9]*/.'
                             '[0-9][0-9]*/.[0-9][0-9]*"')
        first_eth_address = re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
                                      addresses.read()).group()
        # self.address = first_eth_address
        self.address = '127.0.0.1'

        # initialize the server
        self.server = NodeServer(self.logger)
        self.server_thread = threading.Thread(
            target=self.server.run)
        self.server_thread.start()

        # find known nodes
        self.known_nodes_db = KnownNodes(self.logger)
        self.known_nodes = self.known_nodes_db.extract_known_nodes()
        if self.address in self.known_nodes:
                self.known_nodes.remove(self.address)
        if len(self.known_nodes) == 0:
            hosts_db = HostNodes(self.logger)
            self.known_nodes = hosts_db.extract_hosts()
            if self.address in self.known_nodes:
                self.known_nodes.remove(self.address)
            for address in self.known_nodes:
                self.known_nodes_db.insert_address(address)
            hosts_db.close_connection()
        self.known_nodes_db.close_connection()
        self.client = NodeClient(self.logger, self.known_nodes)
        self.msg_handler = None
        self.to_close = False

    def update_chain(self):
        """
        the node updates its chain
        by getting the longest one from the
        network
        """
        self.logger.info('Searching for the updated chain')

        # updates the nodes of your current chain
        best_height = len(self.block_chain_db.chain)
        version = Version(best_height, self.address)
        if self.msg_handler is None:
            self.msg_handler = MessagesHandler(version, False)
        else:
            self.msg_handler.change_message(version, False)
        self.msg_handler.pack()
        self.client.send_to_all(self.msg_handler.message)

        # wait for responds to come
        time.sleep(WAITING_TIME)

        # finding the longest chain from
        # the other nodes
        responds = self.server.get_received_messages()
        network_best, holders = self.find_longest_chain(responds)
        # the holders list is a way to screen out nodes that
        # they are not synced or honest because they do not have
        # the longest chain
        if network_best != best_height:
            self.get_longest_chain(network_best, holders)
        self.logger.info('The chain is updated')

    def find_longest_chain(self, messages):
        """
        the function find the longest chain
        in the network
        :return: the holders of the
        longest chain and its length
        """
        best_height = len(self.block_chain_db.chain)
        holders = []
        for message_tup in messages:
            address = message_tup[1]
            message = message_tup[0]
            self.msg_handler.change_message(message, True)
            self.msg_handler.unpack_message()
            unpacked_message = self.msg_handler.message
            # the node does not handle any message
            # until it downloads the longest
            # block chain from the network
            if type(unpacked_message) is Version:
                self.msg_handler.message.address_from = address
                message_height = unpacked_message.best_height
                if message_height > best_height:
                    best_height = message_height
                    holders = [unpacked_message.address_from]
                    self.server.remove_message(message_tup)
                elif message_height == best_height:
                    holders.append(unpacked_message.address_from)
                    self.server.remove_message(message_tup)
        self.logger.info('The best height in the network is ' +
                         str(best_height))
        return best_height, holders

    def get_longest_chain(self, best_height, holders):
        """
        the function gets from the network the missing blocks
        from the longest chain
        :param best_height: the longest chain height
        :param holders: the addresses of the
        holders of the chain
        """
        self.logger.info('Receiving from the network the '
                         'longest chain')
        current_length = len(self.block_chain_db.chain)

        # loop until the node is holding the longest chain
        while current_length != best_height:
            # request blocks from the known nodes
            get_blocks_message = GetBlocks(self.address,
                                           self.block_chain_db.chain[current_length-1].hash_code)
            self.msg_handler.change_message(get_blocks_message, False)
            self.msg_handler.pack()
            for address in holders:
                self.client.send(self.msg_handler.message,
                                 address)

            # waiting for responds
            time.sleep(WAITING_TIME)

            # find the inv messages of blocks which indicate respond
            responds = self.server.get_received_messages()
            inv_responds = []
            for respond in responds:
                message = respond[0]
                address = respond[1]
                self.msg_handler.change_message(message, True)
                self.msg_handler.unpack_message()
                # check that the inv is matching to the demands
                if type(self.msg_handler.message) is not Error:
                    self.msg_handler.message.address_from = address
                if type(self.msg_handler.message) is Inv and \
                        self.msg_handler.message.data_type == 'block' and \
                        self.msg_handler.message.address_from in holders:
                    if best_height - current_length < MAX_HASHES_IN_INV:
                        if len(self.msg_handler.message.hash_codes) == \
                                best_height - current_length:
                            inv_responds.append(self.msg_handler.message)
                            self.server.remove_message(respond)
                    elif len(self.msg_handler.message.hash_codes) == \
                            MAX_HASHES_IN_INV:
                        inv_responds.append(self.msg_handler.message)
                        self.server.remove_message(respond)
            blocks_hashes = self.extract_blocks_hashes(inv_responds)
            downloaded_blocks = self.download_blocks(blocks_hashes)
            if downloaded_blocks is False:
                return False
            self.block_chain_db.\
                add_downloaded_blocks(downloaded_blocks)
            current_length = len(self.block_chain_db.chain)

    @staticmethod
    def extract_blocks_hashes(inv_messages):
        """
        the function extracts the block's
        hashes from the inv messages
        :param inv_messages: the inv messages that the server
        received
        :return: the block hashes to download
        """
        blocks_hashes_list = []

        # extract all hashes to a list of hashes_list
        for inv_message in inv_messages:
            # check that the hashes have proof of work
            is_proof_of_work = True
            for hash_code in inv_message.hash_codes:
                if hash_code[0:DIFFICULTY] != '0'*DIFFICULTY:
                    is_proof_of_work = False
                    break
            if is_proof_of_work:
                blocks_hashes_list.append(inv_message.hash_codes)

        # find the number of times every hash is
        # returning
        hashes_dict = {'max': 0}
        majority_hashes = ''
        for blocks_hashes in blocks_hashes_list:
            hash_code = ''
            for block_hash in blocks_hashes:
                hash_code += block_hash
            hash_code = SHA256.new(hash_code).hexdigest()
            if hash_code in hashes_dict:
                hashes_dict[hash_code] += 1
            else:
                hashes_dict[hash_code] = 1
            if hashes_dict[hash_code] > hashes_dict['max']:
                hashes_dict['max'] = hashes_dict[hash_code]
                majority_hashes = blocks_hashes

        # downloading the block hashes that the majority
        # of the network agrees on is a way to download the
        # honest chain and not every chain
        return majority_hashes

    def download_blocks(self, blocks_hashes):
        """
        the function downloads from other
        nodes the block blocks matching
        to the blocks hashes
        :param blocks_hashes: the blocks to
        download
        :returns: the downloaded blocks. the function
        returns False if there was a problem with downloading
        the blocks
        """
        downloaded_blocks = []
        """
        should done by sending to each peer
        a different block
        """
        for hash_code in blocks_hashes:
            is_found = False
            # request the block
            get_data_message = GetData(self.address,
                                       'block',
                                       hash_code)
            self.msg_handler.change_message(get_data_message, False)
            self.msg_handler.pack()
            self.client.send_to_all(self.msg_handler.message)

            # waiting for responds
            time.sleep(WAITING_TIME)

            responds = self.server.get_received_messages()
            blocks_responds = []

            # find the responds
            for respond in responds:
                message = respond[0]
                address = respond[1]
                self.msg_handler.change_message(message, True)
                self.msg_handler.unpack_message()
                if type(self.msg_handler.message) is BlockMessage:
                    self.msg_handler.message.address_from = address
                    blocks_responds.append(self.msg_handler.message)
                    self.server.remove_message(respond)

            for block_message in blocks_responds:
                if block_message.block.hash_code == hash_code:
                    is_found = True
                    if self.verify_block(block_message.block):
                        downloaded_blocks.append(block_message.block)
                        break
                    else:
                        return False

            if not is_found:
                return False

        last_block = self.block_chain_db.chain[-1]
        for block in downloaded_blocks:
            if block.prev != last_block.hash_code:
                return False

        self.logger.info('Finish downloading all blocks')
        return downloaded_blocks

    def handle_messages(self):
        """
        the function handles the messages
        that the node received
        """
        self.known_nodes_db = KnownNodes(self.logger)
        while not self.server.to_close:
            messages = self.server.get_received_messages()
            for message in messages:
                self.server.remove_message(message)
                message = message[0]
                address = message[1]
                self.msg_handler.change_message(message,
                                                True)
                self.msg_handler.unpack_message()
                if type(self.msg_handler.message) is Error:
                    self.logger.info('Wrong data received')
                else:
                    print address
                    self.msg_handler.message.address_from = address
                    print self.msg_handler.message.address_from
                    if self.msg_handler.message.address_from not in self.known_nodes:
                        self.known_nodes.append(self.msg_handler.message.address_from)
                        self.known_nodes_db.insert_address(
                            self.msg_handler.message.address_from)
                    if type(self.msg_handler.message) is Version:
                        self.handle_version(self.msg_handler.message)
                    elif type(self.msg_handler.message) is GetBlocks:
                        self.handle_get_blocks(self.msg_handler.message)
                    elif type(self.msg_handler.message) is Inv:
                        self.handle_inv(self.msg_handler.message)
                    elif type(self.msg_handler.message) is GetData:
                        self.handle_get_data(self.msg_handler.message)
                    elif type(self.msg_handler.message) is GetAddresses:
                        self.handle_get_addresses(self.msg_handler.message)

    def handle_version(self, version_message):
        """
        The function handles the version
        message.
        the protocol is build so the best height
        in the receiving version connection is must
        be lower or equals to your best height.
        The respond should be matching.
        :param version_message: the version message
        """
        self.logger.info('Handle version message from ' +
                         version_message.address_from)
        received_best_height = version_message.best_height
        best_height = len(self.block_chain_db.chain)
        if best_height > received_best_height:
            respond_version = Version(best_height, self.address)
            self.msg_handler.change_message(respond_version,
                                            False)
            self.msg_handler.pack()
            self.client.send(self.msg_handler.message,
                             version_message.address_from)

    def handle_get_blocks(self, get_blocks_message):
        """
        The function handles the get_blocks_message
        :param get_blocks_message: the get blocks message
        """
        self.logger.info('Handle get blocks message from ' +
                         get_blocks_message.address_from)
        hashes_to_send = []
        chain = self.block_chain_db.chain
        hashes = []
        for block in chain:
            hashes.append(block.hash_code)
        print get_blocks_message
        for hash_code in hashes[hashes.index(get_blocks_message.hash_code)+1:]:
            if len(hashes_to_send) == MAX_HASHES_IN_INV:
                break
            hashes_to_send.append(hash_code)
        inv_message = Inv(self.address, 'block', hashes_to_send)
        self.msg_handler.change_message(inv_message, False)
        self.msg_handler.pack()
        self.client.send(self.msg_handler.message,
                         get_blocks_message.address_from)

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
            responds = self.server.get_received_messages()
            for respond in responds:
                self.msg_handler.change_message(
                    respond, True)
                self.msg_handler.unpack_message()
                if type(self.msg_handler.message) is BlockMessage:
                    self.logger.info('Handle block message')
                    self.server.remove_message(respond)
                    if self.msg_handler.message.address_from == \
                            inv_message.address_from:
                        block = self.msg_handler.message.block
                        if block.hash_code == hash_code:
                            if self.verify_block(block):
                                self.logger.info('Received legal block')
                                self.block_chain_db.add_block(block)
                                for transaction in block.transactions:
                                    if transaction in self.block_chain_db.transactions_pool:
                                        self.block_chain_db.transactions_pool.remove(transaction)
                                # send the block to known nodes
                                self.msg_handler.change_message(Inv(self.address,
                                                                    'block',
                                                                    hash_code), False)
                                self.msg_handler.pack()
                                for address in self.known_nodes:
                                    if address != inv_message.address_from:
                                        self.client.send(self.msg_handler.message, address)
                            else:
                                self.logger.info('Received illegal block')
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
            responds = self.server.get_received_messages()

            # handle the responds
            for respond in responds:
                self.msg_handler.change_message(
                    respond, True)
                self.msg_handler.unpack_message()
                if type(self.msg_handler.message) is TransactionMessage:
                    self.logger.info('Handle transaction message')
                    self.server.remove_message(respond)
                    if self.msg_handler.message.address_from == \
                            inv_message.address_from:
                        transaction = self.msg_handler.message.transaction
                        if transaction.transaction_id == hash_code:
                            if self.verify_transaction(transaction):
                                self.logger.info('Received legal transaction')
                                self.block_chain_db.add_transaction(transaction)

                                # send the transaction to known nodes
                                self.msg_handler.change_message(Inv(self.address,
                                                                    'transaction',
                                                                    hash_code), False)
                                self.msg_handler.pack()
                                for address in self.known_nodes:
                                    if address != inv_message.address_from:
                                        self.client.send(self.msg_handler.message, address)
                            else:
                                self.logger.info('Received illegal transaction')
                            break

    def handle_get_data(self, get_data_message):
        """
        handles get data message
        :param get_data_message: the get data
        message
        """
        self.logger.info('Handle get data message from ' +
                         get_data_message.address_from)
        chain = self.block_chain_db.chain

        # sending the block as a respond
        if get_data_message.data_type == 'block':
            block_to_send = None
            for block in chain:
                if block.hash_code == get_data_message.hash_code:
                    block_to_send = block
                    break
            if block_to_send is not None:
                block_message = BlockMessage(self.address,
                                             block_to_send)
                self.msg_handler.change_message(block_message, False)
                self.msg_handler.pack()
                self.client.send(self.msg_handler.message,
                                 get_data_message.address_from)

        # sending the transaction as a respond
        elif get_data_message.data_type == 'transaction':
            transaction_to_send = None
            for transaction in self.block_chain_db.transactions_pool:
                if transaction.transaction_id == \
                        get_data_message.hash_code:
                    transaction_to_send = transaction
            if transaction_to_send is not None:
                transaction_message = TransactionMessage(self.address,
                                                         transaction_to_send)
                self.msg_handler.change_message(transaction_message, False)
                self.msg_handler.pack()
                self.client.send(self.msg_handler.message,
                                 get_data_message.address_from)

    def handle_get_addresses(self, get_addresses_message):
        """
        handles get addresses message
        :param get_addresses_message: the get addresses
        message
        """
        self.logger.info('Handle get addresses message from ' +
                         get_addresses_message.address_from)
        addresses_message = AddressesMessage(self.address,
                                             self.known_nodes)
        self.msg_handler.change_message(addresses_message, False)
        self.msg_handler.pack()
        self.client.send(self.msg_handler.message,
                         get_addresses_message.address_from)

    def find_connections(self):
        """
        The functions find connected nodes
        which the node can send messages to
        """
        get_addresses = GetAddresses(self.address)
        if self.msg_handler is None:
            self.msg_handler = MessagesHandler(get_addresses, False)
        else:
            self.msg_handler.change_message(get_addresses, False)
        self.msg_handler.pack()
        self.client.send_to_all(self.msg_handler.message)
        time.sleep(WAITING_TIME)

        responds = self.server.get_received_messages()
        for respond in responds:
            message = respond[0]
            address_from = respond[1]
            self.msg_handler.change_message(
                message, True)
            self.msg_handler.unpack_message()
            if type(self.msg_handler.message) is AddressesMessage:
                self.msg_handler.message.address_from = address_from
                addresses = self.msg_handler.message.addresses
                self.server.remove_message(respond)
                for address in addresses:
                    if address not in self.known_nodes and address != self.address:
                        self.known_nodes.append(address)
                        self.known_nodes_db.insert_address(address)

    def verify_transaction(self, transaction):
        """
        the function verify that the transaction
        is legal
        :param transaction: the transaction to verify
        :returns: true if the transaction is legal and false
        otherwise
        """
        are_legal_inputs, proved_value = \
            self.verify_transaction_inputs(transaction.inputs,
                                           transaction)
        if not are_legal_inputs:
            return False

        return self.verify_transaction_outputs(transaction.outputs,
                                               proved_value)

    def verify_block(self, block):
        """
        the function verify that the block
        is legal
        :param block: the block to verify
        :returns: true if the block is legal and false
        otherwise
        """
        # check that there are no
        # different transactions using the same input
        # and that there is only one coin base
        # transaction
        all_inputs = []
        found_coin_base = False

        for transaction in block.transactions:
            # check if coin base
            if transaction.inputs[0].output_index == -1:
                if found_coin_base:
                    return False
                found_coin_base = True
            else:
                for tx_input in transaction.inputs:
                    for out_input in all_inputs:
                        if out_input.transaction_id == tx_input.transaction_id\
                                and out_input.output_index == tx_input.output_index:
                            return False

        # validate the block
        if block.is_valid_proof():
            for transaction in block.transactions:
                if not self.verify_transaction(transaction):
                    return False
            return True
        return False

    def verify_transaction_inputs(self, inputs, transaction):
        """
        the function verifies the inputs in the
        transaction
        :param inputs: the list of the transaction inputs
        :param transaction: the transaction which the inputs belong
        to
        :returns: true if all the inputs are legal and the money
        that the inputs provide, false otherwise
        """
        used_outputs = []
        proved_value = 0
        for tx_input in inputs:
            used_output = [tx_input.transaction_id,
                           tx_input.output_index]

            if used_output[1] == -1:
                # coin base transaction
                if len(inputs) > 1:
                    return False, 0
                if len(transaction.outputs) > 1:
                    return False, 0
                proved_value = REWORD

            else:
                # check that the output exist
                is_found = False
                for block in self.block_chain_db.chain:
                    if not is_found:
                        for tx in block.transactions:
                            if tx.transaction_id == used_output[0] and \
                                    len(tx.outputs) > used_output[1]:
                                is_found = True
                                # add the actual output object to the list
                                used_output.append(
                                    tx.outputs[used_output[1]])
                                break
                if not is_found:
                    return False, 0

                for un_spent_output in used_outputs:
                    # check that the inputs do not use the same output
                    if used_output[0] == un_spent_output.transaction_id and \
                            used_output[1] == un_spent_output.output_index:
                        return False, 0
                    # check that the output is unspent
                    if not self.is_unspent_output(used_output[0],
                                                  used_output[1]):
                        return False, 0

                used_output = UnspentOutput(used_output[2],
                                            used_output[0],
                                            used_output[1])

                # verify the proof
                if not self.verify_proof(tx_input.proof,
                                         used_output,
                                         transaction):
                    return False, 0
                used_outputs.append(used_output)
                proved_value += used_output.output.value
        return True, proved_value

    @staticmethod
    def verify_transaction_outputs(outputs, proved_value):
        """
        the function verifies the outputs in the
        transaction
        :param outputs: the list of the transaction outputs
        :param proved_value: the value that is calculated in the
        inputs. The sum of all of the value in the outputs should
        be equal to this value
        :returns: true if all the outputs are legal,
        false otherwise
        """
        transaction_value = 0
        if len(outputs) > 2:
            return False
        for output in outputs:
            # check that the address is legal
            if len(output.address) != WALLET_ADDRESS_LENGTH:
                return False
            for char in output.address:
                if char not in HEX_DIGEST:
                    return False
            transaction_value += output.value

        # check the value
        if transaction_value != proved_value:
            return False
        return True

    def is_unspent_output(self, transaction_to_check, output_index):
        """
        the function checks if the given output
        was spent by going throw the block_chain
        :param transaction_to_check: a transaction that contains the
        output to check
        :param output_index: the index of the output
        inside the transaction
        :returns: false if the output was spent
        and true otherwise
        """
        # go throw all the inputs in the block chain
        # and checks weather they use the output
        for block in self.block_chain_db.chain:
            for transaction in block.transactions:
                for transaction_input in transaction.inputs:
                    if transaction_input.transaction_id == \
                            transaction_to_check.transaction_id:
                        if transaction_input.output_index == output_index:
                            return False
        return True

    @staticmethod
    def verify_proof(proof, un_spent_output, transaction):
        """
        the function verifies the proof
        :param proof: the proof to validate
        :param un_spent_output: the un spent output
        that the proof proves
        :param transaction: the transaction which the proof
        belongs to
        :return: true if all the proof is validated
        and false otherwise
        """
        # verify the proof address
        public_key = proof[1]
        wallet_address = Wallet.find_address(public_key)
        if not wallet_address == un_spent_output.output.address:
            return False

        # verify the proof signature
        signature = proof[0]
        signed_data = un_spent_output.transaction_id
        signed_data += transaction.outputs[0].address
        signed_data = CryptoSet.hash(signed_data).hexdigest()
        signed_data += str(transaction.outputs[0].value)
        signed_data = CryptoSet.hash(signed_data)
        return CryptoSet.verify(signed_data, signature, public_key)

    def distribute_transaction(self, transaction):
        """
        the function distributes the transaction
        to known nodes
        """
        inv = Inv(self.address, 'transaction',
                  [transaction.transaction_id])
        self.msg_handler.change_message(inv, False)
        self.msg_handler.pack()
        self.client.send_to_all(self.msg_handler.message)

    def close_node(self):
        """
        the function closes connection of the node
        """
        self.server.to_close = True
        self.block_chain_db.close_connection()


if __name__ == '__main__':
    logger = Logging('test').logger
    db = BlockChainDB(logger)
    node = Node(logger, db)
    node.find_connections()
    node.update_chain()
    b1 = Block(1, db.chain[-1].hash_code, [])
    b1.mine_block()
    b2 = Block(2, db.chain[-1].hash_code, [])
    b2.mine_block()
    db.add_downloaded_blocks([b1, b2])
    thread = threading.Thread(target=node.handle_messages)
    thread.start()
