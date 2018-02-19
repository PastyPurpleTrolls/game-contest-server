import time
import random
import copy

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
                        if toRow in VALID_RANGE and toCol in VALID_RANGE and CB[toRow][toCol]==EMPTY and CB[jumpRow][jumpCol] in opponentTokens:
                            validJumps.append(chr(row+65)+str(col)+":"+chr(toRow+65)+str(toCol))
                else: #is a king checker
                    for rInc in INCs:
                        for colInc in INCs:
                            toRow=row+(rInc*2)
                            toCol=col+(colInc*2)
                            jumpRow=row+rInc
                            jumpCol=col+colInc
                            if toRow in VALID_RANGE and toCol in VALID_RANGE and CB[toRow][toCol]==EMPTY and CB[jumpRow][jumpCol] in opponentTokens:
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
    return newJumps

#*********************************************************************************
#************************* Heuristics Helpers *************************************
#*********************************************************************************
def between(jmp,location):
    fromRow=ord(jmp[0:1])-65
    fromCol=int(jmp[1:2])
    betweenRow=ord(location[0])-65
    betweenCol=int(location[1])
    toRow=ord(jmp[-2])-65
    toCol=int(jmp[-1])
    if (fromRow + toRow)//2 == betweenRow and (fromCol+toCol)//2 == betweenCol:
        if DEBUG:print(location, "is between jump",jmp)
        return True
    else:
        if DEBUG:print(location, "is NOT between jump",jmp)
        return False   

def swapPlayer(playerIndex):
    if playerIndex==0:
        playerIndex=1
        rowInc=-1
        playerSymbols=["b","B"]
        opponentSymbols=["r","R"]
    else:
        playerIndex=0
        rowInc=1
        playerSymbols=["r","R"]
        opponentSymbols=["b","B"]
    return playerIndex,playerSymbols,opponentSymbols,rowInc

def countCheckers(board,playerTokens,opponentTokens):
    playerCount = 0
    opponentCount = 0
    for row in board:
        for square in row:
            if square in playerTokens:
                playerCount += 1
            elif square in opponentTokens:
                opponentCount += 1
    return playerCount,opponentCount

#*********************************************************************************
#***************************** Heuristics ****************************************
#*********************************************************************************

