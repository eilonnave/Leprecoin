# -*- coding: utf-8 -*-
import getip
import threading
import time
from node_server import NodeServer
from node_client import NodeClient
from messages import MessagesHandler, \
    Version, \
    GetBlocks, \
    Inv, \
    GetData, \
    BlockMessage, \
    TransactionMessage
KNOWN_NODES = ['127.0.0.1']


class Node:
    """
    p2p node which acts both as a client
    and a server
    """
    def __init__(self, logger, wallet):
        """
        constructor
        """
        self.logger = logger
        self.address = getip.get()
        self.server = NodeServer(logger)
        self.known_nodes = KNOWN_NODES
        self.client = NodeClient(logger, self.known_nodes)
        self.msg_handler = None
        self.wallet = wallet
        self.server_thread = threading.Thread(target=self.server.run)
        self.server_thread.start()

    def update_chain(self):
        """
        the node updates its chain
        by getting the longest one from the
        network
        """
        self.logger.info('Searching for the updated chain')

        # updates the nodes of your current chain
        best_height = len(self.wallet.block_chain_db.chain)
        version = Version(best_height, self.address)
        self.msg_handler = MessagesHandler(version, False)
        self.msg_handler.pack()
        self.client.send_to_all(self.msg_handler.message)
        # wait fo responds to come
        time.sleep(2)

        # finding the longest chain from
        # the other nodes
        responds = self.server.get_received_messages()
        network_best, holders = self.find_longest_chain(responds)
        if network_best != best_height:
            self.get_longest_chain(best_height, holders)
        self.logger.info('The chain is updated')

    def find_longest_chain(self, messages):
        """
        the function find the longest chain
        in the network
        :return: the holders of the
        longest chain and its length
        """
        best_height = len(self.wallet.block_chain_db.chain)
        holders = []
        for message in messages:
            self.msg_handler.change_message(message, True)
            self.msg_handler.unpack_message()
            message = self.msg_handler.message
            # the node does not handle any message
            # until it downloads the longest
            # block chain from the network
            if type(message) is Version:
                message_height = message.best_height
                if message_height > best_height:
                    best_height = message_height
                    holders = [message.address_from]
                    self.server.remove_message(message)
                if message_height == best_height:
                    holders.append(message.address_from)
                    self.server.remove_message(message)
        self.logger.info('the best height in the network is '+
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
        current_length = len(self.wallet.block_chain_db.chain)
        while current_length != best_height:
            get_blocks_message = GetBlocks(self.address, current_length)
            self.msg_handler.change_message(get_blocks_message, False)
            self.msg_handler.pack()
            for address in holders:
                self.client.send(self.msg_handler.message,
                                 address)
            time.sleep(1)
            responds = self.server.get_received_messages()
            inv_responds = []
            for respond in responds:
                self.msg_handler.change_message(responds, True)
                self.msg_handler.unpack_message()
                if type(self.msg_handler.message) is Inv:
                    inv_responds.append(self.msg_handler.message)
                    self.server.remove_message(respond)
            blocks_hashes = self.extract_blocks_hashes(inv_responds)
            downloaded_blocks = self.download_blocks(blocks_hashes)
            self.wallet.block_chain_db.\
                add_downloaded_blocks(downloaded_blocks)
            current_length = len(self.wallet.block_chain_db.chain)

    @staticmethod
    def extract_blocks_hashes(inv_messages):
        """
        the function extracts the block's
        hashes from the inv messages
        :param inv_messages: the inv messages that the server
        received
        :return: the block hashes for the
        inv messages
        """
        blocks_hashes = []
        for inv_message in inv_messages:
            if inv_message.data_type == 'block':
                blocks_hashes.append(inv_messages.hash_codes)
        """
        find the block that the majority of the
        network agrees on
        """
        return blocks_hashes[0]

    def download_blocks(self, blocks_hashes):
        """
        the function downloads from other
        nodes the block blocks matching
        to the blocks hashes
        :param blocks_hashes: the blocks to
        download
        :return: the downloaded blocks
        """
        downloaded_blocks = []
        """
        should done by sending to each peer
        a different block
        """
        for hash_code in blocks_hashes:
            get_data_message = GetData(self.address,
                                       'block',
                                       hash_code)
            self.client.send_to_all(get_data_message)
            time.sleep(2)
            responds = self.server.get_received_messages()
            blocks_responds = []
            for respond in responds:
                self.msg_handler.change_message(respond, True)
                self.msg_handler.unpack_message()
                if type(self.msg_handler.message) is BlockMessage:
                    blocks_responds.append(self.msg_handler.message)
                    self.server.remove_message(respond)
            for block_message in blocks_responds:
                if block_message.block.hash_code == hash_code:
                    downloaded_blocks.append(block_message.block)
                    break
        self.logger.info('Finish downloading all blocks')
        return downloaded_blocks

    def handle_messages(self):
        """
        the function handles the messages
        that the node received
        """
        messages = self.server.get_received_messages()
        for message in messages:
            self.msg_handler.change_message(message,
                                            True)
            self.msg_handler.unpack_message()
            if type(self.msg_handler.message) is Version:
                self.handle_version(self.msg_handler.message)
            elif type(self.msg_handler.message) is GetBlocks:
                self.handle_get_blocks(self.msg_handler.message)
            elif type(self.msg_handler.message) is Inv:
                self.handle_inv(self.msg_handler.message)
            elif type(self.msg_handler.message) is GetData:
                self.handle_get_data(self.msg_handler.message)

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
        self.logger.info('handle version message from ' +
                         version_message.address_from)
        received_best_height = version_message.best_height
        best_height = len(self.wallet.block_chain_db.chain)
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
        self.logger.info('handle get blocks message from ' +
                         get_blocks_message.address_from)
        hashes_to_send = []
        chain = self.wallet.block_chain_db.chain
        for block in chain[chain.index(get_blocks_message.hash_code)+1:]:
            if len(hashes_to_send) == 500:
                break
            hashes_to_send.append(block.hash_code)
        inv_message = Inv(self.address, 'block', hashes_to_send)
        self.msg_handler.change_message(inv_message, False)
        self.msg_handler.pack()
        self.client.send(self.msg_handler.message,
                         get_blocks_message.address_from)

    def handle_inv(self, inv_message):
        """
        handles inv message.
        according to the protocol the inv message
        to handle must contain transactions
        :param inv_message: the inv message
        """
        pass

    def handle_get_data(self, get_data_message):
        """
        handles get data message
        :param get_data_message: the get data
        message
        """
        self.logger.info('handle get data message from ' +
                         get_data_message.address_from)
        chain = self.wallet.block_chain_db.chain
        if get_data_message.type == 'block':
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