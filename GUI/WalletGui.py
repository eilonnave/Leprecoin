# - * - coding: utf - 8 -
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True


def vp_start_gui():
    """Starting point when module is the main routine."""
    global val, w, root
    root = tk.Tk()
    top = WalletMainWindow(root)
    root.mainloop()

w = None


def create_top_level1(root, *args, **kwargs):
    """Starting point when module is imported by another program."""
    global w, w_win, rt
    rt = root
    w = tk.Toplevel (root)
    top = Toplevel1 (w)
    WalletGui_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Toplevel1():
    global w
    w.destroy()
    w = None


class WalletMainWindow:
    def __init__(self, top):
        """
        constructor
        """
        # X11 color: 'gray85'
        _bg_color = '#d9d9d9'
        # X11 color: 'black'
        _fg_color = '#000000'
        # X11 color: 'gray85'
        _comp_color = '#d9d9d9'
        # X11 color: 'gray85'
        _ana1_color = '#d9d9d9'
        # Closest X11 color: 'gray92'
        _ana2_color = '#ececec'

        # configure the top level screen
        top.geometry("800x450+291+113")
        top.title("Wallet Main Window")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")
        self.top = top

        self.buttons_frame = None
        self.send_button = None
        self.request_button = None
        self.leprecoin_label = None
        self.mining_button = None
        self.transactions_button = None
        self.create_buttons_frame()

        self.Frame2 = tk.Frame(top)
        self.Frame2.place(relx=0.0, rely=0.067, relheight=0.933, relwidth=0.625)
        self.Frame2.configure(relief='flat')
        self.Frame2.configure(borderwidth="-1")
        self.Frame2.configure(background="#2f4f4f")
        self.Frame2.configure(highlightbackground="#d9d9d9")
        self.Frame2.configure(highlightcolor="black")
        self.Frame2.configure(width=395)

        self.Label2 = tk.Label(self.Frame2)
        self.Label2.place(relx=0.0, rely=0.0, height=40, width=200)
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(activeforeground="black")
        self.Label2.configure(background="dark slate grey")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(font="-family {Lucida Calligraphy} -size 14")
        self.Label2.configure(foreground="Gold")
        self.Label2.configure(highlightbackground="#d9d9d9")
        self.Label2.configure(highlightcolor="black")
        self.Label2.configure(text='''Last Tranactions''')

        self.Text1 = tk.Text(self.Frame2)
        self.Text1.place(relx=0.03, rely=0.095, relheight=0.833, relwidth=0.9)
        self.Text1.configure(background="dark slate grey")
        self.Text1.configure(borderwidth="2")
        self.Text1.configure(font="-family {Lucida Calligraphy} -size 10")
        self.Text1.configure(foreground="old lace")
        self.Text1.configure(highlightbackground="#d9d9d9")
        self.Text1.configure(highlightcolor="black")
        self.Text1.configure(insertbackground="black")
        self.Text1.configure(selectbackground="#c4c4c4")
        self.Text1.configure(selectforeground="black")
        self.Text1.configure(width=10)
        self.Text1.configure(wrap="word")

        self.Frame3 = tk.Frame(top)
        self.Frame3.place(relx=0.625, rely=0.067, relheight=0.467
                , relwidth=0.375)
        self.Frame3.configure(relief='flat')
        self.Frame3.configure(borderwidth="-1")
        self.Frame3.configure(background="dark slate gray")
        self.Frame3.configure(highlightbackground="#d9d9d9")
        self.Frame3.configure(highlightcolor="black")
        self.Frame3.configure(width=125)

        self.Label3 = tk.Label(self.Frame3)
        self.Label3.place(relx=0.0, rely=0.0, height=40, width=200)
        self.Label3.configure(activebackground="#f9f9f9")
        self.Label3.configure(activeforeground="black")
        self.Label3.configure(anchor='w')
        self.Label3.configure(background="dark slate grey")
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(font="-family {Lucida Calligraphy} -size 14")
        self.Label3.configure(foreground="Gold")
        self.Label3.configure(highlightbackground="#d9d9d9")
        self.Label3.configure(highlightcolor="black")
        self.Label3.configure(text='''Current Balance''')

        self.Text2 = tk.Text(self.Frame3)
        self.Text2.place(relx=0.0, rely=0.19, relheight=0.238, relwidth=0.9)
        self.Text2.configure(background="dark slate grey")
        self.Text2.configure(borderwidth="0")
        self.Text2.configure(font="-family {Lucida Calligraphy} -size 20")
        self.Text2.configure(foreground="old lace")
        self.Text2.configure(highlightbackground="#d9d9d9")
        self.Text2.configure(highlightcolor="black")
        self.Text2.configure(insertbackground="black")
        self.Text2.configure(selectbackground="#c4c4c4")
        self.Text2.configure(selectforeground="black")
        self.Text2.configure(width=10)
        self.Text2.configure(wrap="word")

        self.Frame4 = tk.Frame(top)
        self.Frame4.place(relx=0.625, rely=0.533, relheight=0.467
                , relwidth=0.375)
        self.Frame4.configure(relief='flat')
        self.Frame4.configure(borderwidth="-1")
        self.Frame4.configure(background="dark slate grey")
        self.Frame4.configure(highlightbackground="#d9d9d9")
        self.Frame4.configure(highlightcolor="black")
        self.Frame4.configure(width=125)

        self.Label4 = tk.Label(self.Frame4)
        self.Label4.place(relx=0.0, rely=0.0, height=40, width=200)
        self.Label4.configure(activebackground="#f9f9f9")
        self.Label4.configure(activeforeground="black")
        self.Label4.configure(anchor='w')
        self.Label4.configure(background="dark slate grey")
        self.Label4.configure(disabledforeground="#a3a3a3")
        self.Label4.configure(font="-family {Lucida Calligraphy} -size 14")
        self.Label4.configure(foreground="Gold")
        self.Label4.configure(highlightbackground="#d9d9d9")
        self.Label4.configure(highlightcolor="black")
        self.Label4.configure(text='''Your Address''')

        self.Text3 = tk.Text(self.Frame4)
        self.Text3.place(relx=0.0, rely=0.19, relheight=0.238, relwidth=0.9)
        self.Text3.configure(background="dark slate gray")
        self.Text3.configure(borderwidth="0")
        self.Text3.configure(font="-family {Lucida Calligraphy} -size 16")
        self.Text3.configure(foreground="old lace")
        self.Text3.configure(highlightbackground="#d9d9d9")
        self.Text3.configure(highlightcolor="black")
        self.Text3.configure(insertbackground="black")
        self.Text3.configure(selectbackground="#c4c4c4")
        self.Text3.configure(selectforeground="black")
        self.Text3.configure(width=10)
        self.Text3.configure(wrap="word")

    def create_buttons_frame(self):
        """
        the function creates the buttons frame
        for the gui
        """
        # creates the frame
        self.buttons_frame = tk.Frame(self.top)
        self.buttons_frame.place(relx=0.0, rely=0.0, relheight=0.067, relwidth=1.0)
        self.buttons_frame.configure(relief='flat')
        self.buttons_frame.configure(borderwidth="-1")
        self.buttons_frame.configure(background="saddle brown")
        self.buttons_frame.configure(highlightbackground="#d9d9d9")
        self.buttons_frame.configure(highlightcolor="black")
        self.buttons_frame.configure(width=125)

        # create the send button
        self.send_button = tk.Button(self.buttons_frame)
        self.send_button.place(relx=0.731, rely=0.0, height=30, width=100)
        self.send_button.configure(activebackground="#ececec")
        self.send_button.configure(activeforeground="#000000")
        self.send_button.configure(background="Gold")
        self.send_button.configure(disabledforeground="#a3a3a3")
        self.send_button.configure(font="-family {Calisto MT} -size 12 -slant italic")
        self.send_button.configure(foreground="#000000")
        self.send_button.configure(highlightbackground="#d9d9d9")
        self.send_button.configure(highlightcolor="black")
        self.send_button.configure(pady="0")
        self.send_button.configure(text='''Send coins''')

        # creates the request button
        self.request_button = tk.Button(self.buttons_frame)
        self.request_button.place(relx=0.875, rely=0.0, height=30, width=100)
        self.request_button.configure(activebackground="#ececec")
        self.request_button.configure(activeforeground="#000000")
        self.request_button.configure(background="Gold")
        self.request_button.configure(disabledforeground="#a3a3a3")
        self.request_button.configure(font="-family {Calisto MT} -size 12 -slant italic")
        self.request_button.configure(foreground="#000000")
        self.request_button.configure(highlightbackground="#d9d9d9")
        self.request_button.configure(highlightcolor="black")
        self.request_button.configure(pady="0")
        self.request_button.configure(text='''Request coins''')

        # creates the leprecoin label
        self.leprecoin_label = tk.Label(self.buttons_frame)
        self.leprecoin_label.place(relx=0.0, rely=0.0, height=30, width=150)
        self.leprecoin_label.configure(activebackground="#f9f9f9")
        self.leprecoin_label.configure(activeforeground="black")
        self.leprecoin_label.configure(background="saddle brown")
        self.leprecoin_label.configure(disabledforeground="#a3a3a3")
        self.leprecoin_label.configure(font="-family {Old English Text MT} -size 20")
        self.leprecoin_label.configure(foreground="Gold")
        self.leprecoin_label.configure(highlightbackground="#d9d9d9")
        self.leprecoin_label.configure(highlightcolor="black")
        self.leprecoin_label.configure(text='''Leprecoin''')

        # creates the mining button
        self.mining_button = tk.Button(self.buttons_frame)
        self.mining_button.place(relx=0.588, rely=0.0, height=30, width=100)
        self.mining_button.configure(activebackground="#ececec")
        self.mining_button.configure(activeforeground="#000000")
        self.mining_button.configure(background="Gold")
        self.mining_button.configure(disabledforeground="#a3a3a3")
        self.mining_button.configure(font="-family {Calisto MT} -size 12 -slant italic")
        self.mining_button.configure(foreground="#000000")
        self.mining_button.configure(highlightbackground="#d9d9d9")
        self.mining_button.configure(highlightcolor="black")
        self.mining_button.configure(pady="0")
        self.mining_button.configure(text='''Try mining''')

        # create the transactions button
        self.transactions_button = tk.Button(self.buttons_frame)
        self.transactions_button.place(relx=0.444, rely=0.0, height=30, width=100)
        self.transactions_button.configure(activebackground="#ececec")
        self.transactions_button.configure(activeforeground="#000000")
        self.transactions_button.configure(background="gold")
        self.transactions_button.configure(disabledforeground="#a3a3a3")
        self.transactions_button.configure(font="-family {Calisto MT} -size 12 -slant italic")
        self.transactions_button.configure(foreground="#000000")
        self.transactions_button.configure(highlightbackground="#d9d9d9")
        self.transactions_button.configure(highlightcolor="black")
        self.transactions_button.configure(pady="0")
        self.transactions_button.configure(text='''Transactions''')

    def create_last_transactions_frame(self):
        """
        the function creates the last transactions
        frame for the gui
        """
        self.last_frame = tk.Frame(self.top)
        self.last_frame.place(relx=0.0, rely=0.067, relheight=0.933, relwidth=0.625)
        self.last_frame.configure(relief='flat')
        self.last_frame.configure(borderwidth="-1")
        self.last_frame.configure(background="#2f4f4f")
        self.last_frame.configure(highlightbackground="#d9d9d9")
        self.last_frame.configure(highlightcolor="black")
        self.last_frame.configure(width=395)

        self.Label2 = tk.Label(self.Frame2)
        self.Label2.place(relx=0.0, rely=0.0, height=40, width=200)
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(activeforeground="black")
        self.Label2.configure(background="dark slate grey")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(font="-family {Lucida Calligraphy} -size 14")
        self.Label2.configure(foreground="Gold")
        self.Label2.configure(highlightbackground="#d9d9d9")
        self.Label2.configure(highlightcolor="black")
        self.Label2.configure(text='''Last Tranactions''')

        self.Text1 = tk.Text(self.Frame2)
        self.Text1.place(relx=0.03, rely=0.095, relheight=0.833, relwidth=0.9)
        self.Text1.configure(background="dark slate grey")
        self.Text1.configure(borderwidth="2")
        self.Text1.configure(font="-family {Lucida Calligraphy} -size 10")
        self.Text1.configure(foreground="old lace")
        self.Text1.configure(highlightbackground="#d9d9d9")
        self.Text1.configure(highlightcolor="black")
        self.Text1.configure(insertbackground="black")
        self.Text1.configure(selectbackground="#c4c4c4")
        self.Text1.configure(selectforeground="black")
        self.Text1.configure(width=10)
        self.Text1.configure(wrap="word")

if __name__ == '__main__':
    vp_start_gui()





