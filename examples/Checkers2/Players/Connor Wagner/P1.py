print ('Connor Wagner')
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

def countPieces(board,tokens):
    count = 0
    for row in board:
        for space in row:
            if space in tokens:
                count += 1
    return count

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
        for jmp in enemyJumps:
            if between(jmp,mv[3:5]):
                if mv in lst:
                    lst.remove(mv)
    return lst

# Heuristic 6
def getBackRowMoves(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    lst = list()
    for mv in validMoves:
        fromRow = ord(mv[0])-65
        fromCol = int(mv[1])
        king = board[fromRow][fromCol] == board[fromRow][fromCol].lower()
        if not king and (fromRow == 0 or fromRow == 7):
            lst.append(mv)
    return lst

# Heuristic 7
def getMovesTowardJumps(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    enemyIndex,enemySymbols,mySymbols,enemyRowInc=swapPlayer(playerIndex)
    lst=list()
    for mv in validMoves:
        #As though we were going to make the move . . .
        fromRow=ord(mv[0:1])-65
        fromCol=int(mv[1:2])
        toRow=ord(mv[3:4])-65
        toCol=int(mv[4:5])
        testBoard=copy.deepcopy(board)
        testBoard[toRow][toCol]=testBoard[fromRow][fromCol]
        testBoard[fromRow][fromCol]=0
        tmp=listValidJumps(testBoard,playerIndex,playerTokens,opponentTokens,rowInc)
        if len(tmp) > len(validJumps):
            lst.append(mv)
    return lst

# Heuristic 8
def getMovesToEdge(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    lst = list()
    for move in validMoves:
        if int(move[4]) == 0 or int(move[4]) == 7:
            lst.append(move)
    return lst

# Heuristic 9
def getMovesToBlock(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    enemyIndex,enemySymbols,mySymbols,enemyRowInc=swapPlayer(playerIndex)
    lst=list()
    for mv in validMoves:
        #As though we were going to make the move . . .
        fromRow=ord(mv[0:1])-65
        fromCol=int(mv[1:2])
        toRow=ord(mv[3:4])-65
        toCol=int(mv[4:5])
        testBoard=copy.deepcopy(board)
        enemyJumpsInitial = listValidJumps(testBoard,enemyIndex,opponentTokens,playerTokens,rowInc)
        testBoard[toRow][toCol]=testBoard[fromRow][fromCol]
        testBoard[fromRow][fromCol]=0
        enemyJumpsFinal = listValidJumps(testBoard,enemyIndex,opponentTokens,playerTokens,rowInc)
        if len(enemyJumpsFinal) < len(enemyJumpsInitial):
            lst.append(mv)
    return lst

# Heuristic 10
def getMovesTowardsEnemyPieces(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    indices = list()
    enemyIndices = list()
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] in playerTokens:
                indices.append([row,col])
            elif board[row][col] in opponentTokens:
                enemyIndices.append([row,col])
    enemyRows = 0
    enemyCols = 0
    playerRows = 0
    playerCols = 0
    count = 0
    for point in indices:
        for enPt in enemyIndices:
            count += 1
            enemyRows += enPt[0]
            enemyCols += enPt[1]
            playerRows += point[0]
            playerCols += point[1]
    enemyRows //= count
    enemyCols //= count
    playerRows //= count
    playerCols //= count
    rowsDir = enemyRows - playerRows
    colsDir = enemyCols - playerCols
    lst = list()
    for move in validMoves:
        fromRow=ord(move[0:1])-65
        fromCol=int(move[1:2])
        toRow=ord(move[3:4])-65
        toCol=int(move[4:5])
        if (rowsDir < 0) == (toRow-fromRow < 0) and (colsDir < 0) == (toCol-fromCol < 0):
            lst.append(move)
    return lst

def getKingMovesTowardsCenterOfBoard(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    retList = list()
    for move in validMoves:
        fromRow=ord(move[0:1])-65
        fromCol=int(move[1:2])
        toRow=ord(move[3:4])-65
        toCol=int(move[4:5])
        if board[fromRow][fromCol].upper() == board[fromRow][fromCol]:
            if fromRow < 4:
                if toRow - fromRow > 0:
                    retList.append(move)
            else:
                if toRow - fromRow < 0:
                    retList.append(move)
    return retList

def getMovesTowardsCenterOfBoard(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    retList = list()
    for move in validMoves:
        fromRow=ord(move[0:1])-65
        fromCol=int(move[1:2])
        toRow=ord(move[3:4])-65
        toCol=int(move[4:5])
        if board[fromRow][fromCol].lower() == board[fromRow][fromCol]:
            if fromRow < 4:
                if toRow - fromRow > 0:
                    retList.append(move)
            else:
                if toRow - fromRow < 0:
                    retList.append(move)
    return retList

def getMovesUsingKings(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    retList = list()
    for move in validMoves:
        fromRow=ord(move[0:1])-65
        fromCol=int(move[1:2])
        toRow=ord(move[3:4])-65
        toCol=int(move[4:5])
        if board[fromRow][fromCol].upper() == board[fromRow][fromCol]:
            retList.append(move)
    return retList

def getMovesNotUsingKings(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    retList = list()
    for move in validMoves:
        fromRow=ord(move[0:1])-65
        fromCol=int(move[1:2])
        toRow=ord(move[3:4])-65
        toCol=int(move[4:5])
        if board[fromRow][fromCol].lower() == board[fromRow][fromCol]:
            retList.append(move)
    return retList

def getMovesNotFromBackRow(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    retList = list()
    for move in validMoves:
        fromRow=ord(move[0:1])-65
        fromCol=int(move[1:2])
        king = board[fromRow][fromCol] == board[fromRow][fromCol].upper()
        if king or not (fromRow == 0 or fromRow == 7):
            retList.append(move)
    return retList

"""1) If jumps are present, select a jump that does not leave your checker
in a position where it will be jumped in turn
2) If jumps are present, and a jump into the king row is possible, take it
3) If jumps are present, and a jump resulting in the prevention of one your
checkers being jumped is possible, take it
4) If jumps are present, and a jump into a side square is possible, take it.
5) If only a move is possible, and a move into the king row is possible, take it.
6) Not move out of the back row unless required to
7) Take a move that will give the player a jump on the next move
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

    jumpsIntoSafeSpotList=jumpsIntoSafeSpot(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    jumpsIntoKingRowList=jumpsIntoKingRow(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    jumpsFromPossibleJumpList=jumpsFromPossibleJump(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    jumpsIntoSideSquareList=jumpsIntoSideSquare(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    movesNotFromBackRow=getMovesNotFromBackRow(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)

    numPieces = countPieces(board,playerTokens)
    enemyPieces = countPieces(board,opponentTokens)

    if len(validJumps)==0:
        if len(movesNotFromBackRow) > 0:
            movesIntoSafeSpotList=movesIntoSafeSpot(movesNotFromBackRow,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
            movesUsingKingsList=getMovesUsingKings(movesIntoSafeSpotList,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
            movesNotUsingKingsList=getMovesNotUsingKings(movesIntoSafeSpotList,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
            movesIntoKingRowList=movesIntoKingRow(movesNotUsingKingsList,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
            safeMovesUsingKingsList=getMovesUsingKings(movesIntoSafeSpotList,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
            movesTowardJumpsList=getMovesTowardJumps(movesIntoSafeSpotList,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
            movesToEdgeList=getMovesToEdge(movesIntoSafeSpotList,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
            movesToBlockList=getMovesToBlock(movesIntoSafeSpotList,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
            movesTowardsEnemyPieces=getMovesTowardsEnemyPieces(movesIntoSafeSpotList,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
            kingMovesTowardsMiddleRow=getKingMovesTowardsCenterOfBoard(movesIntoSafeSpotList,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
            movesTowardsMiddleRow=getMovesTowardsCenterOfBoard(movesIntoSafeSpotList,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
            if len(movesToBlockList) > 0:
                move = movesToBlockList[random.randrange(0,len(movesToBlockList))]
                if DEBUG:print("MADE MOVE TO BLOCK")
            elif len(movesIntoKingRowList) > 0:
                move = movesIntoKingRowList[random.randrange(0,len(movesIntoKingRowList))]
                if DEBUG:print("MADE MOVE TO KING ROW")
            elif len(movesTowardJumpsList) > 0:
                move = movesTowardJumpsList[random.randrange(0,len(movesTowardJumpsList))]
                if DEBUG:print("MADE MOVE TOWARDS JUMP")
            elif len(kingMovesTowardsMiddleRow) > 0:
                move = kingMovesTowardsMiddleRow[random.randrange(0,len(kingMovesTowardsMiddleRow))]
                if DEBUG:print("MADE KING MOVE TOWARDS MIDDLE ROW")
            elif len(movesToEdgeList) > 0:
                move = movesToEdgeList[random.randrange(0,len(movesToEdgeList))]
                if DEBUG:print("MADE MOVE TO EDGE")
            elif len(movesTowardsMiddleRow) > 0:
                move = movesTowardsMiddleRow[random.randrange(0,len(movesTowardsMiddleRow))]
                if DEBUG:print("MADE MOVE TOWARDS MIDDLE ROW")
            elif len(movesIntoSafeSpotList):
                move = movesIntoSafeSpotList[random.randrange(0,len(movesIntoSafeSpotList))]
                if DEBUG:print("MADE SAFE MOVE NOT FROM BACK ROW")
            elif len(movesIntoSafeSpotList) > 0:
                move = movesIntoSafeSpotList[random.randrange(0,len(movesIntoSafeSpotList))]
                if DEBUG:print("MADE SAFE MOVE")
            elif enemyPieces <= 5 and len(movesTowardsEnemyPieces) > 0:
                move = movesTowardsEnemyPieces[random.randrange(0,len(movesTowardsEnemyPieces))]
                if DEBUG:print("MADE MOVE TOWARDS ENEMY PIECE")
            else:
                move=validMoves[random.randrange(0,len(validMoves))]
                if DEBUG:print("MADE RANDOM MOVE")
        else:
            movesIntoSafeSpotList=movesIntoSafeSpot(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
            movesUsingKingsList=getMovesUsingKings(movesIntoSafeSpotList,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
            movesNotUsingKingsList=getMovesNotUsingKings(movesIntoSafeSpotList,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
            movesIntoKingRowList=movesIntoKingRow(movesNotUsingKingsList,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
            safeMovesUsingKingsList=getMovesUsingKings(movesIntoSafeSpotList,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
            movesTowardJumpsList=getMovesTowardJumps(movesIntoSafeSpotList,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
            movesToEdgeList=getMovesToEdge(movesIntoSafeSpotList,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
            movesToBlockList=getMovesToBlock(movesIntoSafeSpotList,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
            movesTowardsEnemyPieces=getMovesTowardsEnemyPieces(movesIntoSafeSpotList,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
            kingMovesTowardsMiddleRow=getKingMovesTowardsCenterOfBoard(movesIntoSafeSpotList,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
            movesTowardsMiddleRow=getMovesTowardsCenterOfBoard(movesIntoSafeSpotList,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
            if len(movesToBlockList) > 0:
                move = movesToBlockList[random.randrange(0,len(movesToBlockList))]
                if DEBUG:print("MADE MOVE TO BLOCK")
            elif len(movesIntoKingRowList) > 0:
                move = movesIntoKingRowList[random.randrange(0,len(movesIntoKingRowList))]
                if DEBUG:print("MADE MOVE TO KING ROW")
            elif len(movesTowardJumpsList) > 0:
                move = movesTowardJumpsList[random.randrange(0,len(movesTowardJumpsList))]
                if DEBUG:print("MADE MOVE TOWARDS JUMP")
            elif len(kingMovesTowardsMiddleRow) > 0:
                move = kingMovesTowardsMiddleRow[random.randrange(0,len(kingMovesTowardsMiddleRow))]
                if DEBUG:print("MADE KING MOVE TOWARDS MIDDLE ROW")
            elif len(movesToEdgeList) > 0:
                move = movesToEdgeList[random.randrange(0,len(movesToEdgeList))]
                if DEBUG:print("MADE MOVE TO EDGE")
            elif len(movesTowardsMiddleRow) > 0:
                move = movesTowardsMiddleRow[random.randrange(0,len(movesTowardsMiddleRow))]
                if DEBUG:print("MADE MOVE TOWARDS MIDDLE ROW")
            elif len(movesIntoSafeSpotList):
                move = movesIntoSafeSpotList[random.randrange(0,len(movesIntoSafeSpotList))]
                if DEBUG:print("MADE SAFE MOVE NOT FROM BACK ROW")
            elif len(movesIntoSafeSpotList) > 0:
                move = movesIntoSafeSpotList[random.randrange(0,len(movesIntoSafeSpotList))]
                if DEBUG:print("MADE SAFE MOVE")
            elif enemyPieces <= 5 and len(movesTowardsEnemyPieces) > 0:
                move = movesTowardsEnemyPieces[random.randrange(0,len(movesTowardsEnemyPieces))]
                if DEBUG:print("MADE MOVE TOWARDS ENEMY PIECE")
            else:
                move=validMoves[random.randrange(0,len(validMoves))]
                if DEBUG:print("MADE RANDOM MOVE")
    else:
        if jumpsIntoKingRowList !=[]:
            move=jumpsIntoKingRowList[random.randrange(0,len(jumpsIntoKingRowList))]
            if DEBUG:print("MADE JUMP TO KING ROW")
        elif jumpsFromPossibleJumpList !=[]:
            move=jumpsFromPossibleJumpList[random.randrange(0,len(jumpsFromPossibleJumpList))]
            if DEBUG:print("MADE JUMP AWAY FROM JUMP")
        elif jumpsIntoSideSquareList !=[]:
            move=jumpsIntoSideSquareList[random.randrange(0,len(jumpsIntoSideSquareList))]
            if DEBUG:print("MADE JUMP TO SIDE")
        elif jumpsIntoSafeSpotList != []:
            move=jumpsIntoSafeSpotList[random.randrange(0,len(jumpsIntoSafeSpotList))]
            if DEBUG:print("MADE JUMP TO SAFE SPOT")
        else:
            move=validJumps[random.randrange(0,len(validJumps))]
            if DEBUG:print("MADE RANDOM JUMP")
    if DEBUG:print(move)
    #time.sleep(.05)
    return move
