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


GENERATE_NUMBER = 2048


class UiRunner:
    def __init__(self, private_key):
        self.loggers = [Logging('wallet').logger,
                        Logging('network').logger,
                        Logging('block_chain').logger]
        self.block_chain_db = BlockChainDB(self.loggers[2])
        self.root = None
        self.current_window = None
        self.node = Node
        self.win_dict = {NEXT_KEY: None,
                         MAIN_KEY: WalletMainWindow,
                         SEND_KEY: SendWindow,
                         MINE_KEY: MiningWindow,
                         TRANSACTIONS_KEY: TransactionsWindow}
        self.wallet = Wallet(private_key, self.block_chain_db, self.loggers[0])

    def run(self):
        self.win_dict[NEXT_KEY] = WalletMainWindow
        while self.win_dict[NEXT_KEY] is not None:
            self.root = Tk.Tk()
            self.current_window = self.win_dict[NEXT_KEY](self.root,
                                                          self.win_dict,
                                                          self.wallet)
            self.root.mainloop()


if __name__ == '__main__':
    p_k = RSA.generate(GENERATE_NUMBER)
    log = Logging('user').logger
    db = BlockChainDB(log)
    UiRunner(p_k, log, db).run()

