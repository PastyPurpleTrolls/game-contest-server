#! /usr/bin/env python3

from optparse import OptionParser
import socket

def init(move):
    #Parsing command line arguments
    #Usage: client.py --name [name] -p [port]"
    parser = OptionParser()
    parser.add_option("-p", "--port", action="store", type="int", dest="port")
    parser.add_option("-n", "--name", action="store", type="string", dest="name")
    (options, args) = parser.parse_args()

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