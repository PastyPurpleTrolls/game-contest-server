import random


def getBlockingMoves(pcolors,currentPlayer,board):
    if currentPlayer==2:
        oppositePlayer=1
    if currentPlayer==1:
        oppositePlayer=2
    blockingMovesList=[]
    #4 1's in a row and a 0
    for row in range(len(board)):
        for col in range(len(board)-4):
            if board[row][col]==currentPlayer and board[row][col+1]==currentPlayer and board[row][col+2]==currentPlayer and board[row][col+3]==currentPlayer and board[row][col+4]==0:
                blockingMovesList.append(chr(row+65)+str(col+4))
            elif board[row][col]==0 and board[row][col+1]==currentPlayer and board[row][col+2]==currentPlayer and board[row][col+3]==currentPlayer and board[row][col+4]==currentPlayer:
                blockingMovesList.append(chr(row+65)+str(col))      
    #4 1's in a column and a 0
    for row in range(len(board)-4):
        for col in range(len(board)):
            if board[row][col]==currentPlayer and board[row+1][col]==currentPlayer and board[row+2][col]==currentPlayer and board[row+3][col]==currentPlayer and board[row+4][col]==0:
                blockingMovesList.append(chr(row+69)+str(col))
            if board[row][col]==0 and board[row+1][col]==currentPlayer and board[row+2][col]==currentPlayer and board[row+3][col]==currentPlayer and board[row+4][col]==currentPlayer:
                blockingMovesList.append(chr(row+65)+str(col))
    #diagonals
    #forward
    for row in range(4,len(board)):
        for col in range(len(board)-4):
            if board[row][col]==currentPlayer and board[row-1][col+1]==currentPlayer and board[row-2][col+2]==currentPlayer and board[row-3][col+3]==currentPlayer and board[row-4][col+4]==0:
                blockingMovesList.append(chr(row+61)+str(col+4))
            if board[row][col]==0 and board[row-1][col+1]==currentPlayer and board[row-2][col+2]==currentPlayer and board[row-3][col+3]==currentPlayer and board[row-4][col+4]==currentPlayer:
                blockingMovesList.append(chr(row+65)+str(col))
    #backward
    for row in range(4,len(board)):
        for col in range(4,len(board)):
            if board[row][col]==currentPlayer and board[row-1][col-1]==currentPlayer and board[row-2][col-2]==currentPlayer and board[row-3][col-3]==currentPlayer and board[row-4][col-4]==0:
                blockingMovesList.append(chr(row+61)+str(col-4))
            if board[row][col]==0 and board[row-1][col-1]==currentPlayer and board[row-2][col-2]==currentPlayer and board[row-3][col-3]==currentPlayer and board[row-4][col-4]==currentPlayer:
                blockingMovesList.append(chr(row+65)+str(col))

    return blockingMovesList


