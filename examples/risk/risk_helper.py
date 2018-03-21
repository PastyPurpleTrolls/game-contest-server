#! /usr/bin/env python3

#Maps Risk player functions to a server socket

from optparse import OptionParser

import socket
import pickle

#Get options
parser = OptionParser()
parser.add_option("-p","--path",action="store",type="int",dest="path")
parser.add_option("-n","--name" ,action="store",type="string",dest="name")
(options, args) = parser.parse_args()

class Player():
    def __init__(self, playerFunctions):

        #Dictionary containing all the player functions
        self.playerFunctions = playerFunctions

        self.ref_path = options.path
        self.player_name = options.name

        #Connect to referee
        self.connect()

        #Introduce myself to the ref
        self.send(self.player_name)

        #Start listen loop
        self.listen()

    def connect(self):
        self.ref_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.ref_socket.connect(self.ref_path)

    def send(self, message):
        self.ref_socket.send(message.encode())

    def listen(self):
        while True:
            try:
                #Get the function to call, along with a list of arguments to send
                functionName, arguments = pickle.loads(self.ref_socket.recv(4096))
                #Check that function exists
                if (functionName in self.playerFunctions):
                    self.ref_socket.send(pickle.dumps(self.playerFunctions[functionName](*arguments)))
            except:
                break

    def __del__(self):
        try:
            self.ref_socket.close()
        except:
            return


