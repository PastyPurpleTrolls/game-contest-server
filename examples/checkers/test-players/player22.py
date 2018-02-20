#Checkers Player
#12/12/12
import time
import random
import copy

EMPTY=0
INCs=[-1,1]
VALID_RANGE=range(8)
DEBUG=False
VISIBLE=True

#Makes a list of valid moves based upon the board state
#@param CB The current board state
#@param player Unused param, so I cannot say what this is for
#@param playerTokens The list of two characters that are used to indicate the player's pieces
#@param opponentTokens The list of two characters that are used to indicate the opponent's pieces
#@param rowInc Either a 1 or a -1, used to determine the direction that the player's pieces are going
#@return The list of valid moves
def listValidMoves(CB,player, playerTokens,opponentTokens,rowInc):
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

#Makes a list of valid jumps based upon the board state
#@param CB The current board state
#@param player Unused param, so I cannot say what this is for
#@param playerTokens The list of two characters that are used to indicate the player's pieces
#@param opponentTokens The list of two characters that are used to indicate the opponent's pieces
#@param rowInc Either a 1 or a -1, used to determine the direction that the player's pieces are going
#@return The list of valid jumps
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

#Gets a manual move (unused in the automated player)
#@param validMoves The list of the player's valid moves
#@param validJumps The list of the player's valid jumps
#@param playerIndex The current player's index
#@param playerColors A list of the two players' colors
#@return The move inputted
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

#Expands the old jumps to include multiple jumps
#@param CB The current board state
#@param player Unused param, so I cannot say what this is for
#@param oldJumps The inputted list of old jumps
#@param playerTokens The list of two characters that are used to indicate the player's pieces
#@param opponentTokens The list of two characters that are used to indicate the opponent's pieces
#@param rowInc Either a 1 or a -1, used to determine the direction that the player's pieces are going
#@return The new list of valid jumps
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
#************************* Heuristics Helpers ************************************
#*********************************************************************************

#Checks to see if a checker is between a checker and an open spot
#@param jmp The inputted jump
#@param location The inputted location
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

#Checks to see if the spot is safe (for use by the isCheckersSafe method)
#@param row The row of the piece being checked
#@param col The column of the piece being checked
#@param opponentTokens The list of two characters that are used to indicate the opponent's pieces
#@param rowInc The direction that the other player's pieces are moving
#@param board The board's current state
def checkSpot(row, col, opponentTokens, rowInc, board):
    safe = True
    if(row + rowInc in VALID_RANGE and col + 1 in VALID_RANGE and board[row+rowInc][col+1] in opponentTokens):
        if(row - rowInc in VALID_RANGE and col - 1 in VALID_RANGE and board[row-rowInc][col-1] == 0):
            safe = False
    if(row + rowInc in VALID_RANGE and col - 1 in VALID_RANGE and board[row+rowInc][col-1] in opponentTokens):
        if(row - rowInc in VALID_RANGE and col + 1 in VALID_RANGE and board[row-rowInc][col+1] == 0):
            safe = False
    if(row - rowInc in VALID_RANGE and col + 1 in VALID_RANGE and board[row-rowInc][col+1] == opponentTokens[1]):
        if(row + rowInc in VALID_RANGE and col - 1 in VALID_RANGE and board[row+rowInc][col-1] == 0):
            safe = False
    if(row - rowInc in VALID_RANGE and col - 1 in VALID_RANGE and board[row-rowInc][col-1] == opponentTokens[1]):
        if(row + rowInc in VALID_RANGE and col + 1 in VALID_RANGE and board[row+rowInc][col+1] == 0):
            safe = False
    return safe

#Swaps the players
#@param playerIndex The player's index
#@return The player index, The player's symbols, The oponent's symbols, The row increment
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

#Gets the move values for various heuristics
#@param move The inputted move
#@return The row the checker is coming from, the column the checker is coming from, the row the checker is going to, the column the checker is going to
def getMoveVals(move):
    fromRow=ord(move[0:1])-65
    fromCol=int(move[1:2])
    toRow=ord(move[3:4])-65
    toCol=int(move[4:5])
    return fromRow, fromCol, toRow, toCol

#*********************************************************************************
#***************************** Heuristics ****************************************
#*********************************************************************************

