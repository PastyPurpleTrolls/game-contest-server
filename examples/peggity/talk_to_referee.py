#! /usr/bin/env python3

from optparse import OptionParser
import socket


def connect_to_socket(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = socket.gethostbyname(host)
    s.connect((ip, port))
    return s


def send_name_using_socket(s, name):
    message = str(name + "\n")
    s.send(message.encode())


def handle_moves(s):
    reply = ""
    while "wins" not in reply:
        reply = s.recv(4096).decode()
        if "move" in reply:
            s.send(move.encode())


def init(playerFunction):
    parser = OptionParser()
    parser.add_option("-p", "--port", action="store", type="int", dest="port")
    parser.add_option("-n", "--name", action="store", type="string", dest="name")
    (options, args) = parser.parse_args()

    HOST = 'localhost'
    PORT = options.port
    NAME = options.name

    s = connect_to_socket(HOST, PORT)
    send_name_using_socket(s, NAME)

    reply = ""
    while "wins" not in reply:
        reply = s.recv(4096).decode()
        if "move" in reply:
            s.send(move.encode())

    s.close()
