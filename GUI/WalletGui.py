# - * - coding: utf - 8 -
import tkinter as tk
WIN_WIDTH = 800
WIN_HEIGHT = 450


def vp_start_gui():
    """Starting point when module is the main routine."""
    global root
    root = tk.Tk()
    WalletMainWindow(root)
    root.mainloop()


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
        x = str(int(top.winfo_screenwidth()/2)-int(WIN_WIDTH/2))
        y = str(int(top.winfo_screenheight()/2)-int(WIN_HEIGHT/2))
        top.geometry(str(WIN_WIDTH)+"x"+str(WIN_HEIGHT)+"+"+x+"+"+y)
        top.title("Wallet Main Window")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")
        top.resizable(False, False)
        self.top = top

        self.buttons_frame = None
        self.send_button = None
        self.request_button = None
        self.leprecoin_label = None
        self.mining_button = None
        self.transactions_button = None
        self.create_buttons_frame()

        self.last_frame = None
        self.last_label = None
        self.last_text = None
        self.create_last_transactions_frame()

        self.balance_frame = None
        self.balance_label = None
        self.balance_text = None
        self.create_balance_frame()

        self.address_frame = None
        self.address_label = None
        self.address_text = None
        self.create_address_frame()

    def create_buttons_frame(self):
        """
        the function creates the buttons frame
        for the gui
        """
        # creates the frame
        self.buttons_frame = tk.Frame(self.top)
        self.buttons_frame.place(relx=0.0,
                                 rely=0.0,
                                 relheight=0.067,
                                 relwidth=1.0)
        self.buttons_frame.configure(relief='flat')
        self.buttons_frame.configure(borderwidth="-1")
        self.buttons_frame.configure(background="saddle brown")
        self.buttons_frame.configure(highlightbackground="#d9d9d9")
        self.buttons_frame.configure(highlightcolor="black")
        self.buttons_frame.configure(width=125)

        # create the send button
        self.send_button = tk.Button(self.buttons_frame)
        self.send_button.place(relx=0.731,
                               rely=0.0,
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
        self.send_button.configure(text='''Send coins''')
        self.send_button.configure(command=self.pressed_send)

        # creates the request button
        self.request_button = tk.Button(self.buttons_frame)
        self.request_button.place(relx=0.875,
                                  rely=0.0,
                                  height=30,
                                  width=100)
        self.request_button.configure(activebackground="#ececec")
        self.request_button.configure(activeforeground="#000000")
        self.request_button.configure(background="Gold")
        self.request_button.configure(disabledforeground="#a3a3a3")
        self.request_button.configure(
            font="-family {Calisto MT} -size 12 -slant italic")
        self.request_button.configure(foreground="#000000")
        self.request_button.configure(highlightbackground="#d9d9d9")
        self.request_button.configure(highlightcolor="black")
        self.request_button.configure(pady="0")
        self.request_button.configure(text='''Request coins''')

        # creates the leprecoin label
        self.leprecoin_label = tk.Label(self.buttons_frame)
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

        # creates the mining button
        self.mining_button = tk.Button(self.buttons_frame)
        self.mining_button.place(relx=0.588,
                                 rely=0.0,
                                 height=30,
                                 width=100)
        self.mining_button.configure(activebackground="#ececec")
        self.mining_button.configure(activeforeground="#000000")
        self.mining_button.configure(background="Gold")
        self.mining_button.configure(disabledforeground="#a3a3a3")
        self.mining_button.configure(
            font="-family {Calisto MT} -size 12 -slant italic")
        self.mining_button.configure(foreground="#000000")
        self.mining_button.configure(highlightbackground="#d9d9d9")
        self.mining_button.configure(highlightcolor="black")
        self.mining_button.configure(pady="0")
        self.mining_button.configure(text='''Try mining''')
        self.mining_button.configure(command=self.pressed_mining)

        # create the transactions button
        self.transactions_button = tk.Button(self.buttons_frame)
        self.transactions_button.place(relx=0.444,
                                       rely=0.0,
                                       height=30,
                                       width=100)
        self.transactions_button.configure(activebackground="#ececec")
        self.transactions_button.configure(activeforeground="#000000")
        self.transactions_button.configure(background="gold")
        self.transactions_button.configure(disabledforeground="#a3a3a3")
        self.transactions_button.configure(
            font="-family {Calisto MT} -size 12 -slant italic")
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
        # creates the last transactions frame
        self.last_frame = tk.Frame(self.top)
        self.last_frame.place(relx=0.0,
                              rely=0.067,
                              relheight=0.933,
                              relwidth=0.625)
        self.last_frame.configure(relief='flat')
        self.last_frame.configure(borderwidth="-1")
        self.last_frame.configure(background="#2f4f4f")
        self.last_frame.configure(highlightbackground="#d9d9d9")
        self.last_frame.configure(highlightcolor="black")
        self.last_frame.configure(width=395)

        # creates the lats transactions label
        self.last_label = tk.Label(self.last_frame)
        self.last_label.place(relx=0.0, rely=0.0, height=40, width=200)
        self.last_label.configure(activebackground="#f9f9f9")
        self.last_label.configure(activeforeground="black")
        self.last_label.configure(background="dark slate grey")
        self.last_label.configure(disabledforeground="#a3a3a3")
        self.last_label.configure(font="-family {Lucida Calligraphy} -size 14")
        self.last_label.configure(foreground="Gold")
        self.last_label.configure(highlightbackground="#d9d9d9")
        self.last_label.configure(highlightcolor="black")
        self.last_label.configure(text='''Last Tranactions''')

        # creates the last transactions text
        self.last_text = tk.Text(self.last_frame)
        self.last_text.place(relx=0.03,
                             rely=0.095,
                             relheight=0.833,
                             relwidth=0.9)
        self.last_text.configure(background="dark slate grey")
        self.last_text.configure(borderwidth="2")
        self.last_text.configure(
            font="-family {Lucida Calligraphy} -size 10")
        self.last_text.configure(foreground="old lace")
        self.last_text.configure(highlightbackground="#d9d9d9")
        self.last_text.configure(highlightcolor="black")
        self.last_text.configure(insertbackground="black")
        self.last_text.configure(selectbackground="#c4c4c4")
        self.last_text.configure(selectforeground="black")
        self.last_text.configure(width=10)
        self.last_text.configure(wrap="word")

    def create_balance_frame(self):
        """
        the function creates the balance
        frame for the gui
        """
        self.balance_frame = tk.Frame(self.top)
        self.balance_frame.place(relx=0.625,
                                 rely=0.067,
                                 relheight=0.467,
                                 relwidth=0.375)
        self.balance_frame.configure(relief='flat')
        self.balance_frame.configure(borderwidth="-1")
        self.balance_frame.configure(background="dark slate gray")
        self.balance_frame.configure(highlightbackground="#d9d9d9")
        self.balance_frame.configure(highlightcolor="black")
        self.balance_frame.configure(width=125)

        self.balance_label = tk.Label(self.balance_frame)
        self.balance_label.place(relx=0.0,
                                 rely=0.0,
                                 height=40,
                                 width=200)
        self.balance_label.configure(activebackground="#f9f9f9")
        self.balance_label.configure(activeforeground="black")
        self.balance_label.configure(anchor='w')
        self.balance_label.configure(background="dark slate grey")
        self.balance_label.configure(disabledforeground="#a3a3a3")
        self.balance_label.configure(
            font="-family {Lucida Calligraphy} -size 14")
        self.balance_label.configure(foreground="Gold")
        self.balance_label.configure(highlightbackground="#d9d9d9")
        self.balance_label.configure(highlightcolor="black")
        self.balance_label.configure(text='''Current Balance''')

        self.balance_text = tk.Text(self.balance_frame)
        self.balance_text.place(relx=0.0,
                                rely=0.19,
                                relheight=0.238,
                                relwidth=0.9)
        self.balance_text.configure(background="dark slate grey")
        self.balance_text.configure(borderwidth="0")
        self.balance_text.configure(
            font="-family {Lucida Calligraphy} -size 20")
        self.balance_text.configure(foreground="old lace")
        self.balance_text.configure(highlightbackground="#d9d9d9")
        self.balance_text.configure(highlightcolor="black")
        self.balance_text.configure(insertbackground="black")
        self.balance_text.configure(selectbackground="#c4c4c4")
        self.balance_text.configure(selectforeground="black")
        self.balance_text.configure(width=10)
        self.balance_text.configure(wrap="word")

    def create_address_frame(self):
        """
        the function creates the address
        frame for the gui
        """
        self.address_frame = tk.Frame(self.top)
        self.address_frame.place(relx=0.625,
                                 rely=0.533,
                                 relheight=0.467,
                                 relwidth=0.375)
        self.address_frame.configure(relief='flat')
        self.address_frame.configure(borderwidth="-1")
        self.address_frame.configure(background="dark slate grey")
        self.address_frame.configure(highlightbackground="#d9d9d9")
        self.address_frame.configure(highlightcolor="black")
        self.address_frame.configure(width=125)

        self.address_label = tk.Label(self.address_frame)
        self.address_label.place(relx=0.0,
                                 rely=0.0,
                                 height=40,
                                 width=200)
        self.address_label.configure(activebackground="#f9f9f9")
        self.address_label.configure(activeforeground="black")
        self.address_label.configure(anchor='w')
        self.address_label.configure(background="dark slate grey")
        self.address_label.configure(disabledforeground="#a3a3a3")
        self.address_label.configure(
            font="-family {Lucida Calligraphy} -size 14")
        self.address_label.configure(foreground="Gold")
        self.address_label.configure(highlightbackground="#d9d9d9")
        self.address_label.configure(highlightcolor="black")
        self.address_label.configure(text='''Your Address''')

        self.address_text = tk.Text(self.address_frame)
        self.address_text.place(relx=0.0,
                                rely=0.19,
                                relheight=0.238,
                                relwidth=0.9)
        self.address_text.configure(background="dark slate gray")
        self.address_text.configure(borderwidth="0")
        self.address_text.configure(
            font="-family {Lucida Calligraphy} -size 16")
        self.address_text.configure(foreground="old lace")
        self.address_text.configure(highlightbackground="#d9d9d9")
        self.address_text.configure(highlightcolor="black")
        self.address_text.configure(insertbackground="black")
        self.address_text.configure(selectbackground="#c4c4c4")
        self.address_text.configure(selectforeground="black")
        self.address_text.configure(width=10)
        self.address_text.configure(wrap="word")

    def pressed_send(self):
        """
        the function handles the press on
        the send button
        """
        self.top.destroy()

    def pressed_mining(self):
        """
        the function handles the press
        on the mining button
        """
        self.top.destroy()


if __name__ == '__main__':
    vp_start_gui()