#Checks to see if the checker is safe (Heuristics 1 & 3)
#@param move The inputted move
#@param playerTokens The list of two characters that are used to indicate the player's pieces
#@param opponentTokens The list of two characters that are used to indicate the opponent's pieces
#@param rowInc The direction the player checkers are headed
#@param board The current board state
#@return ((True if the spot is safe, False otherwise),(True if the place being moved to is safe, False otherwise))
def isCheckerSafe(move, playerTokens, opponentTokens, rowInc, board):
    fromRow, fromCol, toRow, toCol = getMoveVals(move)
    safeSpot = checkSpot(fromRow, fromCol, opponentTokens, rowInc, board)
    safeMove = True
    if(toRow - fromRow >= 2 or toCol - fromCol >= 2):
        newBoard = copy.deepcopy(board)
        newBoard[int((fromRow+toRow)/2)][int((fromCol+toCol)/2)] = 0
        safeMove = checkSpot(toRow, toCol, opponentTokens, rowInc, newBoard)
    else:
        newBoard = copy.deepcopy(board)
        newBoard[fromRow][fromCol] = 0
        safeMove = checkSpot(toRow, toCol, opponentTokens, rowInc, newBoard)
    return (safeSpot, safeMove)

#Checks to see if the checker is moving to a king spot (Heuristics 2 &  5)
#@param move The inputted move
#@param playerTokens The player's tokens
#@param playerIndex The player's index
#@param board The board state
def movesToKingSpot(move, playerTokens, playerIndex, board):
    fromRow, fromCol, toRow, toCol = getMoveVals(move)
    if(toRow == 0 and playerIndex == 1 and board[fromRow][fromCol] == playerTokens[0]):
        return True
    elif(toRow == 7 and playerIndex == 0 and board[fromRow][fromCol] == playerTokens[0]):
        return True
    return False

#Checks to see if it moves the checker into a side square (Heuristic 4)
#@param moveTo The inputted move
#@return True if it moves into a side square, False otherwise
def movesIntoSideSquare(moveTo):
    if(moveTo[4] == 7 or moveTo[4] == 0):
       return True
    return False

#Checks to see if the checker is in the back row (Heuristic 6)
#@param move The inputted move
#@param playerIndex The index of the current player
#@return True if the checker is in the back row, False otherwise
def inBackRow(move, playerIndex):
    fromRow, fromCol, toRow, toCol = getMoveVals(move)
    if(fromRow == 7 and playerIndex == 1 or fromRow == 0 and playerIndex == 0):
        return True
    return False

#Checks to see if the checker has multiple jumps (Heuristic 7)
#@param move The inputted move
#@return The interger modification based upon a move
def numJumpsWithWeighting(move):
    return (len(move)-5)*2

#Checks to see if the checker is currently in a side square (Heuristic 8)
#@param move The inputted move
#@return True if the checker is in a side square, False otherwise
def inSideSquare(move):
    if(move[1] == 7 or move[1] == 0):
       return True
    return False

#Checks to see if making a move would block the opponent's checker (Heuristic 9)
#@param move The inputted move
#@param board The current board state
#@param playerToken The player's token
#@param opponentToken The opponent's token
#@param rowInc The row incrementor determining your direction
def blocksOppJumps(move, board, playerTokens, opponentTokens, rowInc):
    fromRow, fromCol, toRow, toCol = getMoveVals(move)
    safeBefore = []
    newBoard = copy.deepcopy(board)
    newBoard[toRow][toCol] = newBoard[fromRow][fromCol]
    newBoard[fromRow][fromCol] = 0
    safeNow = []
    if(toRow + 1 in VALID_RANGE and toCol + 1 in VALID_RANGE and board[toRow+1][toCol+1] in playerTokens):
        safeBefore += [checkSpot(toRow+1, toCol+1, opponentTokens, rowInc, board)]
        safeNow += [checkSpot(toRow+1, toCol+1, opponentTokens, rowInc, newBoard)]
    if(toRow - 1 in VALID_RANGE and toCol + 1 in VALID_RANGE and board[toRow-1][toCol+1] in playerTokens):
        safeBefore += [checkSpot(toRow-1, toCol+1, opponentTokens, rowInc, board)]
        safeNow += [checkSpot(toRow-1, toCol+1, opponentTokens, rowInc, newBoard)]
    if(toRow + 1 in VALID_RANGE and toCol - 1 in VALID_RANGE and board[toRow+1][toCol-1] in playerTokens):
        safeBefore += [checkSpot(toRow+1, toCol-1, opponentTokens, rowInc, board)]
        safeNow += [checkSpot(toRow+1, toCol-1, opponentTokens, rowInc, newBoard)]
    if(toRow - 1 in VALID_RANGE and toCol - 1 in VALID_RANGE and board[toRow-1][toCol-1] in playerTokens):
        safeBefore += [checkSpot(toRow-1, toCol-1, opponentTokens, rowInc, board)]
        safeNow += [checkSpot(toRow-1, toCol-1, opponentTokens, rowInc, newBoard)]
    for i in range(len(safeNow)):
        if(safeBefore[i] == False and safeNow[i] == True):
            return True
    return False

