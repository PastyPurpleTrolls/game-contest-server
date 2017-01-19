print ('Jessica Hofmeister')
import time
import random
import copy
import math 
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
    #print(newJumps)
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
        return True
    else:
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
        if ord(move[3])-65==kingRow and board[ord(move[0])-65][int(move[1])] not in ["R","B"]:
            lst.append(move)
    return lst  

    
def movesIntoSafeSpot(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    enemyIndex,enemySymbols,mySymbols,enemyRowInc=swapPlayer(playerIndex)
    movesIntoSafeSpotList=copy.deepcopy(validMoves)
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
                if mv in movesIntoSafeSpotList:
                    movesIntoSafeSpotList.remove(mv)
    return movesIntoSafeSpotList


"""1) If jumps are present, select a jump that does not leave your checker
in a position where it will be jumped in turn
2) If jumps are present, and a jump into the king row is possible, take it
3) If jumps are present, and a jump resulting in the prevention of one your
checkers being jumped is possible, take it
4) If jumps are present, and a jump into a side square is possible, take it.
5) If only a move is possible, and a move into the king row is possible, take it.
"""
#####################################################################################
### HEURISTIC 6 ### creates a list of moves that "run" away from a jump
def moveAwayFromPossibleJump(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
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

### HERISTIC 7 ### creates a list of moves that do not use a checker in the base row(non-kings only)
def findMovesNotInBackRow(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    if rowInc>0:
        opponentKingRow=0
    else:
        opponentKingRow=7
    if rowInc>0:
        nonKingOpponent="b"
    else:
        nonKingOpponent="r"
    moveNotFromBackRowList=[]
    worthIt=False
    for i in range (8):
        if nonKingOpponent in board[i]:
            worthIt=True
            break
    if worthIt==True:
        for move in validMoves:
            if ord(move[0])-65!=opponentKingRow:
                moveNotFromBackRowList.append(move)
    return moveNotFromBackRowList

### HURISTIC 8 ### creates a list of moves that do not use a checker in the base row (non-kings only) and are "safe"
def safeMoveAndProtectedBackRowCombo(movesIntoSafeSpotList,moveNotFromBackRowList):
    safeMoveAndProtectedBackRowComboList=[]
    for move in movesIntoSafeSpotList:
        if move in moveNotFromBackRowList:
            safeMoveAndProtectedBackRowComboList.append(move)
    return safeMoveAndProtectedBackRowComboList

### HURISTIC 9 ### creates a list of jumps that would prevent an oppnent checker from getting kingship 
def preventOpponentFromGettingKing(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    if rowInc>0:
        opponentKingRow=0
    else:
        opponentKingRow=7
    enemyIndex,enemySymbols,mySymbols,enemyRowInc=swapPlayer(playerIndex)
    testBoard=copy.deepcopy(board)
    lst=[]
    enemyMoves=listValidMoves(testBoard,enemyIndex,enemySymbols,mySymbols,enemyRowInc)
    for enemyMove in enemyMoves:
        if ord(enemyMove[-2])-65==opponentKingRow:
            for jump in validJumps:
                if between(jump,enemyMove[0:2]):
                    lst.append(jump)
    return lst

### HURISTIC 10 ### creates a list of moves that would prevent an opponent checker from jumping another one of my checkers
def blockAPieceFromGettingJumped(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    enemyIndex,enemySymbols,mySymbols,enemyRowInc=swapPlayer(playerIndex)
    testBoard=copy.deepcopy(board)
    lst=[]
    enemyJumps=listValidJumps(testBoard,enemyIndex,enemySymbols,mySymbols,enemyRowInc)
    for jump in enemyJumps:
        for blockingMove in validMoves:
            if blockingMove[3:5]==jump[3:5]:
                lst.append(blockingMove)
    #print ("hur 10---",lst)
    return lst

### HUR 11###
def chaseOpponentWithKing(movesIntoSafeSpotList,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    lst=[]
    for move in movesIntoSafeSpotList:
        fromRow=ord(move[0:1])-65
        fromCol=int(move[1:2])
        toRow=ord(move[3:4])-65
        toCol=int(move[4:5])
        if board[fromRow][fromCol] in ["R","B"]:
            testBoard=copy.deepcopy(board)
            testBoard[toRow][toCol]=testBoard[fromRow][fromCol]
            testBoard[fromRow][fromCol]=0
            if toRow<fromRow:
                if toCol<fromCol:
                    rInc=-1
                    cInc=-1
                else:
                    rInc=-1
                    cInc=1
            else:
                if toCol<fromCol:
                    rInc=1
                    cInc=-1
                else:
                    rInc=1
                    cInc=1
            newMove=(chr(toRow+65)+str(toCol)+":"+chr(toRow+(2*rInc)+65)+str(toCol+(2*cInc)))
            otherNewMove=(chr(toRow+65)+str(toCol)+":"+chr(toRow-(2*rInc)+65)+str(toCol-(2*cInc)))
            NewJumps=listValidJumps(testBoard,playerIndex,playerTokens,opponentTokens,rowInc)
            if newMove in NewJumps:
                lst.append(move)
            elif otherNewMove in NewJumps:
                lst.append(move)
    
    return lst

###HUR 12###
def chaseFromFurtherAwayOr(board,opponentTokens,movesIntoSafeSpotList):
    listOfOpponentPositions=[]
    lenD={}
    values=[]
    lst=[]
    for row in range (8):
        for col in range (8):
            if board[row][col] in opponentTokens:
                listOfOpponentPositions.append(chr(row+65)+str(col))
    for itm in listOfOpponentPositions:
        lenD[itm]={}
        for move in movesIntoSafeSpotList:
            lengthFromCheck = math.sqrt((ord(move[3])-ord(itm[0]))**2+(int(move[4])-int(itm[1]))**2)
            lenD[itm][move]=(lengthFromCheck)
        values.append(list(lenD[itm].values()))
    minLength=min(values)
    if len(minLength)>1:
        minMinLength=min(minLength)
        for itm in lenD:
            for move in lenD[itm]:
                if lenD[itm][move]==minMinLength:
                    lst.append(move)
    else:
        for itm in lenD:
            for move in lenD[itm]:
                if lenD[itm][move]==minLength:
                    lst.append(move)
    return lst

###HUR 13###
def pickLongestJump(validJumps):
    lst=[]
    for jump in range(len(validJumps)):
         if len(validJumps[jump])>5:
             lst.append(validJumps[jump])
    return lst

### HUR 14###
def movesThatDontCreatAJump(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    lst=[]
    enemyIndex,enemySymbols,mySymbols,enemyRowInc=swapPlayer(playerIndex)
    movesIntoSafeSpotList=copy.deepcopy(validMoves)
    enemyJumps=listValidJumps(board,enemyIndex,enemySymbols,mySymbols,enemyRowInc)
    for mv in validMoves:
        #As though we were going to make the move . . .
        fromRow=ord(mv[0:1])-65
        fromCol=int(mv[1:2])
        toRow=ord(mv[3:4])-65
        toCol=int(mv[4:5])
        testBoard=copy.deepcopy(board)
        testBoard[toRow][toCol]=testBoard[fromRow][fromCol]
        testBoard[fromRow][fromCol]=0
        newEnemyJumps=listValidJumps(testBoard,enemyIndex,enemySymbols,mySymbols,enemyRowInc)
        if enemyJumps==newEnemyJumps:
            lst.append(mv)
    return lst
####### 15 *********************
def dontCreateAJumpAndDontGetJumpedCombo(movesThatDontCreatAJumpList,moveFromPossibleJumpsList):
    lst=[]
    for move in movesThatDontCreatAJumpList:
        if move in moveFromPossibleJumpsList:
            lst.append(move)
    return lst
#####
def dontCreateAJumpAndDontGetJumpedComboDelux(dontCreateAJumpAndDontGetJumpedComboList,chaseFromFurtherAwayListOr):
    lst=[]
    for move in chaseFromFurtherAwayListOr:
        if move in dontCreateAJumpAndDontGetJumpedComboList:
            lst.append(move)
    return lst
#############################################################################################
                    
def getMove(board,playerIndex,playerColors,playerTokens,opponentTokens,rowInc):
    validMoves=listValidMoves(board,playerIndex,playerTokens,opponentTokens,rowInc)
    validJumps=listValidJumps(board,playerIndex,playerTokens,opponentTokens,rowInc)

    oldJumps=validJumps[:]
    newJumps=expandJumps(board,playerIndex,oldJumps,playerTokens,opponentTokens,rowInc)
    while newJumps != oldJumps:
        oldJumps=newJumps[:]
        newJumps=expandJumps(board,playerIndex,oldJumps,playerTokens,opponentTokens,rowInc)
    validJumps=newJumps[:]
   
    jumpsIntoSafeSpotList=jumpsIntoSafeSpot(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    jumpsIntoKingRowList=jumpsIntoKingRow(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    jumpsFromPossibleJumpList=jumpsFromPossibleJump(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    jumpsIntoSideSquareList=jumpsIntoSideSquare(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    movesIntoKingRowList=movesIntoKingRow(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    movesIntoSafeSpotList=movesIntoSafeSpot(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    moveFromPossibleJumpsList=moveAwayFromPossibleJump(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    moveNotFromBackRowList=findMovesNotInBackRow(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    safeMoveAndProtectedBackRowComboList=safeMoveAndProtectedBackRowCombo(movesIntoSafeSpotList,moveNotFromBackRowList)
    preventKingshipList=preventOpponentFromGettingKing(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    movesThatBlockJumpsList=blockAPieceFromGettingJumped(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    chaseOpponentWithKingList=chaseOpponentWithKing(movesIntoSafeSpotList,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    pickLongestJumpList=pickLongestJump(validJumps)
    chaseFromFurtherAwayListOr=chaseFromFurtherAwayOr(board,opponentTokens,movesIntoSafeSpotList)
    movesThatDontCreatAJumpList=movesThatDontCreatAJump(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    dontCreateAJumpAndDontGetJumpedComboList=dontCreateAJumpAndDontGetJumpedCombo(movesThatDontCreatAJumpList,moveFromPossibleJumpsList)
    dontCreateAJumpAndDontGetJumpedComboDeluxList=dontCreateAJumpAndDontGetJumpedComboDelux(dontCreateAJumpAndDontGetJumpedComboList,chaseFromFurtherAwayListOr)
      
    if len(validJumps)==0:
        if movesIntoKingRowList != []:
            move = movesIntoKingRowList[random.randrange(0,len(movesIntoKingRowList))]
        elif movesThatBlockJumpsList != []:
            move = movesThatBlockJumpsList[random.randrange(0,len(movesThatBlockJumpsList))]
            if DEBUG:print("hur 10 worked")
        elif dontCreateAJumpAndDontGetJumpedComboList != []:
            move=dontCreateAJumpAndDontGetJumpedComboList[random.randrange(0,len(dontCreateAJumpAndDontGetJumpedComboList))]
        elif moveFromPossibleJumpsList != []:
            move = moveFromPossibleJumpsList[random.randrange(0,len(moveFromPossibleJumpsList))]
            if DEBUG:print("Hur 6 worked")
        elif dontCreateAJumpAndDontGetJumpedComboDeluxList != []:
            move = dontCreateAJumpAndDontGetJumpedComboDeluxList[random.randrange(0,len(dontCreateAJumpAndDontGetJumpedComboDeluxList))]
        elif chaseOpponentWithKingList != []:
            move = chaseOpponentWithKingList[0]
            if DEBUG:print("I DID IT")
        elif chaseFromFurtherAwayListOr != []:
            move = chaseFromFurtherAwayListOr[0]
        elif movesThatDontCreatAJumpList !=[]:
            move = movesThatDontCreatAJumpList[random.randrange(0,len(movesThatDontCreatAJumpList))]
        elif safeMoveAndProtectedBackRowComboList != []:
            move = safeMoveAndProtectedBackRowComboList[random.randrange(0,len(safeMoveAndProtectedBackRowComboList))]
            if DEBUG:print("combo worked")
        elif movesIntoSafeSpotList != []:
            move = movesIntoSafeSpotList[random.randrange(0,len(movesIntoSafeSpotList))]
            time.sleep(0)
        elif moveNotFromBackRowList != []:
            move = moveNotFromBackRowList[random.randrange(0,len(moveNotFromBackRowList))]
            if DEBUG:print("hur 7 worked")
        else:
            move=validMoves[random.randrange(0,len(validMoves))]
    else:
        if jumpsIntoKingRowList !=[]:
            move=jumpsIntoKingRowList[random.randrange(0,len(jumpsIntoKingRowList))]
        elif preventKingshipList !=[]:
            move=preventKingshipList[random.randrange(0,len(preventKingshipList))]
        elif jumpsFromPossibleJumpList !=[]:
            move=jumpsFromPossibleJumpList[random.randrange(0,len(jumpsFromPossibleJumpList))]
        elif jumpsIntoSideSquareList !=[]:
            move=jumpsIntoSideSquareList[random.randrange(0,len(jumpsIntoSideSquareList))]
        elif jumpsIntoSafeSpotList != []:
            move=jumpsIntoSafeSpotList[random.randrange(0,len(jumpsIntoSafeSpotList))]
        elif pickLongestJumpList !=[]:
            move=pickLongestJumpList[random.randrange(0,len(pickLongestJumpList))]
        else:
            move=validJumps[random.randrange(0,len(validJumps))]
    return move
