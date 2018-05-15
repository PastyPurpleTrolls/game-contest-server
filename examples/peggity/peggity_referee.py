#! /usr/bin/env python3

import json
import optparse
import os
import pickle
import random
import signal
import socket
import sys

BOARD_SIZE = 16
SEQUENCE_SIZE_TO_WIN = 5
REFEREE_PATH = "/tmp/peggity-referee"


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

    def move(self, currentPlayer, board):
        data = pickle.dumps((currentPlayer, board))
        self.connection.send(data)
        move = self.connection.listen(1024).decode().rstrip()
        row = ord(move[0])-65
        col = int(moveList[1:])
        return row, col


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
        board = self.__getInitialBoard()
        invalidPreviousMove = False
        playerNum = 1
        spacesFilled = 0
        while spacesFilled < BOARD_SIZE ** 2:
            for player in self.players:
                if invalidPreviousMove:
                    return player.name
                row, col = player.move(playerNum, board)
                row = int(row)
                col = int(col)
                self.__sendMoveToManager(player, row, col)
                if self.__isValidMove(board, row, col):
                    board[row][col] = playerNum
                    if self.__checkWin(board, SEQUENCE_SIZE_TO_WIN):
                        return player
                    playerNum = self.__switchPlayer(playerNum)
                    spacesFilled += 1
                else:
                    invalidPreviousMove = True

    def __getInitialBoard(self):
        board = []
        for rows in range(BOARD_SIZE):
            row = []
            for cols in range(BOARD_SIZE):
                row.append(0)
            board.append(row)
        return board
    
    def __isValidMove(self, board, row, col):
        if row < 0 or row >= BOARD_SIZE or col < 0 or row >= BOARD_SIZE:
            return False
        return board[row][col] == 0
    
    def __switchPlayer(self, player):
        if player == 1:
            return 2
        return 1
    
    def __sendMoveToManager(self, player, row, col):
        moveDescription = "%s plays (%s, %s)" % (player.name, row, col)
        move = json.dumps([player.name, row, col])
        manager.send("move", [moveDescription, move])

    def __checkWin(self, board, inARow):
        horizontal = self.__checkHorizontalWin(board, inARow)
        vertical = self.__checkVerticalWin(board, inARow)
        leftToRight = self.__checkLeftToRightDiagonal(board, inARow)
        rightToLeft = self.__checkRightToLeftDiagonal(board, inARow)
        return horizontal or vertical or leftToRight or rightToLeft

    def __checkHorizontalWin(self, board, inARow):
        for row in range(BOARD_SIZE):
            lastCol = BOARD_SIZE - (inARow - 1)
            for col in range(lastCol):
                if self.__checkWinForSet(board[row][col:col+inARow]):
                    return True
        return False

    def __checkVerticalWin(self, board, inARow):
        lastRow = BOARD_SIZE - (inARow - 1)
        for row in range(lastRow):
            for col in range(BOARD_SIZE):
                potentialWinSet = []
                for i in range(row, row+inARow):
                    potentialWinSet.append(board[i][col])
                if self.__checkWinForSet(potentialWinSet):
                    return True
        return False

    def __checkLeftToRightDiagonal(self, board, inARow):
        lastRowAndCol = BOARD_SIZE - (inARow - 1)
        for row in range(lastRowAndCol):
            for col in range(lastRowAndCol):
                potentialWinSet = []
                for i in range(inARow):
                    potentialWinSet.append(board[row+i][col+i])
                if self.__checkWinForSet(potentialWinSet):
                    return True
        return False

    def __checkRightToLeftDiagonal(self, board, inARow):
        lastRow = BOARD_SIZE - (inARow - 1)
        firstCol = inARow - 1
        for row in range(lastRow):
            for col in range(firstCol, BOARD_SIZE):
                potentialWinSet = []
                for i in range(inARow):
                    potentialWinSet.append(board[row+i][col-i])
                if self.__checkWinForSet(potentialWinSet):
                    return True
        return False
    
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

    def __checkWinForSet(self, sequence):
        firstPiece = sequence[0]
        if firstPiece != 0 and sequence.count(firstPiece) == len(sequence):
            return True
        return False


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
