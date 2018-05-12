import random

def fourInRow(board):
    for row in range(15):
        for col in range(15):
            if board[row][col]!=0:
                #horizontal
                if col<11:
                    count=1
                    for offset in range(1,4,1):
                        if board[row][col]==board[row][col+offset]:
                            count+=1
                    if count==4:
                        if validCheck(row,col-1,board):
                            return row,col-1
                        elif validCheck(row,col+4,board):
                            return row,col+4
                #vertical
                if row<11:
                    count=1
                    for offset in range(1,4,1):
                        if board[row][col]==board[row+offset][col]:
                            count+=1
                    if count==4:
                        if validCheck(row-1,col,board):
                            return row-1,col
                        elif validCheck(row+4,col,board):
                            return row+4,col
                #CHECK DIAGONALS
                #left to right
                if row<11 and col<11:
                    count=1
                    for offset in range(1,4,1):
                        if board[row][col]==board[row+offset][col+offset]:
                            count+=1
                    if count==4:
                         if validCheck(row-1,col-1,board):
                            return row-1,col-1
                         elif validCheck(row+4,col+4,board):
                            return row+4,col+4
                #right to left
                if row<11 and col>3:
                    count=1
                    for offset in range(1,4,1):
                        if board[row][col]==board[row+offset][col-offset]:
                            count+=1
                    if count==4:
                        if validCheck(row-1,col+1,board):
                            return row-1,col+1
                        elif validCheck(row+4,col-4,board):
                            return row+4,col-4
    return -1,-1


def validCheck(row,col,board):
    if len(board)<=row or len(board)<=col or row<0 or col<0:
        return False
    if board[row][col]==0:
        return True
    else:
        return False
        
    
    
def manualMove(pcolors,currentPlayer,board):
    emptyCellsList=[]
    player2ListCol=[]
    player2ListRow=[]
    player1ListCol=[]
    player1ListRow=[]
    for row in range(15):
        for col in range(15):
            if board[row][col]==0:
                emptyCellsList.append(chr(65+row)+str(col))
            elif board[row][col]==2:
                player2ListRow.append(row)
                player2ListCol.append(col)
            elif board[row][col]==1:
                player1ListRow.append(row)
                player1ListCol.append(col)
    row=-1
    col=-1
    if len(player2ListRow)==0:
        move=emptyCellsList[random.randrange(0,len(emptyCellsList))]
        row=ord(move[0])-65
        col=int(move[1:])
        return row,col
    row,col= fourInRow(board)
    if validCheck(row,col,board):
          Frow=int(row)
          Fcol=int(col)
          return Frow,Fcol
    while (validCheck(row,col,board)==False):
           randNum=random.randrange(0,(len(player2ListCol)))
           randNumR=random.randrange(-1,1)
           randNumC=random.randrange(-1,1)
           row=player2ListRow[randNum]+randNumR
           col=player2ListCol[randNum]+randNumC
    Frow=int(row)
    Fcol=int(col)
    return Frow,Fcol
 
