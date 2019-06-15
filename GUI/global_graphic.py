WIN_WIDTH = 800
WIN_HEIGHT = 450
LINE_DOWN = '\n'
NEXT_KEY = 'next'
MAIN_KEY = 'main'
SEND_KEY = 'send'
MINE_KEY = 'mine'
TRANSACTIONS_KEY = 'transactions'
WAITING_KEY = 'waiting'


class GuiWindow(object):
    def __init__(self, top, win_dict, wallet):
        self.win_dict = win_dict
        self.win_dict[NEXT_KEY] = None
        self.wallet = wallet
        self.top = top

        # configure the top level screen
        self.set_window_geometry()
        self.top.configure(background="#d9d9d9")
        self.top.configure(highlightbackground="#d9d9d9")
        self.top.configure(highlightcolor="black")
        self.top.resizable(False, False)

    def set_window_geometry(self):
        """
        the functions calculate and config the
        geometry string that determent the top size
        and place
        """
        x = str(int(self.top.winfo_screenwidth() / 2) - int(WIN_WIDTH / 2))
        y = str(int(self.top.winfo_screenheight() / 2) - int(WIN_HEIGHT / 2))
        self.top.geometry(
            str(WIN_WIDTH) +
            "x" +
            str(WIN_HEIGHT)
            + "+" + x + "+" + y)

    def transaction_to_string(self, transaction):
        """
        the function extracts the transaction data
        from the transaction and returns the string
        so the gui can insert it to a widget
        :param transaction: the transaction to show
        :returns: a string of the transaction's data
        """
        s = ''
        output = transaction.outputs[0]

        # check if coin base transaction
        if transaction.inputs[0].proof[1] is '':
            s += '+' \
                 + str(output.value) \
                 + ' LPC' \
                 + LINE_DOWN \
                 + 'By mining' \
                 + LINE_DOWN * 2

        # check if the wallet got paid
        elif output.address == self.wallet.address:
            sender = self.wallet.find_address(
                transaction.inputs[0].proof[1])
            s += '+' \
                 + str(output.value) \
                 + ' LPC' \
                 + LINE_DOWN \
                 + 'From: ' \
                 + sender + LINE_DOWN * 2

        else:
            # the wallet paid
            # the first output is the payment
            # if there is another then it is the change
            s += '-' \
                 + str(output.value) \
                 + ' LPC' \
                 + LINE_DOWN \
                 + 'To: ' + output.address + LINE_DOWN * 2
        return s
