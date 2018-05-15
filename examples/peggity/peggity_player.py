#! /usr/bin/env python3

import random
import talk_to_referee

def manualMove(currentPlayer,board):
    emptyCellsList=[]
    for row in range(16):
        for col in range(16):
            if board[row][col]==0:
                emptyCellsList.append(chr(65+row)+str(col))
    move=emptyCellsList[random.randrange(0,len(emptyCellsList))]
    return move

talk_to_referee.init(manualMove)