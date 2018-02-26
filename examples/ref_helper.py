#! /usr/bin/env python3

from optparse import OptionParser
import socket
import signal
import sys
import os

def set_alarm_response(func):
    signal.signal(signal.SIGALRM, func)

def stop_alarm():
    signal.alarm(0)

#Create and listen to a socket
class SocketServer():
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', 0))
        self.port = self.socket.getsockname()[1]
        self.socket.listen(10)

    def __del__(self):
        try:
            self.socket.close()
        except:
            return

#Handle individual connections to the socket server
class Connection():
    def __init__(self, server):
        self.connection, self.address = server.socket.accept()

    def listen(self, buffersize):
        var = b""
        while var == b"":
            try:
                var = self.connection.recv(buffersize)
            except InterruptedError:
                continue
            except:
                break
        return var

    def send(self, data):
        if type(data) is str:
            data = data.encode()
        self.connection.send(data)

    def __del__(self):
        try:
            self.connection.shutdown(socket.SHUT_RDWR)
            self.connection.close()
        except:
            return

class Manager():
    #Create connection with manager
    def __init__(self, hostname, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ip = socket.gethostbyname(hostname)
        self.connection.connect((self.ip, port))

    #Send command to manager
    def send(self, command, value):
        #Convert array to value that server can understand
        if isinstance(value, list):
            value = map(str, value)
            value = "|".join(value)
        message = command + ":" + str(value) + "\n"
        try:
            result = self.connection.send(message.encode())
        except:
            result = False
        return result

    def __del__(self):
        try:
            self.connection.close()
        except:
            return

#Parse options from manager
parser = OptionParser()
parser.add_option("-p","--port",action="store",type="int",dest="port")
parser.add_option("-n","--num",action="store",type="int",dest="num") #number of players
parser.add_option("-r", "--rounds", action="store", type="int", dest="rounds") #Number of rounds
parser.add_option("-t", "--time", action="store", type="int", dest="time") #Max amount of time for the match
parser.add_option("-m", "--turns", action="store", type="int", dest="turns") #Max number of turns for the match
(options, args) = parser.parse_args()

signal.alarm(options.time)

#connect to match wrapper
manager = Manager('localhost', options.port)

#create and bind socket to listen for connecting players
playerServer = SocketServer()

#Tell the manager what port players should connect on
manager.send("port", playerServer.port)
