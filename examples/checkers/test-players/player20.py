#! /usr/bin/env python3

from talk_to_referee import *

import time
import random
import math
EMPTY=0
INCs=[-1,1]
VALID_RANGE=range(8)
DEBUG=False
VISIBLE=True
DEPTH=4
def listValidMoves(tempboard,playerIndex,playerTokens,opponentTokens,rowInc):
    validMoves=[]
    for row in range(8):
        for col in range(8):
            if tempboard[row][col] in playerTokens: #it is the specified player's checker
                if tempboard[row][col] not in ["R","B"]: #not a king checker
                    for colInc in INCs:
                        toRow=row+rowInc
                        toCol=col+colInc
                        if toRow in VALID_RANGE and toCol in VALID_RANGE and tempboard[toRow][toCol]==EMPTY:
                            validMoves.append(chr(row+65)+str(col)+":"+chr(toRow+65)+str(toCol))
                else: #is a king checker
                    for rInc in INCs:
                        for colInc in INCs:
                            toRow=row+rInc
                            toCol=col+colInc
                            if toRow in VALID_RANGE and toCol in VALID_RANGE and tempboard[toRow][toCol]==EMPTY:
                                validMoves.append(chr(row+65)+str(col)+":"+chr(toRow+65)+str(toCol))
    return validMoves

def listValidJumps(tempboard,playerIndex,playerTokens,opponentTokens,rowInc):
    validJumps=[]
    for row in range(8):
        for col in range(8):
            if tempboard[row][col] in playerTokens: #it is the specified player's checker
                if tempboard[row][col] not in ["R","B"]: #not a king checker
                    for colInc in INCs:
                        toRow=row+(rowInc*2)
                        toCol=col+(colInc*2)
                        jumpRow=row+rowInc
                        jumpCol=col+colInc
                        if toRow in VALID_RANGE and toCol in VALID_RANGE and tempboard[toRow][toCol]==EMPTY and tempboard[jumpRow][jumpCol]in opponentTokens:
                            validJumps.append(chr(row+65)+str(col)+":"+chr(toRow+65)+str(toCol))
                else: #is a king checker
                    for rInc in INCs:
                        for colInc in INCs:
                            toRow=row+(rInc*2)
                            toCol=col+(colInc*2)
                            jumpRow=row+rInc
                            jumpCol=col+colInc
                            if toRow in VALID_RANGE and toCol in VALID_RANGE and tempboard[toRow][toCol]==EMPTY and tempboard[jumpRow][jumpCol]in opponentTokens:
                                validJumps.append(chr(row+65)+str(col)+":"+chr(toRow+65)+str(toCol))
    oldJumps=validJumps[:]
    newJumps=expandJumps(tempboard,playerIndex,oldJumps,playerTokens,opponentTokens,rowInc)
    while newJumps != oldJumps:
        oldJumps=newJumps[:]
        newJumps=expandJumps(tempboard,playerIndex,oldJumps,playerTokens,opponentTokens,rowInc)
    validJumps=newJumps[:]
    return validJumps

def expandJumps(CB,player,oldJumps,playerTokens,opponentTokens,rowInc):
    newJumps=[]
    for oldJump in oldJumps:
        row=ord(oldJump[-2])-65
        col=int(oldJump[-1])
        newJumps.append(oldJump)
        startRow=ord(oldJump[0])-65
        startCol=int(oldJump[1])
        if CB[startRow][startCol] not in ["R","B"]: #not a king
            for colInc in INCs:
                jumprow=row+rowInc
                jumpcol=col+colInc
                torow=row+2*rowInc
                tocol=col+2*colInc
                if jumprow in VALID_RANGE and jumpcol in VALID_RANGE and torow in VALID_RANGE and tocol in VALID_RANGE \
                and CB[jumprow][jumpcol] in opponentTokens and CB[torow][tocol]==EMPTY:
                    newJumps.append(oldJump+":"+chr(torow+65)+str(tocol))
                    if oldJump in newJumps:
                        newJumps.remove(oldJump)
        else: #is a king
            for colInc in INCs:
                for newRowInc in INCs:
                    jumprow=row+newRowInc
                    jumpcol=col+colInc
                    torow=row+2*newRowInc
                    tocol=col+2*colInc
                    if jumprow in VALID_RANGE and jumpcol in VALID_RANGE and torow in VALID_RANGE and tocol in VALID_RANGE \
                    and CB[jumprow][jumpcol] in opponentTokens and (CB[torow][tocol]==EMPTY or oldJump[0:2]==chr(torow+65)+str(tocol)) \
                    and ((oldJump[-2:]+":"+chr(torow+65)+str(tocol)) not in oldJump) and ((chr(torow+65)+str(tocol)+':'+oldJump[-2:] not in oldJump)) and (chr(torow+65)+str(tocol)!=oldJump[-5:-3]):
                        newJumps.append(oldJump+":"+chr(torow+65)+str(tocol))
                        if oldJump in newJumps:
                            newJumps.remove(oldJump)
