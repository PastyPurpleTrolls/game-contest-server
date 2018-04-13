import random

def winCheck(board,emptyCellsList):
    for row in range(11):
        for col in range(11):
            if board[row][col]==board[row+1][col] and board[row+1][col]==board[row+2][col] and board[row+2][col]==board[row+3][col] and board[row][col]!=0:
                if board[row+4][col]==0:
                    x=row+4
                    y=col
                    return x,y
                elif board[row-1][col]==0:
                    x=row-1
                    y=col
                    return x,y
            elif board[row][col]==board[row][col+1] and board[row][col+1]==board[row][col+2] and board[row][col+2]==board[row][col+3] and board[row][col]!=0:
                if board[row][col+4]==0:
                    x=row
                    y=col+4
                    return x,y
                elif board[row][col-1]==0:
                    x=row
                    y=col-1
                    return x,y
            elif board[row][col]==board[row+1][col+1] and board[row+1][col+1]==board[row+2][col+2] and board[row+2][col+2]==board[row+3][col+3] and board[row][col]!=0:
                if board[row+4][col+4]==0:
                    x=row+4
                    y=col+4
                    return x,y
                elif board[row-1][col-1]==0:
                    x=row-1
                    y=col-1
                    return x,y
            elif board[row][col]==board[row-1][col+1] and board[row-1][col+1]==board[row-2][col+2] and board[row-2][col+2]==board[row-3][col+3] and board[row][col]!=0:
                if board[row-4][col+4]==0:
                    x=row-4
                    y=col+4
                    return x,y
                elif board[row+1][col-1]==0:
                    x=row+1
                    y=col-1
                    return x,y
    return 0,0

def manualMove(pcolors,currentPlayer,board):
    emptyCellsList=[]
    temp=False
    row,col=winCheck(board,emptyCellsList)
    if row!=0:
        return row,col
    if emptyCellsList!=[]:
        move=emptyCellsList[random.randrange(0,len(emptyCellsList))]
        row=ord(move[0])-65
        col=int(move[1:])
        return row,col
    for row in range(15):
        for col in range(15):
            if board[row][col]!=0:
                x=random.randint(1,5)
                if x==1:
                    emptyCellsList.append(chr(65+row-1)+str(col))
                elif x==2:
                    emptyCellsList.append(chr(65+row)+str(col+1))
                elif x==3:
                    emptyCellsList.append(chr(65+row+1)+str(col))
                elif x==4:
                    emptyCellsList.append(chr(65+row)+str(col-1))
                temp=True
    if temp==True:
        move=emptyCellsList[random.randrange(0,len(emptyCellsList))]
        row=ord(move[0])-65
        col=int(move[1:])
        return row,col
    for row in range(15):
        for col in range(15):
            if board[row][col]==0:
                emptyCellsList.append(chr(65+row)+str(col))
    move=emptyCellsList[random.randrange(0,len(emptyCellsList))]
    row=ord(move[0])-65
    col=int(move[1:])
    return row,col
