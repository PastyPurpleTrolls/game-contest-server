import random

def NinARow(board,N,playerNumber):
    moves=[]
    for row in range(15):
        for col in range(15):
            if board[row][col]==playerNumber:
                #horizontal
                if col<15-N+1:
                    count=1
                    for offset in range(1,N,1):
                        if board[row][col]==board[row][col+offset]:
                            count+=1
                    if count==N:
                        #now find empty ends as possible moves
                        if col != 0 and board[row][col-1]==0: #left end
                            moves.append(chr(row+65)+str(col-1))
                        if col+offset !=14 and board[row][col+offset+1]==0: #right end
                            moves.append(chr(row+65)+str(col+offset+1))
                #vertical
                if row<15-N+1:
                    count=1
                    for offset in range(1,N,1):
                        if board[row][col]==board[row+offset][col]:
                            count+=1
                    if count==N:
                        #now find empty ends as possible moves
                        if row != 0 and board[row-1][col]==0: #top end
                            moves.append(chr(row+65-1)+str(col))
                        if row+offset !=14 and board[row+offset+1][col]==0: #bottom end
                            moves.append(chr(row+offset+65+1)+str(col))
                #CHECK DIAGONALS
                #left to right
                if row<15-N+1 and col<15-N+1:
                    count=1
                    for offset in range(1,N,1):
                        if board[row][col]==board[row+offset][col+offset]:
                            count+=1
                    if count==N:
                        #now find empty ends as possible moves
                        if row != 0 and col != 0 and board[row-1][col-1]==0: #top upper left end
                            moves.append(chr(row+65-1)+str(col-1))
                        if row+offset !=14 and col+offset != 14 and board[row+offset+1][col+offset+1]==0: #bottom lower right end
                            moves.append(chr(row+offset+65+1)+str(col+offset+1))
                #right to left
                if row<15-N+1 and col>N-2:
                    count=1
                    for offset in range(1,N,1):
                        if board[row][col]==board[row+offset][col-offset]:
                            count+=1
                    if count==N:
                        #now find empty ends as possible moves
                        if row != 0 and col != 14 and board[row-1][col+1]==0: #top upper right end
                            moves.append(chr(row+65-1)+str(col+1))
                        if row+offset !=14 and col-offset != 0 and board[row+offset+1][col-offset-1]==0: #bottom lower left end
                            moves.append(chr(row+offset+65+1)+str(col-offset-1))
    if len(moves)>0:
        return moves
    else:
        return []

def threeTwoFix(ThreeInARowList,TwoInARowList):
    if TwoInARowList!=[] and ThreeInARowList != []:
        for aLoc in ThreeInARowList:
            if aLoc in TwoInARowList:
                TwoInARowList.remove(aLoc)
    return TwoInARowList

def findSingleMoves(board,playerNumber):
    moves=[]
    for row in range(15):
        for col in range(15):
            if board[row][col]==playerNumber:
                noNeighbor=True
                tempMoves=[]
                for rowInc in range(-1,2,1):
                    for colInc in range(-1,2,1):
                        newCol=col+colInc
                        newRow=row+rowInc
                        if noNeighbor and newRow>=0 and newRow<=14 and newCol>=0 and newCol<=14 and not(newCol==col and newRow==row):
                            if board[newRow][newCol]!=0:
                                noNeighbor=False
                            else:
                                 tempMoves.append(chr(newRow+65)+str(newCol))
                if noNeighbor:
                    moves=moves+tempMoves
    return moves

def findPegs(board,pNum): #finds all locations of pegs for specified player number
    pegList=[]
    for row in range(15):
        for col in range(15):
            if board[row][col]==pNum:
                pegList.append(chr(row+65)+str(col))
    return pegList

def lookAround(board,pegsList): #finds open locations next to existing pegs
    openList=[]
    for peg in pegsList:
        row=ord(peg[0])-65
        col=int(peg[1:])
        for rowInc in range(-1,2,1):
            for colInc in range(-1,2,1):
                newCol=col+colInc
                newRow=row+rowInc
                if newRow>=0 and newRow<=14 and newCol>=0 and newCol<=14 and not(newCol==col and newRow==row):
                    if board[newRow][newCol]==0:
                         openList.append(chr(newRow+65)+str(newCol))
    return openList   

#MAIN LOGIC FOR AUTOMATED PLAYER
def getMove(board,playerNumber,enemyNumber):
    #MUST MOVES - WIN OR BLOCK WIN IN THAT ORDER
    #Check for a 4 in a row possible WIN situation
    myPossibleWins4InARowList=NinARow(board,4,playerNumber)
    if myPossibleWins4InARowList != []: 
        return myPossibleWins4InARowList[0]
            
    #Check for a 4 in a row possible BLOCK situation
    myPossibleLosses4InARow=NinARow(board,4,enemyNumber) #notice enemyNumber is passed
    if myPossibleLosses4InARow != []:
        return myPossibleLosses4InARow[0]

    #NOW - What else is open?
    #Check for 3 in a row possible next move for player
    threeInARowList=NinARow(board,3,playerNumber)
    if len(threeInARowList)>0:
        return threeInARowList[random.randint(0,len(threeInARowList)-1)]
    
    #Check for 2 in a row possible next move for player
    twoInARowList=NinARow(board,2,playerNumber)
    #print("2 in a row for auto",TwoInARowList)
    twoInARowList=threeTwoFix(threeInARowList,twoInARowList)
    if len(twoInARowList)>0:
        return twoInARowList[random.randint(0,len(twoInARowList)-1)]

    #Check if any pegs for pairs
    nextToMovesList=lookAround(board,findPegs(board, playerNumber))
    if len(nextToMovesList)>0:
        return nextToMovesList[random.randint(0,len(nextToMovesList)-1)]
    

    #Check for single pegs for possible next move for player
    singleMoves=findSingleMoves(board,playerNumber)
    if len(singleMoves)>0:
        return singleMoves[random.randint(0,len(singleMoves)-1)]

    #No moves have been made by player, so:
    return("G6")

