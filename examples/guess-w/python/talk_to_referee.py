#! /usr/bin/env python3

import socket

def init(move):
    HOST = 'localhost'
    PORT = options.port
    NAME = options.name

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = socket.gethostbyname(HOST)
    s.connect((ip, PORT))

    message = str(NAME + "\n")
    s.send(message.encode())

    while True:
        reply = s.recv(4096).decode()
        if "move" in reply:
            s.send(move.encode())
        elif "wins" in reply:
            break

    s.close()