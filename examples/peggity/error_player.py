#! /usr/bin/env python3

import random
import talk_to_referee

def manualMove(pcolors,currentPlayer,board):
    emptyCellsList=[]
    for row in range(16):
        for col in range(16):
            if board[row][col]==0:
                emptyCellsList.append(chr(65+row)+str(col))
    move=emptyCellsList[random.randrange(0,len(emptyCellsList))]
    row=ord(move[0])-65
    col=int(moves[1:])
    return row,col

talk_to_referee.init(manualMove)
