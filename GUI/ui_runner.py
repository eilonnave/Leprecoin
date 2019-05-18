#  -*- coding: utf-8 -*-
import Tkinter as Tk
from SendGui import SendWindow
from WalletGui import WalletMainWindow, \
    SEND_KEY, \
    NEXT_KEY, \
    MINE_KEY, \
    MAIN_KEY
from MiningGui import MiningWindow
from core_code.wallet import Wallet
from Crypto.PublicKey import RSA
from core_code.logger import Logging
from core_code.database import BlockChainDB


GENERATE_NUMBER = 2048


class UiRunner:
    def __init__(self, private_key, logger, block_chain_db):
        self.logger = logger
        self.block_chain_db = block_chain_db
        self.root = None
        self.current_window = None
        self.win_dict = {NEXT_KEY: None,
                         MAIN_KEY: WalletMainWindow,
                         SEND_KEY: SendWindow,
                         MINE_KEY: MiningWindow}
        self.wallet = Wallet(private_key, self.block_chain_db, self.logger)
        self.wallet.update_transactions()
        self.wallet.update_balance()

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

