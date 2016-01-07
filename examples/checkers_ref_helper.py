#! /usr/bin/env python3

#ref_helper.py

from optparse import OptionParser
import socket
import pickle

class PlayerConnection():

    def __init__(self, connection , address, player_name):
        #Get a connection from a player
        self.connection = connection
        self.address = address
        self.name = player_name

    def automatedMove(self, CB,player):
        self.connection.send(pickle.dumps((CB,player)))
        return pickle.loads(self.connection.recv(4096))

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
        self.connection.shutdown(socket.SHUT_RDWR)
        self.connection.close()

#To be run on import

#Parsing command line arguments
#Recieves port and number of players from game contest server
parser = OptionParser()
parser.add_option("-p","--port",action="store",type="int",dest="port")
parser.add_option("-n","--num",action="store",type="int",dest="num") #number of players, not used with checkers
parser.add_option("-r", "--rounds", action="store", type="int", dest="rounds") #Number of rounds, not used
(options, args) = parser.parse_args()

wrapper_port = options.port
wrapper_hostname = 'localhost'


#connect to match wrapper
manager = Manager(wrapper_hostname, wrapper_port)

#create and bind socket to listen for connecting players
player_socket  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
player_socket.bind(('',0))
player_socket_port = player_socket.getsockname()[1]
player_socket.listen(10)

#Tell the manager that the match has started
manager.send("port", str(player_socket_port))

#Wait for two players to connect and send their names

conn1,addr1 = player_socket.accept()
P1_name = ""
while P1_name == "":
    P1_name = conn1.recv(1024).decode()
P1 = PlayerConnection(conn1,addr1,P1_name)

conn2,addr2 = player_socket.accept()
P2_name = ""
while P2_name == "":
    P2_name = conn2.recv(1024).decode()
P2 = PlayerConnection(conn2,addr1,P2_name)


def report_results(resulttype, p1wins,p2wins):
    p1result = "Win"
    p2result = "Loss"
    if p2wins >= p1wins:
        if p2wins != p1wins:
            p1result = "Loss"
            p2result = "Win"
        else:
            p1result = "Tie"
            p2result = "Tie"
    manager.send(resulttype, [P1_name, p1result, str(p1wins)])
    manager.send(resulttype, [P2_name, p2result, str(p2wins)])

