#  -*- coding: utf-8 -*-

import Tkinter as Tk
import ScrolledText
from PIL import ImageTk
from global_graphic import *
import os

PIC_PATH = 'leprechaun_transactions.png'
PIC_DIR = 'GUI/pics'


class TransactionsWindow(GuiWindow):
    def __init__(self, top, win_dict, wallet):
        """
        constructor
        """
        super(TransactionsWindow, self).__init__(top,
                                                 win_dict,
                                                 wallet)
        top.title("Transactions Window")

        self.buttons_frame = None
        self.leprecoin_label = None
        self.back_button = None
        self.create_buttons_frame()

        self.transactions_frame = None
        self.transactions_text = None
        self.pic_label = None
        self.create_transactions_frame()
        self.wallet.update_transactions()
        self.current_length = len(self.wallet.block_chain_db.chain)
        self.top.after(500, self.update_window)
        self.show_transactions()

    def create_buttons_frame(self):
        """
        the function creates the buttons
        frame for the gui
        """
        self.buttons_frame = Tk.Frame(self.top)
        self.buttons_frame.place(relx=0.0,
                                 rely=0.0,
                                 relheight=0.067,
                                 relwidth=1.0)
        self.buttons_frame.configure(relief='flat')
        self.buttons_frame.configure(borderwidth="2")
        self.buttons_frame.configure(background="saddle brown")
        self.buttons_frame.configure(width=125)

        self.leprecoin_label = Tk.Label(self.buttons_frame)
        self.leprecoin_label.place(relx=0.0,
                                   rely=0.0,
                                   height=30,
                                   width=150)
        self.leprecoin_label.configure(background="saddle brown")
        self.leprecoin_label.configure(disabledforeground="#a3a3a3")
        self.leprecoin_label.configure(
            font="-family {Old English Text MT} -size 20")
        self.leprecoin_label.configure(foreground="Gold")
        self.leprecoin_label.configure(text='''Leprecoin''')

        self.back_button = Tk.Button(self.buttons_frame)
        self.back_button.place(relx=0.813,
                               rely=0.0,
                               height=30,
                               width=100)
        self.back_button.configure(activebackground="#ececec")
        self.back_button.configure(activeforeground="#000000")
        self.back_button.configure(background="Gold")
        self.back_button.configure(disabledforeground="#a3a3a3")
        self.back_button.configure(
            font="-family {Calisto MT} -size 12 -slant italic")
        self.back_button.configure(foreground="#000000")
        self.back_button.configure(highlightbackground="#d9d9d9")
        self.back_button.configure(highlightcolor="black")
        self.back_button.configure(pady="0")
        self.back_button.configure(text='''Back''')
        self.back_button.configure(command=self.pressed_back)

    def create_transactions_frame(self):
        """
        the function creates the transactions
        frame for the gui
        """
        self.transactions_frame = Tk.Frame(self.top)
        self.transactions_frame.place(relx=0.0,
                                      rely=0.067,
                                      relheight=0.933,
                                      relwidth=1.0)
        self.transactions_frame.configure(relief='flat')
        self.transactions_frame.configure(borderwidth="2")
        self.transactions_frame.configure(background="dark slate grey")
        self.transactions_frame.configure(width=125)

        self.transactions_text = ScrolledText.\
            ScrolledText(self.transactions_frame)
        self.transactions_text.place(relx=0.063,
                                     rely=0.119,
                                     relheight=0.7,
                                     relwidth=0.5)
        self.transactions_text.configure(background="white")
        self.transactions_text.configure(font="TkTextFont")
        self.transactions_text.configure(foreground="black")
        self.transactions_text.configure(
            highlightbackground="#d9d9d9")
        self.transactions_text.configure(highlightcolor="black")
        self.transactions_text.configure(insertbackground="black")
        self.transactions_text.configure(insertborderwidth="3")
        self.transactions_text.configure(selectbackground="#c4c4c4")
        self.transactions_text.configure(selectforeground="black")
        self.transactions_text.configure(width=10)
        self.transactions_text.configure(wrap="none")
        self.show_transactions()

        default_cwd = os.getcwd()
        parent_path = os.path.dirname(default_cwd)
        if not os.path.isdir(parent_path+'/'+PIC_DIR):
            os.mkdir(parent_path+'/'+PIC_DIR)
        os.chdir(parent_path+'/'+PIC_DIR)
        pic = ImageTk.PhotoImage(file=PIC_PATH)
        self.pic_label = Tk.Label(self.transactions_frame,
                                  image=pic)
        self.pic_label.image = pic
        self.pic_label.place(relx=0.65,
                             rely=0.119,
                             height=294,
                             width=217)
        self.pic_label.configure(background="#d9d9d9")
        self.pic_label.configure(disabledforeground="#a3a3a3")
        self.pic_label.configure(foreground="#000000")
        os.chdir(default_cwd)

    def pressed_back(self):
        """
        the function handles the press
        on the back button
        """
        self.win_dict[NEXT_KEY] = self.win_dict[MAIN_KEY]
        self.top.destroy()

    def show_transactions(self):
        """
        the function shows the transactions
        on the window
        """
        s = ''
        if len(self.wallet.transactions) != 0:
            for transaction in self.wallet.transactions[::-1]:
                s += self.transaction_to_string(transaction)
        self.transactions_text.configure(state=Tk.NORMAL)
        self.transactions_text.delete(1.0, Tk.END)
        self.transactions_text.insert(Tk.END, s)
        self.transactions_text.configure(state=Tk.DISABLED)

    def update_window(self):
        """
        the functions update the window
        """
        if len(self.wallet.block_chain_db.chain) > self.current_length:
            self.wallet.update_transactions()
            self.show_transactions()
            self.current_length = len(self.wallet.block_chain_db.chain)
        self.top.after(500, self.update_window)