#Check to see if making a move would give the opponent a double jump (Heuristic 10)
#@param move The inputted move
#@param playerIndex The player's index
#@param board The current board state
#@param movementTypeMethod Either listValidJumps or listValidMoves depending upon if it's testing for jumps or moves
def oppDoubleJump(move, playerIndex, board, movementTypeMethod):
    fromRow, fromCol, toRow, toCol = getMoveVals(move)
    playerIndex, playerTokens, opponentTokens, rowInc = swapPlayer(playerIndex)
    newBoard = copy.deepcopy(board)
    newBoard[toRow][toCol] = newBoard[fromRow][fromCol]
    newBoard[fromRow][fromCol] = 0
    opponentMovesBefore = listValidJumps(board, playerIndex, playerTokens, opponentTokens, rowInc)
    opponentMovesAfter = listValidJumps(newBoard, playerIndex, playerTokens, opponentTokens, rowInc)
    maxJumpsBefore = 0
    maxJumpsAfter = 0
    for i in range(len(opponentMovesBefore)):
        if(len(opponentMovesBefore[i]) > maxJumpsBefore):
            maxJumpsBefore = len(opponentMovesBefore[i])
    for i in range(len(opponentMovesAfter)):
        if(len(opponentMovesAfter) > i and len(opponentMovesAfter[i]) > maxJumpsAfter):
           maxJumpsAfter = len(opponentMovesAfter[i])
    if(maxJumpsAfter > maxJumpsBefore):
        return True
    return False

#Checks to see if making a move would allow you to jump another piece next turn
#@param move The inputted move
#@param playerIndex The player's index
#@param board The current board state
#@param movementTypeMethod Either listValidJumps or listValidMoves depending upon if it's testing for jumps or moves
def jumpNextMove(move, playerIndex, board, playerTokens, opponentTokens, rowInc):
    fromRow, fromCol, toRow, toCol = getMoveVals(move)
    newBoard = copy.deepcopy(board)
    newBoard[toRow][toCol] = newBoard[fromRow][fromCol]
    newBoard[fromRow][fromCol] = 0
    newJumps = listValidJumps(newBoard, playerIndex, playerTokens, opponentTokens, rowInc)
    isGood = False
    for i in range(len(newJumps)):
        if(newJumps[i][0:2] == move[3:5]):
            isGood = True
    playerIndex, playerTokens, opponentTokens, rowInc = swapPlayer(playerIndex)
    newJumpsOpp = listValidJumps(newBoard, playerIndex, playerTokens, opponentTokens, rowInc)
    playerIndex, playerTokens, opponentTokens, rowInc = swapPlayer(playerIndex)
    if(len(newJumpsOpp) > 0):
        isSafe = False
    else:
        isSafe = True
    for i in range(len(newJumpsOpp)):
        if(checkSpot(toRow, toCol, playerTokens, rowInc, newBoard)):
            ifSafe = True
    if(isSafe and isGood):
        return True
    return False

"""
1)  If jumps are present, select a jump that does not leave your checker
in  a position where it will be jumped in turn
2)  If jumps are present, and a jump into the king row is possible, take it
3)  If jumps are present, and a jump resulting in the prevention of one your
checkers being jumped is possible, take it
4)  If jumps are present, and a jump into a side square is possible, take it.
5)  If only a move is possible, and a move into the king row is possible, take it.
6)  Unless it is the only possible move, if jumps or moves are possible and the checker is in the back row, do not take it.
7)  Double jumps take precedence over single jumps
8)  If a move taking a checker out of a side square is possible, it is discouraged.
9)  If a move prevents one of your checkers from being jumped, take it.
10) If a move causes your checkers to be multiple jumped, it is heavily discouraged.
"""

#Returns a move to the main checkers runner
#@param board The current board state
#@param playerIndex The index of the player
#@param playerColors A list of the players' colors
#@param playerTokens The list of two characters that are used to indicate the player's pieces
#@param opponentTokens The list of two characters that are used to indicate the opponent's pieces
#@param rowInc Either a 1 or a -1, used to determine the direction that the player's pieces are going
#@return The checkers move
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
    return moveMaker(board,playerIndex,playerColors,playerTokens,opponentTokens,rowInc, validJumps, validMoves)