##    print("Double Jump List: ",end="")
##    print(newJumps)
    return newJumps

def changetempboard(tempboard,fromTo,playerIndex):
    if playerIndex==0:
        kingRow=7
    else:
        kingRow=0
    while len(fromTo)>=5:
        fromRow=ord(fromTo[0])-65
        fromCol=int(fromTo[1])
        toRow=ord(fromTo[3])-65
        toCol=int(fromTo[4])
        if toRow==kingRow or tempboard[fromRow][fromCol] in ["R","B"]:
            isKing=True
        else:
            isKing=False
        if isKing:
            tempboard[toRow][toCol]=tempboard[fromRow][fromCol].upper()
        else:
            tempboard[toRow][toCol]=tempboard[fromRow][fromCol]
        tempboard[fromRow][fromCol]=0
        fromTo=fromTo[3:]
        
def findtokens(tempboard,playerIndex):
    if playerIndex==0:
        playerSymbols=["b","B"]
        opponentSymbols=["r","R"]
    if playerIndex==1:
        playerSymbols=["r","R"]
        opponentSymbols=["b","B"]
    numopponentTokens=0
    numplayerTokens=0
    for line in range(8):
        for char in range(line%2,8,2):
            if tempboard[line][char] in playerSymbols:
                numplayerTokens+=1
            if tempboard[line][char] in opponentSymbols:
                numopponentTokens+=1
    return numplayerTokens,numopponentTokens,playerSymbols,opponentSymbols
    
def evalmove(tempboard,move,playerIndex,rowInc):
    if playerIndex == 0:
        homerow="A"
    else:
        homerow="H"
    numplayerTokens,numopponentTokens,playerSymbols,opponentSymbols = findtokens(tempboard,playerIndex)
    valofmove=2
    if len(move)>5: #MultiJumps
        valofmove+=(len(move))
    if (int(move[-1]) - int(move[1])) not in [1,-1]: #Jumps
        valofmove+=6
    else: #Moves
        if move[-1]=="0" or move[-1]=="7":
            if numplayerTokens>numopponentTokens:
                valofmove+=1
            else:
                valofmove+=2
        elif move[0] == homerow and str(tempboard[ord(move[0])-65][int(move[1])]) != playerSymbols[1]:
            valofmove-=1
        if str(tempboard[ord(move[-2])-65][int(move[-1])]) in playerSymbols: #All
            if ord(move[-2])-65+(2*rowInc) in range(8) and int(move[-1])+(2*rowInc) in range(8):
                if str(tempboard[ord(move[-2])-65+(2*rowInc)][int(move[-1])]) in opponentSymbols:
                    valofmove+=1
                if str(tempboard[ord(move[-2])-65+(2*rowInc)][int(move[-1])+(2*rowInc)]) in opponentSymbols and str(tempboard[ord(move[-2])-65+(2*rowInc)][int(move[-1])+(2*rowInc)]) not in opponentSymbols:
                    valofmove+=2
                if str(tempboard[ord(move[-2])-65+(1*rowInc)][int(move[-1])+(1*rowInc)]) in playerSymbols and str(tempboard[ord(move[-2])-65+(2*rowInc)][int(move[-1])+(2*rowInc)]) in opponentSymbols:
                    valofmove+=3
                if move[-1]=="0" or move[-1]=="7" and str(tempboard[ord(move[-2])-65+(1*rowInc)][int(move[-1])+(1*rowInc)]) in playerSymbols and str(tempboard[ord(move[-2])-65+(2*rowInc)][int(move[-1])+(2*rowInc)]) in opponentSymbols:
                    valofmove+=2
            if ord(move[-2])-65+(2*rowInc) in range(8) and int(move[-1])-(2*rowInc) in range(8):    
                if str(tempboard[ord(move[-2])-65+(2*rowInc)][int(move[-1])-(2*rowInc)]) in opponentSymbols:
                    valofmove+=2
                if str(tempboard[ord(move[-2])-65+(1*rowInc)][int(move[-1])-(1*rowInc)]) in playerSymbols and  str(tempboard[ord(move[-2])-65+(2*rowInc)][int(move[-1])-(2*rowInc)]) in opponentSymbols:
                    valofmove+=2
                if move[-1]=="0" or move[-1]=="7" and str(tempboard[ord(move[-2])-65+(1*rowInc)][int(move[-1])-(1*rowInc)]) in playerSymbols and str(tempboard[ord(move[-2])-65+(2*rowInc)][int(move[-1])-(2*rowInc)]) in opponentSymbols:
                    valofmove+=3
        if str(tempboard[ord(move[-2])-65][int(move[-1])]) == playerSymbols[1]: #Kings
            if ord(move[-2])-65-(1*rowInc) in range(8):
                if int(move[-1])+(1*rowInc) in range(8):
                    if int(move[-1])-(1*rowInc) in range(8):
                        if str(tempboard[ord(move[-2])-65-(1*rowInc)][int(move[-1])+(1*rowInc)]) == opponentSymbols[0] and str(tempboard[ord(move[-2])-65-(1*rowInc)][int(move[-1])-(1*rowInc)]) not in opponentSymbols[1]:
                            valofmove+=2
                        if str(tempboard[ord(move[-2])-65-(1*rowInc)][int(move[-1])-(1*rowInc)]) == opponentSymbols[0] and str(tempboard[ord(move[-2])-65-(1*rowInc)][int(move[-1])+(1*rowInc)]) in playerSymbols:
                            valofmove+=2
                        if str(tempboard[ord(move[-2])-65-(1*rowInc)][int(move[-1])+(1*rowInc)]) == opponentSymbols[1] or str(tempboard[ord(move[-2])-65-(1*rowInc)][int(move[-1])-(1*rowInc)]) == opponentSymbols[1]:
                            valofmove-=4
            if ord(move[-2])-65-(2*rowInc) in range(8):
                if str(tempboard[ord(move[-2])-65-(2*rowInc)][int(move[-1])]) in opponentSymbols[1]:
                    valofmove-=3
    return valofmove

