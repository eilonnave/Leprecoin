#  -*- coding: utf-8 -*-
import Tkinter as Tk
from PIL import ImageTk
from core_code.blockchain import REWORD
from core_code.miner import Miner
import time
from global_graphic import *


PIC_PATH = 'Leprechaun_with_Beer_PNG_Clipart.png'


class MiningWindow:
    def __init__(self, top, win_dict, wallet):
        """
        constructor
        """
        # configure the top level screen
        # set_window_geometry(top)
        top.title("Mining Window")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")
        top.resizable(False, False)
        self.top = top
        self.top.after(500, self.execute_mining)
        self.win_dict = win_dict
        self.win_dict[NEXT_KEY] = None
        self.wallet = wallet

        self.buttons_frame = None
        self.leprecoin_label = None
        self.cancel_button = None
        self.create_buttons_frame()

        self.mining_frame = None
        self.mining_label = None
        self.leprechaun_label = None
        self.success_label = None
        self.fail_label = None
        self.create_mining_frame()

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

        self.cancel_button = Tk.Button(self.buttons_frame)
        self.cancel_button.place(relx=0.813,
                                 rely=0.0,
                                 height=30,
                                 width=100)
        self.cancel_button.configure(activebackground="#ececec")
        self.cancel_button.configure(activeforeground="#000000")
        self.cancel_button.configure(background="Gold")
        self.cancel_button.configure(disabledforeground="#a3a3a3")
        self.cancel_button.configure(
            font="-family {Calisto MT} -size 12 -slant italic")
        self.cancel_button.configure(foreground="black")
        self.cancel_button.configure(highlightbackground="#d9d9d9")
        self.cancel_button.configure(highlightcolor="black")
        self.cancel_button.configure(pady="0")
        self.cancel_button.configure(text='''Cancel''')
        self.cancel_button.configure(command=self.pressed_cancel)

    def create_mining_frame(self):
        """
        the function creates the mining frame
        for the gui
        """
        self.mining_frame = Tk.Frame(self.top)
        self.mining_frame.place(relx=0.0,
                                rely=0.067,
                                relheight=0.933,
                                relwidth=1.0)
        self.mining_frame.configure(relief='groove')
        self.mining_frame.configure(borderwidth="2")
        self.mining_frame.configure(relief="groove")
        self.mining_frame.configure(background="dark slate gray")
        self.mining_frame.configure(width=125)

        self.mining_label = Tk.Label(self.mining_frame)
        self.mining_label.place(relx=0.156,
                                rely=0.286,
                                height=164,
                                width=200)
        self.mining_label.configure(background="#2f4f4f")
        self.mining_label.configure(disabledforeground="#a3a3a3")
        self.mining_label.configure(
            font="-family {Lucida Calligraphy} -size 18")
        self.mining_label.configure(foreground="Gold")
        self.mining_label.configure(text='''Mining is \nunder progress''')

        pic = ImageTk.PhotoImage(file=PIC_PATH)
        self.leprechaun_label = Tk.Label(self.mining_frame, image=pic)
        self.leprecoin_label.image = pic
        self.leprechaun_label.configure(background="dark slate grey")
        self.leprechaun_label.configure(disabledforeground="#a3a3a3")
        self.leprechaun_label.configure(foreground="#000000")
        self.leprechaun_label.place(relx=0.594,
                                    rely=0.286,
                                    height=164,
                                    width=200)

        self.success_label = Tk.Label(self.mining_frame)
        self.success_label.configure(background="#2f4f4f")
        self.success_label.configure(disabledforeground="#a3a3a3")
        self.success_label.configure(
            font="-family {Lucida Calligraphy} -size 18")
        self.success_label.configure(foreground="Gold")
        self.success_label.configure(
            text='success in mining\nreward: \n'+str(REWORD)+' LPC')

        self.fail_label = Tk.Label(self.mining_frame)
        self.fail_label.configure(background="#2f4f4f")
        self.fail_label.configure(disabledforeground="#a3a3a3")
        self.fail_label.configure(
            font="-family {Lucida Calligraphy} -size 18")
        self.fail_label.configure(foreground="Gold")
        self.fail_label.configure(
            text='failed mining')

    def pressed_cancel(self):
        """
        the function handles the press
        on the send button
        """
        self.win_dict[NEXT_KEY] = MAIN_KEY
        self.top.destroy()

    def execute_mining(self):
        """
        the function executes the mining
        """
        miner = Miner(self.wallet)
        miner.mine()
        self.mining_label.destroy()
        self.success_label.place(relx=0.156,
                                 rely=0.286,
                                 height=164,
                                 width=250)
        self.top.update()
        time.sleep(4)
        self.win_dict[NEXT_KEY] = self.win_dict[MAIN_KEY]
        self.top.destroy()
