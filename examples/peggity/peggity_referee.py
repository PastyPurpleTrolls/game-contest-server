#! /usr/bin/env python3

from ref_helper import *
import json
import pickle
import random

BOARD_SIZE = 16

class Player:
    def __init__(self, server):
        self.wins = 0
        self.connection = Connection(server)
        self.name = self.connection.listen(1024).decode().rstrip()

    def move(self, currentPlayer, board):
        stringBoard = pickle.dumps(board)
        data = "%s|%s" % (currentPlayer, board)
        self.connection.send(data)
        move = self.connection.listen(1024).decode().rstrip()
        moveList = move.split(',')
        row = moveList[0]
        col = moveList[1]
        return row, col


class Game:
    def __init__(self, numPlayers):
        self.players = self.getPlayers(numPlayers)
        manager.send("match", "start")
        winner = self.runGame()
        manager.send("round", "end")
        self.reportResults("roundresult", winner)
        manager.send("match", "end")
        self.reportResults("matchresult", winner)
    
    def getPlayers(self, numPlayers):
        players = []
        for i in range(numPlayers):
            players.append(Player(playerServer))
        return players
    
    def runGame(self):
        manager.send("round", ["start", 0])
        board = self.getInitialBoard()
        invalidPreviousMove = False
        playerNum = 1
        while True:
            for player in self.players:
                if invalidPreviousMove:
                    return player.name
                row, col = player.move(playerNum, board)
                if self.isValidMove(row, col):
                    board[row][col] = player
                    if self.checkWin(board):
                        player.addWin()
                        return player
                    playerNum = switchPlayer(playerNum)
                else:
                    invalidPreviousMove = True

    def getInitialBoard(self):
        board = []
        for rows in range(BOARD_SIZE):
            row = []
            for cols in range(BOARD_SIZE):
                row.append(0)
            board.append(row)
        return board
    
    def isValidMove(self, row, col):
        if row < 0 or row >= BOARD_SIZE or col < 0 or row >= BOARD_SIZE:
            return False
        return board[row][col] == 0
    
    def switchPlayer(self, player):
        if player == 1:
            return 2
        return 1
    
    def sendMoveToManager(self, player, row, col):
        moveDescription = "%s plays (%s, %s)" % (player.name, row, col)
        move = json.dumps([player.name, row, col])
        manager.send("move", [moveDescription, move])

    def checkWin(self, board):
        horizontal = self.checkHorizontalWin(board)
        vertical = self.checkVerticalWin(board)
        leftToRight = self.checkLeftToRightDiagonal(board)
        rightToLeft = self.checkRightToLeftDiagonal(board)
        return horizontal or vertical or leftToRight or rightToLeft

    def checkHorizontalWin(self, board):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE-4):
                if self.checkWinForSet(board[row][col:col+5]):
                    return True
        return False

    def checkVerticalWin(self, board):
        for row in range(BOARD_SIZE-4):
            for col in range(BOARD_SIZE):
                potentialWinSet = []
                for i in range(row, row+5):
                    potentialWinSet.append(board[i][col])
                if self.checkWinForSet(potentialWinSet):
                    return True
        return False

    def checkLeftToRightDiagonal(self, board):
        for row in range(BOARD_SIZE-4):
            for col in range(BOARD_SIZE-4):
                potentialWinSet = []
                for i in range(5):
                    potentialWinSet.append(board[row+i][col+i])
                if self.checkWinForSet(potentialWinSet):
                    return True
        return False

    def checkRightToLeftDiagonal(self, board):
        for row in range(BOARD_SIZE-4):
            for col in range(4, BOARD_SIZE):
                potentialWinSet = []
                for i in range(5):
                    potentialWinSet.append(board[row+i][col-i])
                if self.checkWinForSet(potentialWinSet):
                    return True
        return False
    
    def reportResults(self, resulttype, winner):
        for player in self.players:
            # Tell the player who won
            data = "%s|%s" % (winner, "win")
            player.connection.send(data)
            # Get the result for who won
            result = "Win" if (player.name == winner.name) else "Loss"
            manager.send(resulttype, [player.name, result, str(player.wins)])

    def checkWinForSet(self, setOfFive):
        firstPiece = setOfFive[0]
        if firstPiece != 0 and setOfFive.count(firstPiece) == 5:
            return True
        return False


game = Game(options.num)
