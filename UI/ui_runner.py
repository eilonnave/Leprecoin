#  -*- coding: utf-8 -*-
import Tkinter as Tk
from GUI.global_graphic import *
from GUI.send_gui import SendWindow
from GUI.wallet_main_gui import WalletMainWindow
from GUI.mining_gui import MiningWindow
from GUI.transactions_gui import TransactionsWindow
from core_code.wallet import Wallet
from Crypto.PublicKey import RSA
from core_code.logger import Logging
from core_code.database import BlockChainDB
from core_code.node import Node
import pickle
import os

GENERATE_NUMBER = 2048
PRIVATE_KEY_FILE = 'private_key.txt'

# ToDo: add loading windows
# ToDo: add error labels to windows


class UiRunner:
    def __init__(self):
        """
        constructor
        """
        self.loggers = [Logging('wallet').logger,
                        Logging('network').logger,
                        Logging('block_chain').logger]
        self.block_chain_db = BlockChainDB(self.loggers[2],
                                           'tests.db')
        self.root = None
        self.current_window = None
        self.node = Node(self.loggers[1],
                         self.block_chain_db)
        self.win_dict = {NEXT_KEY: None,
                         MAIN_KEY: WalletMainWindow,
                         SEND_KEY: SendWindow,
                         MINE_KEY: MiningWindow,
                         TRANSACTIONS_KEY: TransactionsWindow}
        self.wallet = None

    def run(self):
        """
        Runs the user interface
        """
        # open private key file for the address
        if os.path.isfile(PRIVATE_KEY_FILE):
            with open(PRIVATE_KEY_FILE, 'rb') as private_key_file:
                private_key = pickle.load(private_key_file)
                private_key = RSA.import_key(private_key)
        else:
            with open(PRIVATE_KEY_FILE, 'wb') as private_key_file:
                private_key = RSA.generate(GENERATE_NUMBER)
                pickle.dump(private_key.export_key(),
                            private_key_file)
        self.wallet = Wallet(private_key,
                             self.block_chain_db,
                             self.loggers[0])
        self.node.update_chain()
        self.win_dict[NEXT_KEY] = WalletMainWindow
        while self.win_dict[NEXT_KEY] is not None:
            self.root = Tk.Tk()
            self.current_window = self.win_dict[NEXT_KEY](self.root,
                                                          self.win_dict,
                                                          self.wallet)
            self.root.mainloop()

        # handle exiting form the system
        pass


if __name__ == '__main__':
    l1 = Logging('test in another port')
    n1 = Node(l1, BlockChainDB('test.db'))
    n1.handle_messages()
    UiRunner().run()

