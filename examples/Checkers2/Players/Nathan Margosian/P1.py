print ('Nathan Margosian')
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

#*********************************************************************************
#***************************** Heuristics ****************************************
#*********************************************************************************
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

def jumpsIntoSideSquare(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    lst=[]
    for jmp in validJumps:
        if jmp[-1]in ['0','7']:
            lst.append(jmp)
    return lst

def movesIntoKingRow(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    lst=[]
    for mv in validMoves:
        fromRow=ord(mv[0:1])-65
        fromCol=int(mv[1:2])
        if board[fromRow][fromCol] in ["b","r"]:
            if rowInc>0:
                kingRow=7
            else:
                kingRow=0
            for move in validMoves:
                if ord(move[3])-65==kingRow:
                    lst.append(move)
        else:
            lst=[]
    return lst  

  
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

#6
def moveBlockJump(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    enemyIndex,enemySymbols,mySymbols,enemyRowInc=swapPlayer(playerIndex)
    lst=[]
    for mv in validMoves:
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
            for mov in validMoves:
                if mov[3:] == jmp[3:]:
                    lst.append(mov)
    return lst

#7
def moveFromJump(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    enemyIndex,enemySymbols,mySymbols,enemyRowInc=swapPlayer(playerIndex)
    testBoard=copy.deepcopy(board)
    lst=[]
    enemyJumps=listValidJumps(testBoard,enemyIndex,enemySymbols,mySymbols,enemyRowInc)
    #Are any of my starting points the in between point for any of his jumps?
    for move in validMoves:
        for jmpe in enemyJumps:
            if between(jmpe,move[0:2]):
                lst.append(move)
    return lst

#8
def jumpBlockJump(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    enemyIndex,enemySymbols,mySymbols,enemyRowInc=swapPlayer(playerIndex)
    lst=[]
    for jmp in validJumps:
        fromRow=ord(jmp[0:1])-65
        fromCol=int(jmp[1:2])
        toRow=ord(jmp[3:4])-65
        toCol=int(jmp[4:5])
        testBoard=copy.deepcopy(board)
        testBoard[toRow][toCol]=testBoard[fromRow][fromCol]
        testBoard[fromRow][fromCol]=0
        enemyJumps=listValidJumps(testBoard,enemyIndex,enemySymbols,mySymbols,enemyRowInc)
        #if DEBUG:print("ENEMY JUMPS for move",mv,enemyJumps)
        for jmpe in enemyJumps:
            for jmp in validJumps:
                if jmp[3:] != jmp[3:]:
                    last.append(jmp)
    return lst

#9
def moveIntoSide(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    lst=[]
    for move in validMoves:
        if move[-1]in ['0','7']:
            lst.append(move)
    return lst

#10
def notMoveOutOfOwnKingRow(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    if rowInc>0:
        ownkingRow=0
    else:
        ownkingRow=7
    lst=[]
    for move in validMoves:
        if ord(move[0])-65!=ownkingRow:
            lst.append(move)
    return lst

#11
def tradeIfMore(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    countOwn=0
    countEnemy=0
    lst=[]
    enemyIndex,enemySymbols,mySymbols,enemyRowInc=swapPlayer(playerIndex)
    testBoard=copy.deepcopy(board)
    enemyJumps=listValidJumps(testBoard,enemyIndex,enemySymbols,mySymbols,enemyRowInc)
    for i in range(len(board)):
        for x in board[i]:
            if x in playerTokens:
                countOwn+=1
            elif x in opponentTokens:
                countEnemy+=1
    if countOwn > countEnemy:
        for jmp in validJumps:
            for jmpe in enemyJumps:
                if between(jmpe,jmp[-2:]):
                    lst.append(jmp)
    return lst

    
"""1) If jumps are present, select a jump that does not leave your checker
in a position where it will be jumped in turn
2) If jumps are present, and a jump into the king row is possible, take it
3) If jumps are present, and a jump resulting in the prevention of one your
checkers being jumped is possible, take it
4) If jumps are present, and a jump into a side square is possible, take it.
5) If only a move is possible, and a move into the king row is possible, take it.
6) If ony a move is possible, block a possible jump.
7) Make a jump to block a possible jump
8) If about to be jumped, and only move is possible, move into an empty space
9) If only a move is available, move into side square if possible
10) If only moves are possible, and checkers are in your own king row, leave them there if possible
11) (not done for this lab) If more checkers, trade pieces if possible
"""
def getMove(board,playerIndex,playerColors,playerTokens,opponentTokens,rowInc):
    validMoves=listValidMoves(board,playerIndex,playerTokens,opponentTokens,rowInc)
    validJumps=listValidJumps(board,playerIndex,playerTokens,opponentTokens,rowInc)

    oldJumps=validJumps[:]
    newJumps=expandJumps(board,playerIndex,oldJumps,playerTokens,opponentTokens,rowInc)
    while newJumps != oldJumps:
        oldJumps=newJumps[:]
        newJumps=expandJumps(board,playerIndex,oldJumps,playerTokens,opponentTokens,rowInc)
        expandJumpsList=expandJumps(board,playerIndex,oldJumps,playerTokens,opponentTokens,rowInc)
        print('expandJumpsList',expandJumpsList)
    validJumps=newJumps[:]
    print('p1p1',validJumps)
    if DEBUG:print("MOVES:",validMoves)
    if DEBUG:print("JUMPS:",validJumps)

    jumpsIntoSafeSpotList=jumpsIntoSafeSpot(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    jumpsIntoKingRowList=jumpsIntoKingRow(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    jumpsFromPossibleJumpList=jumpsFromPossibleJump(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    jumpsIntoSideSquareList=jumpsIntoSideSquare(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    movesIntoKingRowList=movesIntoKingRow(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    movesIntoSafeSpotList=movesIntoSafeSpot(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    moveBlockJumpList=moveBlockJump(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    jumpBlockJumpList=jumpBlockJump(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    moveFromJumpList=moveFromJump(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    moveIntoSideList=moveIntoSide(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    notMoveOutOfOwnKingRowList = notMoveOutOfOwnKingRow(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    tradeIfMoreList=tradeIfMore(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    expandJumpsList=expandJumps(board,playerIndex,oldJumps,playerTokens,opponentTokens,rowInc)
        

  
    print(len(validJumps))
    if len(validJumps)==0:
        print('move')
        if movesIntoKingRowList != []:
            move = movesIntoKingRowList[random.randrange(0,len(movesIntoKingRowList))]
            print('1')
        elif moveBlockJumpList != []:
            move=moveBlockJumpList[random.randrange(0,len(moveBlockJumpList))]
            print('2')
        elif moveFromJumpList != []:
            move=moveFromJumpList[random.randrange(0,len(moveFromJumpList))]
            print('boner')
        elif moveIntoSideList != []:
            move=moveIntoSideList[random.randrange(0,len(moveIntoSideList))]
            print('4')
        elif movesIntoSafeSpotList != []:
            move = movesIntoSafeSpotList[random.randrange(0,len(movesIntoSafeSpotList))]
            print("MADE SAFE MOVE")
            if DEBUG:print(movesIntoSafeSpotList)
            time.sleep(.8)
        elif notMoveOutOfOwnKingRowList != []:
             move=notMoveOutOfOwnKingRowList[random.randrange(0,len(notMoveOutOfOwnKingRowList))]
             print('5')
        else:
            move=validMoves[random.randrange(0,len(validMoves))]
            print('fuck')
    else:
        if expandJumpsList!=[]:
            move=expandJumpsList[random.randrange(0,len(expandJumpsList))]
        if jumpsIntoKingRowList !=[]:
            move=jumpsIntoKingRowList[random.randrange(0,len(jumpsIntoKingRowList))]
        elif jumpBlockJumpList != []:
            move=jumpBlockJumpList[random.randrange(0,len(jumpBlockJumpList))]
        elif jumpsFromPossibleJumpList !=[]:
            move=jumpsFromPossibleJumpList[random.randrange(0,len(jumpsFromPossibleJumpList))]
        elif tradeIfMoreList != []:
            move=tradeIfMoreList[random.randrange(0,len(tradeIfMore))]
        elif jumpsIntoSideSquareList !=[]:
            move=jumpsIntoSideSquareList[random.randrange(0,len(jumpsIntoSideSquareList))]
        elif jumpsIntoSafeSpotList != []:
            move=jumpsIntoSafeSpotList[random.randrange(0,len(jumpsIntoSafeSpotList))]
        else:
            move=validJumps[random.randrange(0,len(validJumps))]
    return move
