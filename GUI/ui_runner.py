#  -*- coding: utf-8 -*-
import tkinter as tk
from GUI.SendGui import SendWindow
from GUI.WalletGui import WalletMainWindow
from core_code.wallet import Wallet
from core_code.logger import Logging
from core_code.database import BlockChainDB


class UiRunner:
    def __init__(self, wallet):
        self.logger = Logging('user').logger
        self.block_chain_db = BlockChainDB(self.logger, 'test1.db')
        self.root = None
        self.current_window = None
        self.win_dict = {'main': WalletMainWindow,
                         'send': SendWindow}
        # self.wallet = Wallet(private_key, self.block_chain_db, self.logger)
        self.wallet = wallet
        self.wallet.update_transactions()
        self.wallet.update_balance()

    def run(self):
        next_win = [WalletMainWindow]
        while next_win[0] is not None:
            self.root = tk.Tk()
            self.current_window = next_win[0](self.root,
                                              next_win,
                                              self.win_dict,
                                              self.wallet)
            self.root.mainloop()


if __name__ == '__main__':
    UiRunner().run()
