import Tkinter as Tk
from PIL import ImageTk
from global_graphic import *


PIC_PATH = 'D:\Leprecoin\GUI\pics/Leprechaun_with_Beer_PNG_Clipart.png'


class LoadingWindow(GuiWindow):
    def __init__(self, top, win_dict, wallet):
        """
        constructor
        """
        self.started_length = len(wallet.transactions)
        super(LoadingWindow, self).__init__(top,
                                            win_dict,
                                            wallet)
        self.top.title("Loading Window")
        self.finished = False

        self.buttons_frame = None
        self.leprecoin_label = None
        self.create_buttons_frame()

        self.loading_frame = None
        self.loading_label = None
        self.leprechaun_label = None
        self.create_loading_frame()

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

    def create_loading_frame(self):
        """
        the function creates the waiting frame
        for the gui
        """
        self.loading_frame = Tk.Frame(self.top)
        self.loading_frame.place(relx=0.0,
                                 rely=0.067,
                                 relheight=0.933,
                                 relwidth=1.0)
        self.loading_frame.configure(relief='groove')
        self.loading_frame.configure(borderwidth="2")
        self.loading_frame.configure(relief="groove")
        self.loading_frame.configure(background="dark slate gray")
        self.loading_frame.configure(width=125)

        self.loading_label = Tk.Label(self.loading_frame)
        self.loading_label.place(relx=0.156, rely=0.286, height=164, width=200)
        self.loading_label.configure(background="#2f4f4f")
        self.loading_label.configure(disabledforeground="#a3a3a3")
        self.loading_label.configure(
            font="-family {Lucida Calligraphy} -size 18")
        self.loading_label.configure(foreground="Gold")
        self.loading_label.configure(text='''Loading...''')

        pic = ImageTk.PhotoImage(file=PIC_PATH)
        self.leprechaun_label = Tk.Label(self.loading_frame, image=pic)
        self.leprecoin_label.image = pic
        self.leprechaun_label.configure(background="dark slate grey")
        self.leprechaun_label.configure(disabledforeground="#a3a3a3")
        self.leprechaun_label.configure(foreground="#000000")
        self.leprechaun_label.place(relx=0.594,
                                    rely=0.286,
                                    height=164,
                                    width=200)

    def stopped_loading(self):
        """
        the function closes the window
        """
        self.win_dict[NEXT_KEY] = self.win_dict[MAIN_KEY]
        self.top.destroy()
