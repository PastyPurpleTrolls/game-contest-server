#! /usr/bin/env python3

from optparse import OptionParser
import pickle
import socket


def connect_to_socket(path):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect(path)
    return s


def send_name_using_socket(s, name):
    message = str(name + "\n")
    s.send(message.encode())


def handle_moves(s):
    pcolors = ["blue", "green", "yellow", "orange", "black", "white", "purple"]
    win = False
    while not win:
        currentPlayer, board = pickle.loads(s.recv(4096))
        if board != "win":
            row, col = playerFunction(pcolors, currentPlayer, board)
            data = "%s,%s" % (row, col)
            s.send(data)
        else:
            win = True


def init(playerFunction):
    parser = OptionParser()
    parser.add_option("-p", "--path", action="store", type="string", dest="path")
    parser.add_option("-n", "--name", action="store", type="string", dest="name")
    (options, args) = parser.parse_args()

    HOST = 'localhost'
    PATH = options.path
    NAME = options.name

    s = connect_to_socket(PATH)
    send_name_using_socket(s, NAME)
    handle_moves(s)
    s.close()
