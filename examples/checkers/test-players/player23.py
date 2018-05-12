#! /usr/bin/env python3

from talk_to_referee import *

## MP14

import time
import random
EMPTY=0
INCs=[-1,1]
VALID_RANGE=range(8)
DEBUG=False
VISIBLE=True

def listValidMoves(CB,player,playerTokens,opponentTokens,rowInc):
    validMoves=[]
    for row in range(8):
        for col in range(8):
            if CB[row][col] in playerTokens: #it is the specified player's checker
                if CB[row][col] not in ["R","B"]: #not a king checker
                    for colInc in INCs:
                        toRow=row+rowInc
                        toCol=col+colInc
                        if toRow in VALID_RANGE and toCol in VALID_RANGE and CB[toRow][toCol]==EMPTY:
                            validMoves.append(chr(row+65)+str(col)+":"+chr(toRow+65)+str(toCol))
                else: #is a king checker
                    for rInc in INCs:
                        for colInc in INCs:
                            toRow=row+rInc
                            toCol=col+colInc
                            if toRow in VALID_RANGE and toCol in VALID_RANGE and CB[toRow][toCol]==EMPTY:
                                validMoves.append(chr(row+65)+str(col)+":"+chr(toRow+65)+str(toCol))
    return validMoves

def listValidJumps(CB,player,playerTokens,opponentTokens,rowInc):
    validJumps=[]
    for row in range(8):
        for col in range(8):
            if CB[row][col] in playerTokens: #it is the specified player's checker
                if CB[row][col] not in ["R","B"]: #not a king checker
                    for colInc in INCs:
                        toRow=row+(rowInc*2)
                        toCol=col+(colInc*2)
                        jumpRow=row+rowInc
                        jumpCol=col+colInc
                        if toRow in VALID_RANGE and toCol in VALID_RANGE and CB[toRow][toCol]==EMPTY and CB[jumpRow][jumpCol]in opponentTokens:
                            validJumps.append(chr(row+65)+str(col)+":"+chr(toRow+65)+str(toCol))
                else: #is a king checker
                    for rInc in INCs:
                        for colInc in INCs:
                            toRow=row+(rInc*2)
                            toCol=col+(colInc*2)
                            jumpRow=row+rInc
                            jumpCol=col+colInc
                            if toRow in VALID_RANGE and toCol in VALID_RANGE and CB[toRow][toCol]==EMPTY and CB[jumpRow][jumpCol]in opponentTokens:
                                validJumps.append(chr(row+65)+str(col)+":"+chr(toRow+65)+str(toCol))
    return validJumps

def getManualMove(validMoves,validJumps,playerIndex,playerColors):
    move=input("Enter a move " + playerColors[playerIndex] + " => ")
    if move=="exit":
        return move
    if len(validJumps)>0:
        while move not in validJumps:
            print("You must take the jump!")
            print(validJumps)
            move=input("Enter a jump " + playerColors[playerIndex] + " => ")
        return move
    while move not in validMoves:
        print(move, "is invalid!  Please try again from the following:")
        print(validMoves)
        move=input("Enter a move " + playerColors[playerIndex] + " => ")
    return move

def getMove(board,playerIndex,playerColors,playerTokens,opponentTokens,rowInc):
    validMoves=listValidMoves(board,playerIndex,playerTokens,opponentTokens,rowInc)
    validJumps=listValidJumps(board,playerIndex,playerTokens,opponentTokens,rowInc)
    if rowInc==1:
        kingRow="H"
    else:
        kingRow="A"
    if len(validJumps)==0:
        for m in validMoves:
            if m[3]==kingRow:
                move=m
                return move
        
        move=validMoves[random.randrange(0,len(validMoves))]
    else:
        for j in validJumps:
            if j[3]==kingRow:
                move=j
                return move
            if j[4]=="0" or j[4]=="7":
                move=j
                return move
            destR=j[3]
            destC=int(j[4])
            destR=ord(destR)-65
            if board[destR+rowInc][destC+1] in opponentTokens:
                if board[destR-rowInc][destC-1] == 0:
                    if len(validJumps) > 1:
                        validJumps.remove(j)
                        continue
            if board[destR+rowInc][destC-1] in opponentTokens:
                if board[destR-rowInc][destC+1] == 0:
                    if len(validJumps) > 1:
                        validJumps.remove(j)
                        continue
            if board[destR-rowInc][destC+1] == opponentTokens[1]:
                if board[destR+rowInc][destC-1] == 0:
                    if len(validJumps) > 1:
                        validJumps.remove(j)
                        continue
            if board[destR-rowInc][destC-1] == opponentTokens[1]:
                if board[destR+rowInc][destC+1] == 0:
                    if len(validJumps) > 1:
                        validJumps.remove(j)
                        continue 
            if destC<6 and destC>1 and destR>1 and destR<6:
                if board[destR+rowInc][destC+1] in playerTokens:
                    if board[destR+rowInc+rowInc][destC+2] in opponentTokens:
                        move=j
                        return move
                if board[destR+rowInc][destC-1] in playerTokens:
                    if board[destR+rowInc+rowInc][destC-2] in opponentTokens:
                        move=j
                        return move
                if board[destR-rowInc][destC-1] in playerTokens:
                    if board[destR-rowInc-rowInc][destC-2] == opponentTokens[1]:
                        move=j
                        return move
                if board[destR-rowInc][destC+1] in playerTokens:
                    if board[destR-rowInc-rowInc][destC+2] == opponentTokens[1]:
                        move=j
                        return move
        move=validJumps[random.randrange(0,len(validJumps))]
             
    return move
