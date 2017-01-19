print ('Chinyi Oh')
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
    if rowInc>0:
        kingRow=7
    else:
        kingRow=0
    lst=[]
    for move in validMoves:
        if ord(move[3])-65==kingRow:
            lst.append(move)
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

#Heuristics #6
#If opponent is going to jump to side square, move to prevent jump
def jumpToPreventSideSquare(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    enemyIndex,enemySymbols,mySymbols,enemyRowInc=swapPlayer(playerIndex)
    lstt=copy.deepcopy(validMoves)
    lst=[]
    for jump in validJumps:
        testBoard=copy.deepcopy(board)
        enemyJumps=listValidJumps(testBoard,enemyIndex,enemySymbols,mySymbols,enemyRowInc)
        for jmp in enemyJumps:
            if jmp[-1] in ['0','7']:
                for jumps in validJumps:
                    if jumps[-1] in ['0','7']:
                        lst.append(jumps)
    return lst

#Heuristics #7
#moves to side square
def movesIntoSideSquare(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    lst=[]
    for move in validMoves:
        if move[-1]in ['0','7']:
            lst.append(move)
    return lst


#Heuristics #8
#Move checker nearest to king row first
def moveNearKingRow(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    if rowInc>0:
        nearKingRow=6
    else:
        nearKingRow=1
    lst=[]
    for move in validMoves:
        if ord(move[3])-65==nearKingRow:
            if ord(board[ord(move[0])-65][int(move[1])])>89:
                lst.append(move)
    return lst

#Heuristics #9
#Jump to prevent enemy jump
def jumpToStopEnemyJump(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    enemyIndex,enemySymbols,mySymbols,enemyRowInc=swapPlayer(playerIndex)
    testBoard=copy.deepcopy(board)
    lst=[]
    enemyJumps=listValidJumps(testBoard,enemyIndex,enemySymbols,mySymbols,enemyRowInc)
    for jmp in validJumps:
        for jmpe in enemyJumps:
            if jmp[-2]==jmpe[-2] and jmp[-1]==jmpe[-1]:
                lst.append(jmp)
    return lst

#Heuristics #9
#Move to prevent enemy jump
def moveToStopEnemyJump(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    enemyIndex,enemySymbols,mySymbols,enemyRowInc=swapPlayer(playerIndex)
    testBoard=copy.deepcopy(board)
    lst=[]
    enemyJumps=listValidJumps(testBoard,enemyIndex,enemySymbols,mySymbols,enemyRowInc)
    for mv in validMoves:
        for jmpe in enemyJumps:
            if mv[-2]==jmpe[-2] and mv[-1]==jmpe[-1]:
                lst.append(mv)
    return lst

#Heuristics #10
#Move towards enemy when near end of game, move two checkers to kill off the other checker
def moveTowardsEnemy(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    lst=[]
    checker=[]
    opponentChecker=[]
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] in playerTokens:
                checker.append(str(row)+str(col))
            elif board[row][col] in opponentTokens:
                opponentChecker.append(str(row)+str(col))
    rowDistance=int(checker[0][0])-int(opponentChecker[0][0])
    colDistance=int(checker[0][1])-int(opponentChecker[0][1])
    if rowDistance>0:
        if colDistance>0:
            move=chr(int(checker[0][0])+65)+checker[0][1]+":"+chr(int(checker[0][0])+64)+str(int(checker[0][1])-1)
        if colDistance<0:
            move=chr(int(checker[0][0])+65)+checker[0][1]+":"+chr(int(checker[0][0])+64)+str(int(checker[0][1])+1)
        if colDistance==0:
            if checker[0][1]!="7":
                move=chr(int(checker[0][0])+65)+checker[0][1]+":"+chr(int(checker[0][0])+64)+str(int(checker[0][1])+1)
            else:
                move=chr(int(checker[0][0])+65)+checker[0][1]+":"+chr(int(checker[0][0])+64)+str(int(checker[0][1])-1)
    if rowDistance<0:
        if colDistance>0:
            move=chr(int(checker[0][0])+65)+checker[0][1]+":"+chr(int(checker[0][0])+66)+str(int(checker[0][1])-1)
        if colDistance<0:
            move=chr(int(checker[0][0])+65)+checker[0][1]+":"+chr(int(checker[0][0])+66)+str(int(checker[0][1])+1)
        if colDistance==0:
            if checker[0][1]!="7":
                move=chr(int(checker[0][0])+65)+checker[0][1]+":"+chr(int(checker[0][0])+66)+str(int(checker[0][1])+1)
            else:
                move=chr(int(checker[0][0])+65)+checker[0][1]+":"+chr(int(checker[0][0])+66)+str(int(checker[0][1])-1)
    if rowDistance==0:
        if checker[0][0]!="0":
            if colDistance>0:
                move=chr(int(checker[0][0])+65)+checker[0][1]+":"+chr(int(checker[0][0])+64)+str(int(checker[0][1])-1)
            if colDistance<0:
                move=chr(int(checker[0][0])+65)+checker[0][1]+":"+chr(int(checker[0][0])+64)+str(int(checker[0][1])+1)
        else:
            if colDistance>0:
                move=chr(int(checker[0][0])+65)+checker[0][1]+":"+chr(int(checker[0][0])+64)+str(int(checker[0][1])-1)
            if colDistance<0:
                move=chr(int(checker[0][0])+65)+checker[0][1]+":"+chr(int(checker[0][0])+64)+str(int(checker[0][1])+1)
    
    return move
    
def countCheckers(board,playerIndex,playerTokens,opponentTokens):
    count=0
    countOpponent=0
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] in playerTokens:
                count+=1
            elif board[row][col] in opponentTokens:
                countOpponent+=1
    return count,countOpponent

"""1) If jumps are present, select a jump that does not leave your checker
in a position where it will be jumped in turn
2) If jumps are present, and a jump into the king row is possible, take it
3) If jumps are present, and a jump resulting in the prevention of one your
checkers being jumped is possible, take it
4) If jumps are present, and a jump into a side square is possible, take it.
5) If only a move is possible, and a move into the king row is possible, take it.
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
    movesIntoSafeSpotList=movesIntoSafeSpot(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)

    jumpToPreventSideSquareList=jumpToPreventSideSquare(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    movesIntoSideSquareList=movesIntoSideSquare(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    moveNearKingRowList=moveNearKingRow(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    jumpToStopEnemyJumpList=jumpToStopEnemyJump(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    moveToStopEnemyJumpList=moveToStopEnemyJump(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    moveTowardsEnemyList=moveTowardsEnemy(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)

    if len(validJumps)==0:
        move=""
        if movesIntoKingRowList != []:
            move = movesIntoKingRowList[random.randrange(0,len(movesIntoKingRowList))]
        elif movesIntoSafeSpotList != []:
            count,countOpponent=countCheckers(board,playerIndex,playerTokens,opponentTokens)
            if count>countOpponent and count+countOpponent<8:
                if moveTowardsEnemyList in movesIntoSafeSpotList:
                    move=moveTowardsEnemyList
                else:
                    move = movesIntoSafeSpotList[random.randrange(0,len(movesIntoSafeSpotList))]
        elif moveToStopEnemyJumpList != []:
            move=moveToStopEnemyJumpList[random.randrange(0,len(moveToStopEnemyJumpList))]
        if move=="":
            if movesIntoSideSquareList != []:
                move=movesIntoSideSquareList[random.randrange(0,len(movesIntoSideSquareList))]
            elif moveNearKingRowList != []:
                move=moveNearKingRowList[random.randrange(0,len(moveNearKingRowList))]
            else:
                move=validMoves[random.randrange(0,len(validMoves))]
    else:
        if jumpsIntoKingRowList !=[]:
            move=jumpsIntoKingRowList[random.randrange(0,len(jumpsIntoKingRowList))]
        elif jumpToStopEnemyJumpList != []:
            move=jumpToStopEnemyJumpList[random.randrange(0,len(jumpToStopEnemyJumpList))]
        elif jumpToPreventSideSquareList != []:
            move=jumpToPreventSideSquareList[random.randrange(0,len(jumpToPreventSideSquareList))]
        elif jumpsFromPossibleJumpList !=[]:
            move=jumpsFromPossibleJumpList[random.randrange(0,len(jumpsFromPossibleJumpList))]
        elif jumpsIntoSideSquareList !=[]:
            move=jumpsIntoSideSquareList[random.randrange(0,len(jumpsIntoSideSquareList))]
        elif jumpsIntoSafeSpotList != []:
            move=jumpsIntoSafeSpotList[random.randrange(0,len(jumpsIntoSafeSpotList))]
        else:
            move=validJumps[random.randrange(0,len(validJumps))]
    return move