def findboardstate(tempboard,move,playerIndex,playerTokens,opponentTokens,rowInc,depth):
    if depth==0:
##        print(evalmove(tempboard,move,playerIndex,rowInc))
        return evalmove(tempboard,move,playerIndex,rowInc)
    else:
        validMoves = listValidJumps(tempboard,playerIndex,playerTokens,opponentTokens,rowInc)
        if len(validMoves) == 0:
            validMoves = listValidMoves(tempboard,playerIndex,playerTokens,opponentTokens,rowInc)
        templist = [] #make a new name for this
        valofmove=evalmove(tempboard,move,playerIndex,rowInc)
        if len(validMoves) == 0:
            return -100
        for Move in validMoves:
            tempBoard = []
            for line in tempboard:
                tempBoard.append(line[:])
            changetempboard(tempBoard,Move,playerIndex)
            templist.append(findboardstate(tempBoard,Move, not playerIndex,opponentTokens,playerTokens,rowInc*-1,(depth-1)))
            if Move[-2] in "AH" and str(tempboard[ord(Move[-2])-65][int(Move[-1])]) != playerTokens[1]: 
                templist[-1]+=6
##        print(move, valofmove-max(templist))
        return valofmove-max(templist)

def getMove(board,playerIndex,playerColors,playerTokens,opponentTokens,rowInc):
    tempBoard=[]
    bettermove=""
    for line in board:
        tempBoard.append(line[:])
    validMoves = listValidMoves(tempBoard,playerIndex,playerTokens,opponentTokens,rowInc)
    validJumps = listValidJumps(tempBoard,playerIndex,playerTokens,opponentTokens,rowInc)
    if len(validJumps)==0:
        validmovelist=validMoves
    else:
        validmovelist=validJumps
    validMovesD={}
    for move in validmovelist:
        tempBoard=[]
        for line in board:
            tempBoard.append(line[:])
        changetempboard(tempBoard,move,playerIndex)
        moveval = findboardstate(tempBoard,move,playerIndex,playerTokens,opponentTokens,rowInc*-1,DEPTH)
        validMovesD[move]=moveval
    vallist = list(validMovesD.values())
    maxval=max(vallist)
    maxvallist=[]
    for move in validMovesD:
        if validMovesD[move]==maxval:
            maxvallist.append(move)
    #print(maxvallist)
    if len(maxvallist)!=0:
        bettermove = random.choice(maxvallist)
    else:
        bettermove = random.choice(validmovelist)
        #print ("WHEEEEEE")
    return bettermove


