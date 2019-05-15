# -*- coding: utf-8 -*-
from pyp2p import *
import time


def main():
    #Setup Alice's p2p node.
    alice = Net(passive_bind="192.168.0.45", passive_port=44444, interface="eth0:2", node_type="passive", debug=1)
    alice.start()
    alice.bootstrap()
    alice.advertise()

    #Event loop.
    while 1:
        for con in alice:
            for reply in con:
                print(reply)

    time.sleep(1)

    #Setup Bob's p2p node.
    bob = net.Net(passive_bind="192.168.0.44", passive_port=44445, interface="eth0:1", node_type="passive", debug=1)
    bob.start()
    bob.bootstrap()
    bob.advertise()

    #Event loop.
    while 1:
        for con in bob:
            con.send_line("test")

        time.sleep(1)


if __name__ == '__main__':
    main()