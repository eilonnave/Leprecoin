#  -*- coding: utf-8 -*-
import tkinter as tk
from GUI.SendGui import SendWindow
from GUI.WalletGui import WalletMainWindow
from core_code.wallet import Wallet


class UiRunner:
    def __init__(self):
        self.root = tk.Tk()
        self.current_window = WalletMainWindow(self.root)

    def run(self):
        self.root.mainloop()
        self.root = tk.Tk()
        self.current_window = SendWindow(self.root)
        self.root.mainloop()


if __name__ == '__main__':
    UiRunner().run()
