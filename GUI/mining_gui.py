#  -*- coding: utf-8 -*-
import Tkinter as Tk
from PIL import ImageTk
from core_code.blockchain import REWORD
from core_code.miner import Miner
from global_graphic import *


PIC_PATH = 'C:\Leprecoin\GUI\pics/Leprechaun_with_Beer_PNG_Clipart.png'


class MiningWindow(GuiWindow):
    def __init__(self, top, win_dict, wallet):
        """
        constructor
        """
        super(MiningWindow, self).__init__(top,
                                           win_dict,
                                           wallet)
        self.top.title("Loading Window")
        self.finished = False

        self.buttons_frame = None
        self.leprecoin_label = None
        self.back_button = None
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
        self.mining_label.configure(text='''Loading...''')

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
            text='Waiting for a miner')
        self.success_label.place(relx=0.156,
                              rely=0.286,
                              height=164,
                              width=300)

        self.fail_label = Tk.Label(self.mining_frame)
        self.fail_label.configure(background="#2f4f4f")
        self.fail_label.configure(disabledforeground="#a3a3a3")
        self.fail_label.configure(
            font="-family {Lucida Calligraphy} -size 18")
        self.fail_label.configure(foreground="Gold")
        self.fail_label.configure(
            text='It seems that \nthere is no miner')

    def failed_mining(self):
        """
        the function handles the fact
        that a miner won the user
        """
        self.success_label.destroy()
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
        self.mining_label.destroy()
        self.fail_label.place(relx=0.156,
                              rely=0.286,
                              height=164,
                              width=250)
        self.top.update()
