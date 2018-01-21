#! /usr/bin/env python3

import json
from ref_helper import *

class Player():
    def __init__(self, server):
        self.wins = 0

        self.connection = Connection(server)
        self.name = self.connection.listen(1024).decode().rstrip()

    def addWin(self):
        self.wins += 1
        return self.wins

    def move(self):
        self.connection.send('move')
        move = self.connection.listen(1024).decode().rstrip()
        return move

class Game():

    def __init__(self, numPlayers):
        self.players = []

        #Create players
        for i in range(numPlayers):
            self.players.append(Player(playerServer))

        manager.send("match", "start")

        winner = self.runGame()
        manager.send("round", "end")
        self.reportResults("roundresult", winner)

        manager.send("match", "end")
        self.reportResults("matchresult", winner)

    def reportResults(self, resulttype, winner):
        for player in self.players:
            #Tell the player who won
            player.connection.send(winner.name + " wins\n")
            #Get the result for who won
            result = "Win" if (player.name == winner.name) else "Loss"
            manager.send(resulttype, [player.name, result, str(player.wins)])

    def runGame(self):
        #Loop until someone wins
        manager.send("round", ["start", 0])
        while True:
            for player in self.players:
                move = player.move()
                #Report move to manager
                manager.send("move", [player.name + " plays " + move, json.dumps([player.name, move])])
                #Check if it's a winning move
                if self.checkWin(move):
                    player.addWin()
                    return player

    def checkWin(self, move):
        return move == 'w'

game = Game(options.num)
