#! /usr/bin/env python3

# Alex Sjoberg
# Jan 2014
# Library for COS 120 student checker program
# When started, sends name to port provided

from optparse import OptionParser
import socket
import pickle

def init(playerFunction):
    ref_path = options.path
    player_name  = options.name

    ref_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    ref_socket.connect(ref_path)
    ref_socket.send(player_name.encode())
    while True:
        try:
            b,playerIndex,playerColors,playerSymbols,opponentSymbols,rowInc = pickle.loads(ref_socket.recv(4096))
            ref_socket.send(pickle.dumps(playerFunction(b,playerIndex,playerColors,playerSymbols,opponentSymbols,rowInc)))
        except EOFError:
            break

#Parsing command line arguments
#Usage: client.py --name [name] -p [port]"
parser = OptionParser()
parser.add_option("-p","--path",action="store",type="int",dest="path")
parser.add_option("-n","--name" ,action="store",type="string",dest="name")
(options, args) = parser.parse_args()
