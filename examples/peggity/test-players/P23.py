import random

def adjacent(myCells,opCells,emptyCellsList,board):
    if len(myCells) + len(opCells) > 0:
        valid=False
        while(valid==False):
            move=emptyCellsList[random.randrange(0,len(emptyCellsList))]
            row=ord(move[0])-65
            col=int(move[1:])
            if row==14 and col!=14:
                if board[row-1][col+1]!=0 or board[row][col+1]!=0 or board[row-1][col]!=0 or board[row-1][col-1]!=0 or board[row][col-1]!=0:
                    valid=True
            elif row!=14 and col==14:
                if board[row-1][col]!=0 or board[row+1][col]!=0 or board[row-1][col-1]!=0 or board[row][col-1]!=0 or board[row+1][col-1]!=0:
                    valid=True
            elif row==14 and col==14:
                if board[row-1][col]!=0 or board[row-1][col-1]!=0 or board[row][col-1]!=0:
                    valid=True
            elif row==0 and col>0:
                if board[row][col+1]!=0 or board[row+1][col+1]!=0 or board[row+1][col]!=0 or board[row][col-1]!=0 or board[row+1][col-1]!=0:
                    valid=True
            elif row>0 and col==0:
                if board[row-1][col+1]!=0 or board[row][col+1]!=0 or board[row+1][col+1]!=0 or board[row-1][col]!=0 or board[row+1][col]!=0:
                    valid=True
            elif row==0 and col==0:
                if board[row][col+1]!=0 or board[row+1][col+1]!=0 or board[row+1][col]!=0:
                    valid=True
            else:
                if board[row-1][col+1]!=0 or board[row][col+1]!=0 or board[row+1][col+1]!=0 or board[row-1][col]!=0 or board[row+1][col]!=0 or board[row-1][col-1]!=0 or board[row][col-1]!=0 or board[row+1][col-1]!=0:
                    valid=True
    else:
        row=random.randrange(0,14)
        col=random.randrange(0,14)
    return row,col

def manualMove(pcolors,currentPlayer,board):
   
    myCells=[]
    opCells=[]
    emptyCellsList=[]
    for row in range(15):
        for col in range(15):
            if board[row][col]==currentPlayer:
                myCells.append(chr(65+row)+str(col))
            elif board[row][col]!=0:
                opCells.append(chr(65+row)+str(col))
            else:
                emptyCellsList.append(chr(65+row)+str(col))
    myWin=checkMove(myCells,board,currentPlayer,4)
    if myWin is not None:
        row,col=checkMove(myCells,board,currentPlayer,4)
        return row,col
    if currentPlayer==1:
        checkP=2
    else:
        checkP=1
    opWin=checkMove(opCells,board,checkP,4)
    if opWin is not None:
        row,col=checkMove(opCells,board,checkP,4)
        return row,col
    myScore=checkMove(myCells,board,currentPlayer,3)
    if myScore is not None:
        row,col=checkMove(myCells,board,currentPlayer,3)
        return row,col
    opScore=checkMove(opCells,board,checkP,3)
    if opScore is not None:
        row,col=checkMove(opCells,board,checkP,3)
        return row,col
    row,col=adjacent(myCells,opCells,emptyCellsList,board)
    return row,col



def checkMove(cellList,board,checkP,pegs):
    for cell in cellList:
            row=ord(cell[0])-65
            col=int(cell[1:])
            horz=[]
            vert=[]
            diag1=[]
            diag2=[]
            for i in range(-4,5):
                if row-i>=0 and row-i<=14 and col-i>=0 and col-i<=14:
                    diag2.append([row-i,col-i,board[row-i][col-i]])
                if row+i>=0 and row+i<=14 and col-i>=0 and col-i<=14:
                    diag1.append([row+i,col-i,board[row+i][col-i]])
                if row+i>=0 and row+i<=14:
                    horz.append([row+i,col,board[row+i][col]])
                if col+i>=0 and col+i<=14:
                    vert.append([row,col+i,board[row][col+i]])
            lines=[horz,vert,diag1,diag2]
            for line in lines:
                score=0
                emptyCell=False
                for c in line:
                    if c[2]==checkP:
                        score+=1
                    elif c[2]==0 and emptyCell==False:
                        nRow=c[0]
                        nCol=c[1]
                        emptyCell=True
                    elif c[2]==0 and emptyCell==True:
                        nRow=c[0]
                        nCol=c[1]
                        score=0
                        emptyCell=True
                    elif c[2]!=checkP:
                        emptyCell=False
                        score=0
                    if score==pegs and emptyCell==True:
                        return nRow,nCol