#Heuristic 1
def jumpsIntoSafeSpot(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    enemyIndex,enemySymbols,mySymbols,enemyRowInc=swapPlayer(playerIndex)
    lst=copy.deepcopy(validJumps)
    for jmp in validJumps:
        #As though we were going to make the move . . .
        fromRow=ord(jmp[0:1])-65
        fromCol=int(jmp[1:2])
        toRow=ord(jmp[-2])-65
        toCol=int(jmp[-1])
        betweenRow=(fromRow + toRow)//2
        betweenCol=(fromCol + toCol)//2
        testBoard=copy.deepcopy(board)
        testBoard[toRow][toCol]=testBoard[fromRow][fromCol]
        testBoard[fromRow][fromCol]=0
        testBoard[betweenRow][betweenCol]=0
        enemyJumps=listValidJumps(testBoard,enemyIndex,enemySymbols,mySymbols,enemyRowInc)
        for jmpe in enemyJumps:
            if between(jmpe,jmp[-2:]):
                if jmp in lst:
                    lst.remove(jmp)
    return lst    

#Heuristic 2
def jumpsIntoKingRow(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    if rowInc>0:
        kingRow=7
    else:
        kingRow=0
    lst=[]
    for jump in validJumps:
        if ord(jump[-2])-65==kingRow:
            lst.append(jump)
    return lst  

#Heuristic 3
def jumpsFromPossibleJump(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    enemyIndex,enemySymbols,mySymbols,enemyRowInc=swapPlayer(playerIndex)
    testBoard=copy.deepcopy(board)
    lst=[]
    enemyJumps=listValidJumps(testBoard,enemyIndex,enemySymbols,mySymbols,enemyRowInc)
    #Are any of my starting points the in between point for any of his jumps?
    for jmp in validJumps:
        for jmpe in enemyJumps:
            if between(jmpe,jmp[0:2]):
                lst.append(jmp)
    return lst

#Heuristic 4
def jumpsIntoSideSquare(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    lst=[]
    for jmp in validJumps:
        if jmp[-1]in ['0','7']:
            lst.append(jmp)
    return lst

#Heuristic 5
def movesIntoKingRow(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    if rowInc>0:
        kingRow=7
    else:
        kingRow=0
    lst=[]
    for move in validMoves:
        if board[ord(move[0])-65][int(move[1])] == playerTokens[0]:
            if ord(move[3])-65==kingRow:
                lst.append(move)
    return lst  

#Heuristic 6
def moveToBlockJump(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    enemyIndex,enemySymbols,mySymbols,enemyRowInc=swapPlayer(playerIndex)
    testBoard=copy.deepcopy(board)
    lst=[]
    enemyJumps=listValidJumps(testBoard,enemyIndex,enemySymbols,mySymbols,enemyRowInc)
    for move in validMoves:
        for jmpe in enemyJumps:
            if between(jmpe,move[3:5]):
                lst.append(move)
    return lst

#Heuristic 7
def moveToEvadeJump(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    enemyIndex,enemySymbols,mySymbols,enemyRowInc=swapPlayer(playerIndex)
    enemyJumps=listValidJumps(board,enemyIndex,enemySymbols,mySymbols,enemyRowInc)
    lst = []
    for move in validMoves:
        for jmpe in enemyJumps:
            if between(jmpe,move[0:2]):
                lst.append(move)
    return lst

#Heuristic 8
def moveToForceJumpOutOfKing(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    enemyIndex,enemySymbols,mySymbols,enemyRowInc=swapPlayer(playerIndex)
    playerCount,opponentCount = countCheckers(board,playerTokens,opponentTokens)
    lst = []
    if playerCount > opponentCount:
        for mv in validMoves:
            #As though we were going to make the move . . .
            fromRow=ord(mv[0:1])-65
            fromCol=int(mv[1:2])
            toRow=ord(mv[3:4])-65
            toCol=int(mv[4:5])
            testBoard=copy.deepcopy(board)
            testBoard[toRow][toCol]=testBoard[fromRow][fromCol]
            testBoard[fromRow][fromCol]=0
            enemyJumps=listValidJumps(testBoard,enemyIndex,enemySymbols,mySymbols,enemyRowInc)
            for jmp in enemyJumps:
                if between(jmp,mv[3:5]):
                    if enemyRowInc == 1: 
                        if jmp[0] == "A":
                            lst.append(mv)
                    elif enemyRowInc == -1:
                        if jmp[0] == "H":
                            lst.append(mv)
    return lst

#Heuristic 9
def moveToSideSquare(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    lst = []
    for move in validMoves:
        if board[ord(move[0])-65][int(move[1])] == playerTokens[0]:
            if (move[-1] == "0" or move[-1] == "7") and (move[0] != "A" and move[0] != "H"):
                lst.append(move)
    return lst
        
#Heuristic 10
def moveNotKingRow(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    lst = []
    for move in validMoves:
        if rowInc == 1:
            if move[0] != "A":
                lst.append(move)
        elif rowInc == -1:
            if move[0] != "H":
                lst.append(move)
    return lst

#Heuristic 11
def movesIntoSafeSpot(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    enemyIndex,enemySymbols,mySymbols,enemyRowInc=swapPlayer(playerIndex)
    lst=copy.deepcopy(validMoves)
    for mv in validMoves:
        #As though we were going to make the move . . .
        fromRow=ord(mv[0:1])-65
        fromCol=int(mv[1:2])
        toRow=ord(mv[3:4])-65
        toCol=int(mv[4:5])
        testBoard=copy.deepcopy(board)
        testBoard[toRow][toCol]=testBoard[fromRow][fromCol]
        testBoard[fromRow][fromCol]=0
        enemyJumps=listValidJumps(testBoard,enemyIndex,enemySymbols,mySymbols,enemyRowInc)
        if DEBUG:print("ENEMY JUMPS for move",mv,enemyJumps)
        for jmp in enemyJumps:
            if between(jmp,mv[3:5]):
                if mv in lst:
                    lst.remove(mv)
    return lst


"""1) If jumps are present, select a jump that does not leave your checker
in a position where it will be jumped in turn
2) If jumps are present, and a jump into the king row is possible, take it
3) If jumps are present, and a jump resulting in the prevention of one your
checkers being jumped is possible, take it
4) If jumps are present, and a jump into a side square is possible, take it.
5) If only a move is possible, and a move into the king row is possible, take it.
6) If only a move is possible, move into a square to block an opponent's jump.
7) If only a move is possible, and you are in danger of being jumped, move to a safe square.
8) If only a move is possible, and you have more remaining checkers than your opponent, move into a square that will force your
   opponent to jump out of their king row.
9) If only a move is possible, move into a side square as long as the checker is not in the king row.
10) If only a move is possible, move a checker that is not in your king row.
11) If only a move is possible, move a checker to a spot where it can't be jumped (already included in Dr. White's code).
"""
def getMove(board,playerIndex,playerColors,playerTokens,opponentTokens,rowInc):
    validMoves=listValidMoves(board,playerIndex,playerTokens,opponentTokens,rowInc)
    validJumps=listValidJumps(board,playerIndex,playerTokens,opponentTokens,rowInc)

    oldJumps=validJumps[:]
    newJumps=expandJumps(board,playerIndex,oldJumps,playerTokens,opponentTokens,rowInc)
    while newJumps != oldJumps:
        oldJumps=newJumps[:]
        newJumps=expandJumps(board,playerIndex,oldJumps,playerTokens,opponentTokens,rowInc)
    validJumps=newJumps[:]
    if DEBUG:print("MOVES:",validMoves)
    if DEBUG:print("JUMPS:",validJumps)

    jumpsIntoSafeSpotList=jumpsIntoSafeSpot(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    jumpsIntoKingRowList=jumpsIntoKingRow(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    jumpsFromPossibleJumpList=jumpsFromPossibleJump(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    jumpsIntoSideSquareList=jumpsIntoSideSquare(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    movesIntoKingRowList=movesIntoKingRow(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)

    moveToBlockJumpList=moveToBlockJump(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    moveToEvadeJumpList=moveToEvadeJump(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    moveToForceJumpOutOfKingList=moveToForceJumpOutOfKing(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    moveToSideSquareList=moveToSideSquare(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    moveNotKingRowList=moveNotKingRow(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    
    movesIntoSafeSpotList=movesIntoSafeSpot(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)

    if len(validJumps)==0:
##        print(moveToSideSquareList)
        validMovesScores = []
        for validMove in validMoves:
            validMovesScores.append(0)
        if movesIntoKingRowList != []:
            for move in movesIntoKingRowList:
                index = validMoves.index(move)
                validMovesScores[index] += 2
##            print("Heuristic #5!")
##            move = movesIntoKingRowList[random.randrange(0,len(movesIntoKingRowList))]
        if moveToBlockJumpList != []:
            for move in moveToBlockJumpList:
                index = validMoves.index(move)
                validMovesScores[index] += 4
##            print("Heuristic #6!")
##            move = moveToBlockJumpList[random.randrange(0,len(moveToBlockJumpList))]
        if moveToEvadeJumpList != []:
            for move in moveToEvadeJumpList:
                index = validMoves.index(move)
                validMovesScores[index] += 3
##            print("Heuristic #7!")
##            move = moveToEvadeJumpList[random.randrange(0,len(moveToEvadeJumpList))]
        if moveToForceJumpOutOfKingList != []:
            for move in moveToForceJumpOutOfKingList:
                index = validMoves.index(move)
                validMovesScores[index] += 6
##            print("Heuristic #8!")
##            move = moveToForceJumpOutOfKingList[random.randrange(0,len(moveToForceJumpOutOfKingList))]
        if moveToSideSquareList != []:
            for move in moveToSideSquareList:
                index = validMoves.index(move)
                validMovesScores[index] += 1
##            print("Heuristic #9!")
##            move = moveToSideSquareList[random.randrange(0,len(moveToSideSquareList))]
        if movesIntoSafeSpotList != []:
            for move in movesIntoSafeSpotList:
                index = validMoves.index(move)
                validMovesScores[index] += 6
##            print("Heuristic #11!")
##            move = movesIntoSafeSpotList[random.randrange(0,len(movesIntoSafeSpotList))]
##            if DEBUG:print("MADE SAFE MOVE")
##            if DEBUG:print(movesIntoSafeSpotList)
##            time.sleep(.8)
        if moveNotKingRowList != []:
            for move in moveNotKingRowList:
                index = validMoves.index(move)
                validMovesScores[index] += 4
##            print("Heuristic #10!")
##            move = moveNotKingRowList[random.randrange(0,len(moveNotKingRowList ))]
        maxScore = max(validMovesScores)
        if maxScore != 0:
##            print("Max Score =",maxScore)
            move = validMoves[validMovesScores.index(maxScore)]
        else:
            move=validMoves[random.randrange(0,len(validMoves))]
    else:
        if jumpsIntoKingRowList !=[]:
##            print("Heuristic #2!")
            move=jumpsIntoKingRowList[random.randrange(0,len(jumpsIntoKingRowList))]
        elif jumpsFromPossibleJumpList !=[]:
##            print("Heuristic #3!")
            move=jumpsFromPossibleJumpList[random.randrange(0,len(jumpsFromPossibleJumpList))]
        elif jumpsIntoSideSquareList !=[]:
##            print("Heuristic #4!")
            move=jumpsIntoSideSquareList[random.randrange(0,len(jumpsIntoSideSquareList))]
        elif jumpsIntoSafeSpotList != []:
##            print("Heuristic #1!")
            move=jumpsIntoSafeSpotList[random.randrange(0,len(jumpsIntoSafeSpotList))]
        else:
            move=validJumps[random.randrange(0,len(validJumps))]
    return move
