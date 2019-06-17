#  -*- coding: utf-8 -*-
import Tkinter as Tk
from GUI.global_graphic import *
from GUI.send_gui import SendWindow
from GUI.wallet_main_gui import WalletMainWindow
from GUI.waiting_gui import WaitingForMiningWindow
from GUI.transactions_gui import TransactionsWindow
from GUI.loading_gui import LoadingWindow
from core_code.wallet import Wallet
from Crypto.PublicKey import RSA
from core_code.logger import Logging
from core_code.database import BlockChainDB
from core_code.node import Node
import pickle
import os
import threading

GENERATE_NUMBER = 2048
PRIVATE_KEY_FILE = 'private_key.txt'


class UiRunner:
    def __init__(self):
        """
        constructor
        """
        self.loggers = [Logging('wallet').logger,
                        Logging('network').logger,
                        Logging('block_chain').logger]
        self.block_chain_db = BlockChainDB(self.loggers[2])
        self.root = None
        self.current_window = None
        self.node = Node(self.loggers[1],
                         self.block_chain_db)
        self.win_dict = {NEXT_KEY: None,
                         MAIN_KEY: WalletMainWindow,
                         SEND_KEY: SendWindow,
                         TRANSACTIONS_KEY: TransactionsWindow,
                         WAITING_KEY: WaitingForMiningWindow,
                         LOADING_KEY: LoadingWindow}
        self.wallet = None

    def run(self):
        """
        Runs the user interface
        """
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
        self.root = Tk.Tk()
        self.current_window = LoadingWindow(self.root,
                                            self.win_dict,
                                            self.wallet)
        loading_thread = threading.Thread(target=self.sync)
        loading_thread.start()
        self.root.mainloop()
        while self.win_dict[NEXT_KEY] is not None:
            self.root = Tk.Tk()
            self.current_window = self.win_dict[NEXT_KEY](self.root,
                                                          self.win_dict,
                                                          self.wallet)
            self.root.mainloop()
            if type(self.current_window) is SendWindow:
                transaction = self.current_window.transaction
                if transaction is not None:
                    self.block_chain_db.add_transaction(transaction)
                    self.node.distribute_transaction(transaction)

        # handle exiting form the system

    def sync(self):
        """
        the function syncs the node
        """
        self.win_dict[NEXT_KEY] = None
        self.node.find_connections()
        self.node.update_chain()
        self.win_dict[NEXT_KEY] = self.win_dict[MAIN_KEY]


if __name__ == '__main__':
    UiRunner().run()