#Makes the move based upon priority and returns it
#@param board The current board state
#@param playerIndex The index of the player
#@param playerColors A list of the players' colors
#@param playerTokens The list of two characters that are used to indicate the player's pieces
#@param opponentTokens The list of two characters that are used to indicate the opponent's pieces
#@param rowInc Either a 1 or a -1, used to determine the direction that the player's pieces are going
#@param validJumps A list of the player's valid jumps
#@param validMoves A list of the player's valid moves
def moveMaker(board, playerIndex, playerColors, playerTokens,opponentTokens, rowInc, validJumps, validMoves):
    if len(validJumps)==0:
        movePriority = validMoves[:]
        maxMovePriority = -255
        for i in range(len(validMoves)):
            movePriority[i] = 0
            #Checks if the player will move to a safe spot (Heuristic 5)
            if(movesToKingSpot(validMoves[i], playerTokens, playerIndex, board) == True):
                movePriority[i] += 2
            #Checks if the checker will move into a side square (Heuristic 4)
            if(movesIntoSideSquare(validMoves[i]) == True):
                movePriority[i] += 1
            #Checks for safety of various states the checkers could be in (Heuristic 1)
            if(isCheckerSafe(validMoves[i], playerTokens, opponentTokens, rowInc, board) == (False, True)):
                movePriority[i] += 4
            if(isCheckerSafe(validMoves[i], playerTokens, opponentTokens, rowInc, board) == (True, False)):
                movePriority[i] -= 5
            #Checks if the checker is in the back row, decreases move priority if true (Heuristic 6)
            if(inBackRow(validMoves[i], playerIndex)):
                movePriority[i] -= 2
            #Checks if the checker is in the side square (Heuristic 8)
            if(inSideSquare(validMoves[i])):
                movePriority[i] -= 2
            #Checks if checker can block the opponent's jump (Heuristic 9)
            if(blocksOppJumps(validMoves[i], board, playerTokens, opponentTokens, rowInc) == True):
                movePriority[i] += 5
            #Checks if the move will allow an opponent multiple jump
            if(oppDoubleJump(validMoves[i], playerIndex, board, listValidMoves) == True):
                movePriority[i] -= 20
            #Checks if a checker can make a jump next move based upon
            if(jumpNextMove(validMoves[i], playerIndex, board, playerTokens, opponentTokens, rowInc)):
                movePriority[i] += 3
            #Makes the max move priority equal to the largest move priority
            if(movePriority[i] > maxMovePriority):
                maxMovePriority = movePriority[i]
        newMoveList = []
        for i in range(len(validMoves)):
            if(maxMovePriority == movePriority[i]):
                newMoveList += [validMoves[i]]
        move=newMoveList[random.randint(0,len(newMoveList)-1)]
    else:
        movePriority = validJumps[:]
        maxMovePriority = -255
        for i in range(len(validJumps)):
            movePriority[i] = 0
            #Checks if the move would put a piece into a king spot (Heuristic 2)
            if(movesToKingSpot(validJumps[i], playerTokens, playerIndex, board) == True):
                movePriority[i] += 2
            #Checks if the move would put a piece into a side square (Heuristic 4)
            if(movesIntoSideSquare(validJumps[i]) == True):
                movePriority[i] += 1
            #Checks for safety of various states the checker could be in (Heuristic 3)
            if(isCheckerSafe(validJumps[i], playerTokens, opponentTokens, rowInc, board) == (False, True)):
                movePriority[i] += 4
            if(isCheckerSafe(validJumps[i], playerTokens, opponentTokens, rowInc, board) == (True, False)):
                movePriority[i] -= 5
            #Checks if the checker is in the back row, decreases move priority if true (Heuristic 6)
            if(inBackRow(validJumps[i], playerIndex)):
                movePriority[i] -= 2
            #Checks if the checker is in the side square (Heuristic 8)
            if(inSideSquare(validJumps[i])):
                movePriority[i] -= 2
            #Checks if the checker can block the opponent's jump (Heuristic 9)
            if(blocksOppJumps(validJumps[i], board, playerTokens, opponentTokens, rowInc) == True):
                movePriority[i] += 6
            #Adds move priority to jumps based on how many jumps there are
            movePriority[i] += numJumpsWithWeighting(validJumps[i])
            #Checks if the move will allow an opponent multiple jump
            if(oppDoubleJump(validJumps[i], playerIndex, board, listValidJumps)):
                movePriority[i] -= 20
            #Makes the max move priority equal to the largest move priority
            if(movePriority[i] > maxMovePriority):
                maxMovePriority = movePriority[i]
        newJumpList = []
        for i in range(len(validJumps)):
            if(maxMovePriority == movePriority[i]):
               newJumpList += [validJumps[i]]
        move=newJumpList[random.randint(0, len(newJumpList)-1)]
    return move

#*********************************************************************************
#******************************* Testers *****************************************
#*********************************************************************************

#Prints the board
#@param board The board state
def printBoard(board):
    for i in range(len(board)):
        for j in range(len(board)):
            print(str(board[i][j]),end="")
        print()
