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


# Receives the game state from the referee,
# and sends the player move to the referee.
def handle_moves(s, playerFunction):
    win = False
    while not win:
        gameStateVariable1, gameStateVariable2 = pickle.loads(s.recv(4096))
        if gameStateVariable1 != "win":
            move = playerFunction()
            s.send(move.encode())
        else:
            win = True


def init(playerFunction):
    parser = OptionParser()
    parser.add_option("-p", "--path", action="store", type="string", dest="path")
    parser.add_option("-n", "--name", action="store", type="string", dest="name")
    (options, args) = parser.parse_args()

    PATH = options.path
    NAME = options.name

    s = connect_to_socket(PATH)
    send_name_using_socket(s, NAME)
    handle_moves(s, playerFunction)
    s.close()
