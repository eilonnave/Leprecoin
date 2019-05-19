#  -*- coding: utf-8 -*-
import Tkinter as Tk
from global_graphic import *


ADDRESS_LENGTH = 40
HEX_DIGEST = '0123456789abcdef'


class SendWindow:
    def __init__(self, top, win_dict, wallet):
        """
        constructor
        """
        self.win_dict = win_dict
        self.win_dict[NEXT_KEY] = None
        self.wallet = wallet

        # configure the top level screen
        # set_window_geometry(top)
        top.title("Send Window")
        top.configure(background="#d9d9d9")
        top.resizable(False, False)
        self.top = top

        self.send_frame = None
        self.send_label = None
        self.amount_label = None
        self.send_entry = None
        self.amount_entry = None
        self.send_button = None
        self.create_send_frame()

        self.buttons_frame = None
        self.leprecoin_label = None
        self.back_button = None
        self.create_buttons_frame()

    def create_send_frame(self):
        """
        the function creates the send frame
        for the gui
        """
        self.send_frame = Tk.Frame(self.top)
        self.send_frame.place(relx=0.0,
                              rely=0.067,
                              relheight=1.0,
                              relwidth=1.0)
        self.send_frame.configure(relief='flat')
        self.send_frame.configure(borderwidth="2")
        self.send_frame.configure(background="dark slate grey")
        self.send_frame.configure(width=125)

        self.send_label = Tk.Label(self.send_frame)
        self.send_label.place(relx=0.25,
                              rely=0.244,
                              height=30,
                              width=100)
        self.send_label.configure(background="dark slate grey")
        self.send_label.configure(disabledforeground="#a3a3a3")
        self.send_label.configure(
            font="-family {Lucida Calligraphy} -size 14")
        self.send_label.configure(foreground="Gold")
        self.send_label.configure(text='''Send to''')

        self.amount_label = Tk.Label(self.send_frame)
        self.amount_label.place(relx=0.25,
                                rely=0.444,
                                height=30,
                                width=100)
        self.amount_label.configure(background="dark slate grey")
        self.amount_label.configure(disabledforeground="#a3a3a3")
        self.amount_label.configure(
            font="-family {Lucida Calligraphy} -size 14")
        self.amount_label.configure(foreground="gold")
        self.amount_label.configure(text='''Amount''')

        self.send_entry = Tk.Entry(self.send_frame)
        self.send_entry.place(relx=0.5,
                              rely=0.244,
                              height=30,
                              relwidth=0.313)
        self.send_entry.configure(background="#d9d9d9")
        self.send_entry.configure(disabledforeground="#a3a3a3")
        self.send_entry.configure(
            font="-family {Courier New} -size 10")
        self.send_entry.configure(foreground="#000000")
        self.send_entry.configure(insertbackground="black")

        self.amount_entry = Tk.Entry(self.send_frame)
        self.amount_entry.place(relx=0.5,
                                rely=0.444,
                                height=30,
                                relwidth=0.313)
        self.amount_entry.configure(background="#d9d9d9")
        self.amount_entry.configure(disabledforeground="#a3a3a3")
        self.amount_entry.configure(
            font="-family {Courier New} -size 10")
        self.amount_entry.configure(foreground="#000000")
        self.amount_entry.configure(highlightbackground="#d9d9d9")
        self.amount_entry.configure(highlightcolor="black")
        self.amount_entry.configure(insertbackground="black")
        self.amount_entry.configure(selectbackground="#c4c4c4")
        self.amount_entry.configure(selectforeground="black")

        self.send_button = Tk.Button(self.send_frame)
        self.send_button.place(relx=0.813,
                               rely=0.756,
                               height=30,
                               width=100)
        self.send_button.configure(activebackground="#ececec")
        self.send_button.configure(activeforeground="#000000")
        self.send_button.configure(background="Gold")
        self.send_button.configure(disabledforeground="#a3a3a3")
        self.send_button.configure(
            font="-family {Calisto MT} -size 12 -slant italic")
        self.send_button.configure(foreground="#000000")
        self.send_button.configure(highlightbackground="#d9d9d9")
        self.send_button.configure(highlightcolor="black")
        self.send_button.configure(pady="0")
        self.send_button.configure(text='''Send''')
        self.send_button.configure(command=self.pressed_send)

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

    def pressed_back(self):
        """
        the function handles the press
        on the back button
        """
        self.win_dict[NEXT_KEY] = self.win_dict[MAIN_KEY]
        self.top.destroy()

    def pressed_send(self):
        """
        the function handles the press
        on the send button
        """
        address = self.send_entry.get()
        legal = True
        for char in address:
            if char not in HEX_DIGEST:
                legal = False
                break
        if len(address) != ADDRESS_LENGTH:
            legal = False
        if address == self.wallet.address:
            legal = False
        amount = self.amount_entry.get()
        if not amount.isdigit():
            legal = False
        else:
            amount = int(amount)
        if legal:
            self.wallet.create_transaction(amount, address)





