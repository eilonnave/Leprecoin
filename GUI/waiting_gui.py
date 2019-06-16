#  -*- coding: utf-8 -*-
import Tkinter as Tk
from PIL import ImageTk
from global_graphic import *


PIC_PATH = 'D:\Leprecoin\GUI\pics/Leprechaun_with_Beer_PNG_Clipart.png'
SECONDS_TO_WAIT = 300


class WaitingForMiningWindow(GuiWindow):
    def __init__(self, top, win_dict, wallet):
        """
        constructor
        """
        self.started_length = len(wallet.transactions)
        super(WaitingForMiningWindow, self).__init__(top,
                                                     win_dict,
                                                     wallet)
        self.top.title("Waiting Window")
        self.finished = False

        self.buttons_frame = None
        self.leprecoin_label = None
        self.back_button = None
        self.create_buttons_frame()

        self.waiting_frame = None
        self.waiting_label = None
        self.leprechaun_label = None
        self.fail_label = None
        self.create_waiting_frame()
        self.top.after(1000,
                       self.check_for_transaction,
                       0)

    def create_buttons_frame(self):
        """
        the function creates the buttons frame
        for the gui
        """
        self.buttons_frame = Tk.Frame(self.top)
        self.buttons_frame.place(relx=0.0,
                                 rely=0.0,
                                 relheight=0.067,
                                 relwidth=1.0)
        self.buttons_frame.configure(relief='flat')
        self.buttons_frame.configure(borderwidth="2")
        self.buttons_frame.configure(background="saddle brown")
        self.buttons_frame.configure(highlightbackground="#d9d9d9")
        self.buttons_frame.configure(highlightcolor="black")
        self.buttons_frame.configure(width=125)

        self.leprecoin_label = Tk.Label(self.buttons_frame)
        self.leprecoin_label.place(relx=0.0,
                                   rely=0.0,
                                   height=30,
                                   width=150)
        self.leprecoin_label.configure(activebackground="#f9f9f9")
        self.leprecoin_label.configure(activeforeground="black")
        self.leprecoin_label.configure(background="saddle brown")
        self.leprecoin_label.configure(disabledforeground="#a3a3a3")
        self.leprecoin_label.configure(
            font="-family {Old English Text MT} -size 20")
        self.leprecoin_label.configure(foreground="Gold")
        self.leprecoin_label.configure(highlightbackground="#d9d9d9")
        self.leprecoin_label.configure(highlightcolor="black")
        self.leprecoin_label.configure(text='''Leprecoin''')

    def create_waiting_frame(self):
        """
        the function creates the waiting frame
        for the gui
        """
        self.waiting_frame = Tk.Frame(self.top)
        self.waiting_frame.place(relx=0.0,
                                 rely=0.067,
                                 relheight=0.933,
                                 relwidth=1.0)
        self.waiting_frame.configure(relief='groove')
        self.waiting_frame.configure(borderwidth="2")
        self.waiting_frame.configure(relief="groove")
        self.waiting_frame.configure(background="dark slate gray")
        self.waiting_frame.configure(width=125)

        pic = ImageTk.PhotoImage(file=PIC_PATH)
        self.leprechaun_label = Tk.Label(self.waiting_frame, image=pic)
        self.leprecoin_label.image = pic
        self.leprechaun_label.configure(background="dark slate grey")
        self.leprechaun_label.configure(disabledforeground="#a3a3a3")
        self.leprechaun_label.configure(foreground="#000000")
        self.leprechaun_label.place(relx=0.594,
                                    rely=0.286,
                                    height=164,
                                    width=200)

        self.waiting_label = Tk.Label(self.waiting_frame)
        self.waiting_label.configure(background="#2f4f4f")
        self.waiting_label.configure(disabledforeground="#a3a3a3")
        self.waiting_label.configure(
            font="-family {Lucida Calligraphy} -size 18")
        self.waiting_label.configure(foreground="Gold")
        self.waiting_label.configure(
            text='Waiting for a miner')
        self.waiting_label.place(relx=0.156,
                                 rely=0.286,
                                 height=164,
                                 width=300)

        self.fail_label = Tk.Label(self.waiting_frame)
        self.fail_label.configure(background="#2f4f4f")
        self.fail_label.configure(disabledforeground="#a3a3a3")
        self.fail_label.configure(
            font="-family {Lucida Calligraphy} -size 18")
        self.fail_label.configure(foreground="Gold")
        self.fail_label.configure(
            text='It seems that \nthere is no miner\n '
                 'try again later')

    def failed_mining(self):
        """
        the function handles the fact
        that there is no miner
        """
        self.waiting_label.destroy()
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
        self.fail_label.place(relx=0.156,
                              rely=0.286,
                              height=164,
                              width=250)
        self.top.update()

    def pressed_back(self):
        """
        the function handles the press
        on the back button
        """
        self.win_dict[NEXT_KEY] = self.win_dict[MAIN_KEY]
        self.top.destroy()

    def check_for_transaction(self, times):
        """
        the function checks if the transaction
        the the user waiting for
        was inserted to the block chain
        to the
        :return:
        """
        print times
        if times > SECONDS_TO_WAIT:
            self.failed_mining()
        elif len(self.wallet.transactions) > self.started_length:
            for transaction in self.wallet.transactions[self.started_length:]:
                if self.wallet.equals_public_keys(transaction.inputs[0].proof[1]):
                    self.win_dict[NEXT_KEY] = self.win_dict[MAIN_KEY]
                    self.top.destroy()
        else:
            self.top.after(1000,
                           self.check_for_transaction,
                           times+1)

