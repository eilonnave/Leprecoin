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
    GetData
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
        best_height = len(self.wallet.block_chain_db.chain)
        version = Version(best_height, self.address)
        self.msg_handler = MessagesHandler(version, False)
        self.msg_handler.pack()
        self.client.send_to_all(self.msg_handler.message)
        # wait fo responds to come
        time.sleep(2)
        responds = self.server.received
        network_best, holders = self.find_longest_chain(responds)
        if network_best != best_height:
            self.get_longest_chain(best_height, holders)

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
                if message_height == best_height:
                    holders.append(message.address_from)
            self.server.received.remove(message)
        return best_height, holders

    def get_longest_chain(self, best_height, holders):
        """
        the function gets from the network the longest chain
        :param best_height: the longest chain height
        :param holders: the addresses of the
        holders of the chain
        """
        current_length = len(self.wallet.block_chain_db.chain)
        get_blocks_message = GetBlocks(self.address, current_length)
        self.msg_handler.change_message(get_blocks_message, False)
        self.msg_handler.pack()
        while current_length != best_height:
            for address in holders:
                self.client.send(self.msg_handler.message,
                                 address)
            time.sleep(1)
            responds = self.server.received
            inv_responds = []
            for respond in responds:
                self.msg_handler.change_message(responds, True)
                self.msg_handler.unpack_message()
                if type(self.msg_handler.message) is Inv:
                    inv_responds.append(respond)
                self.server.received.remove(respond)
            blocks_hashes = self.extract_blocks_hashes(inv_responds)

    def extract_blocks_hashes(self, inv_messages):
        """
        the function extracts the block's
        hashes from the inv messages
        :param inv_messages: the inv messages that the server
        received
        :return: the block hashes for the
        inv messages
        """
        blocks_hashes = []
        for message in inv_messages:
            self.msg_handler.change_message(message,
                                            True)
            self.msg_handler.unpack_message()
            inv = self.msg_handler.message
            if inv.data_type == 'block':
                blocks_hashes.append(inv.hash_codes)
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
        downloded_blocks = []
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