def getNearPeg(board):    
    emptyCellsList=[]
    nonEmptyCellsList=[]
    for row in range(15):
        for col in range(15):
            if board[row][col]==0:
                emptyCellsList.append(chr(65+row)+str(col))
            else:
                nonEmptyCellsList.append(chr(65+row)+str(col))
    potentialMovesList=[]
    for coordinate in nonEmptyCellsList:
        row=ord(coordinate[0])-65
        col=int(coordinate[1:])
        if row==0:#rowA and not A0 or A14
            if col==0:
                potentialMovesList.append(chr(65+row)+str(col+1))
                potentialMovesList.append(chr(65+row+1)+str(col))
                potentialMovesList.append(chr(65+row+1)+str(col+1))
            elif col==14:
                potentialMovesList.append(chr(65+row)+str(col-1))
                potentialMovesList.append(chr(65+row+1)+str(col))
                potentialMovesList.append(chr(65+row+1)+str(col-1))
            else:

                potentialMovesList.append(chr(65+row)+str(col-1))
                potentialMovesList.append(chr(65+row)+str(col+1))
                potentialMovesList.append(chr(65+row+1)+str(col))
                potentialMovesList.append(chr(65+row+1)+str(col+1))
                potentialMovesList.append(chr(65+row+1)+str(col-1))
        elif row==14:#row O and not O0 or O14
            if col==0:

                potentialMovesList.append(chr(65+row-1)+str(col))
                potentialMovesList.append(chr(65+row-1)+str(col+1))
                potentialMovesList.append(chr(65+row)+str(col+1))
            elif col==14:

                potentialMovesList.append(chr(65+row-1)+str(col))
                potentialMovesList.append(chr(65+row-1)+str(col-1))
                potentialMovesList.append(chr(65+row)+str(col-1))
            else:

                potentialMovesList.append(chr(65+row)+str(col-1))
                potentialMovesList.append(chr(65+row)+str(col+1))
                potentialMovesList.append(chr(65+row-1)+str(col))
                potentialMovesList.append(chr(65+row-1)+str(col+1))
                potentialMovesList.append(chr(65+row-1)+str(col-1))
        elif col==0: #col 0 and not A0 or O0
            if row==0:

                potentialMovesList.append(chr(65+row)+str(col+1))
                potentialMovesList.append(chr(65+row+1)+str(col))
                potentialMovesList.append(chr(65+row+1)+str(col+1))
            elif row==14:

                potentialMovesList.append(chr(65+row-1)+str(col))
                potentialMovesList.append(chr(65+row-1)+str(col+1))
                potentialMovesList.append(chr(65+row)+str(col+1))
            else:

                potentialMovesList.append(chr(65+row+1)+str(col))
                potentialMovesList.append(chr(65+row-1)+str(col))
                potentialMovesList.append(chr(65+row)+str(col+1))
                potentialMovesList.append(chr(65+row-1)+str(col+1))
                potentialMovesList.append(chr(65+row+1)+str(col+1))
        elif col==14:#col 14 and not A14 or O14
            if row==0:

                potentialMovesList.append(chr(65+row)+str(col-1))
                potentialMovesList.append(chr(65+row+1)+str(col))
                potentialMovesList.append(chr(65+row+1)+str(col-1))
            elif row==14:

                potentialMovesList.append(chr(65+row-1)+str(col))
                potentialMovesList.append(chr(65+row-1)+str(col-1))
                potentialMovesList.append(chr(65+row)+str(col-1)) 
            else:

                potentialMovesList.append(chr(65+row+1)+str(col))
                potentialMovesList.append(chr(65+row-1)+str(col))
                potentialMovesList.append(chr(65+row)+str(col-1))
                potentialMovesList.append(chr(65+row+1)+str(col-1))
                potentialMovesList.append(chr(65+row-1)+str(col-1))
        else:

            potentialMovesList.append(chr(65+row-1)+str(col-1))
            potentialMovesList.append(chr(65+row-1)+str(col))
            potentialMovesList.append(chr(65+row-1)+str(col+1))
            potentialMovesList.append(chr(65+row)+str(col+1))
            potentialMovesList.append(chr(65+row+1)+str(col-1))
            potentialMovesList.append(chr(65+row+1)+str(col))
            potentialMovesList.append(chr(65+row+1)+str(col+1))
            potentialMovesList.append(chr(65+row)+str(col-1))
    if len(potentialMovesList)>0:
        potentialMove=potentialMovesList[random.randrange(0,len(potentialMovesList))] #move that is next to a peg
        while board[ord(potentialMove[0])-65][int(potentialMove[1:])]!=0:
            potentialMove=potentialMovesList[random.randrange(0,len(potentialMovesList))]
    
        row=ord(potentialMove[0])-65
        col=int(potentialMove[1:])
        return row,col
    else:
        return random.randrange(0,len(board)),random.randrange(0,len(board))

def manualMove(pcolors,currentPlayer,board):
    blockingList=getBlockingMoves(pcolors,currentPlayer,board)
    if len(blockingList)==0:
        return getNearPeg(board)
    else:
        blockingMove=blockingList[random.randrange(0,len(blockingList))]
        row=ord(blockingMove[0])-65
        col=int(blockingMove[1:])
        return row,col



