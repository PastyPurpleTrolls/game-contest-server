#! /usr/bin/env python3

import json
import optparse
import os
import pickle
import signal
import socket

REFEREE_PATH = "/tmp/referee"


class SocketServer:
    def __init__(self, path):
        if os.path.exists(path):
            os.remove(path)
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.bind(path)
        self.socket.listen(10)

    def __del__(self):
        try:
            self.socket.close()
        except:
            return


class Connection:
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


class Manager:
    def __init__(self, path):
        self.connection = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.connection.connect(path)

    def send(self, command, value):
        value = self.__convertArrayToServerValue(value)
        message = command + ":" + str(value) + "\n"
        try:
            return self.connection.send(message.encode())
        except:
            return False

    def __convertArrayToServerValue(self, value):
        if isinstance(value, list):
            value = map(str, value)
            return "|".join(value)
        return value

    def __del__(self):
        try:
            self.connection.close()
        except:
            return


class Player:
    def __init__(self, server):
        self.wins = 0
        self.connection = Connection(server)
        self.name = self.connection.listen(1024).decode().rstrip()

    def move(self):
        data = None
        self.connection.send(data)
        move = self.connection.listen(1024).decode().rstrip()
        return move


class Match:
    def __init__(self, numPlayers):
        self.players = self.__getPlayers(numPlayers)
        signal.signal(signal.SIGALRM, self.__reportTie)

    def run(self):
        manager.send("match", "start")
        manager.send("round", ["start", 0])
        winner = self.__runRound()
        manager.send("round", "end")
        self.__reportResults("roundresult", winner, True)
        manager.send("match", "end")
        self.__reportResults("matchresult", winner, False)
    
    def __getPlayers(self, numPlayers):
        playerServer = SocketServer(REFEREE_PATH)
        players = []
        for i in range(numPlayers):
            players.append(Player(playerServer))
        return players

    def __runRound(self):
        pass
    
    def __reportResults(self, resulttype, winner, informPlayer=True):
        if winner:
            self.__reportWinner(resulttype, winner, informPlayer)
        else:
            self.__reportTie(resulttype, informPlayer)

    def __reportWinner(self, resulttype, winner, informPlayer=True):
        for player in self.players:
            # Tell the player who won
            data = pickle.dumps((winner.name, "win"))
            if informPlayer:
                player.connection.send(data)
            # Get the result for who won
            result = "Win" if (player.name == winner.name) else "Loss"
            manager.send(resulttype, [player.name, result, str(player.wins)])

    def __reportTie(self, resulttype="match", informPlayer=True):
        for player in self.players:
            # Inform player round ended
            data = pickle.dumps(("", "win"))
            if informPlayer:
                player.connection.send(data)
            manager.send(resulttype, [player.name, "Tie", str(player.wins)])


def getOptions():
    parser = optparse.OptionParser()
    parser.add_option("-p", "--path", action="store", type="string", dest="path")
    parser.add_option("-n", "--num", action="store", type="int", dest="num")  # number of players
    parser.add_option("-r", "--rounds", action="store", type="int", dest="rounds")  # Number of rounds
    parser.add_option("-t", "--time", action="store", type="int", dest="time")  # Max amount of time for the match
    parser.add_option("-m", "--turns", action="store", type="int", dest="turns")  # Max number of turns for the match
    return parser.parse_args()


options, args = getOptions()
signal.alarm(options.time)

manager = Manager(options.path)
manager.send("path", REFEREE_PATH)

match = Match(options.num)
match.run()
