import random
def manualMove(pcolors,currentPlayer,board):
    rowFound2=""
    colFound2=""
    rowFound1=""
    colFound1=""
    count=0
    count2=0
    for rows in board:
        if 1 in rows:
            count+=1
        if 2 in rows:
            count2+=1
        for col in range(len(rows)):
            if rows[col]==2 and count==0:
                rowFound2=board.index(rows)   #if 2 in board and no 1 in board
                colFound2=col
            if rows[col]==1:
                rowFound1=board.index(rows)    #finds the last 1 played
                colFound1=col

    if rowFound2=="" and count==0:
        row,col=generateMove(board) #if no one has played random
        return row,col
    elif rowFound2!="" and count==0:
        count+=1
        row,col=next2(rowFound2,colFound2,board)
        return row,col
    else:
        if Four_in_a_row(board)==False:
            row,col=next2(rowFound1,colFound1,board)
            return row,col
        else:
            winRow,winCol,position=Four_in_a_row(board)
            if placeTheWin(winRow,winCol,position,board)!=False:
                row,col=placeTheWin(winRow,winCol,position,board)
                return row,col
            else:
               row,col=next2(rowFound1,colFound1,board)
               return row,col 
            

def next2(row,col,board):
    newrow=int(row)+random.randint(-1,1)
    newcol=int(col)+random.randint(-1,1)
    while emptySpace(newrow,newcol,board)==False:
        newrow=int(row)+random.randint(-1,1)
        newcol=int(col)+random.randint(-1,1)
    return newrow,newcol

   
def placeTheWin(row,col,position,board):
    if position=="horizontal":
        if emptySpace(row,col-1,board)==False:
            if emptySpace(row,col+4,board)!=False:
                col=col+4
                return row,col
            else:
                return False
        else:
            col=col-1
            return row,col                
    elif position=="vertical":
        if emptySpace(row-1,col,board)==False:
            if emptySpace(row+4,col,board)!=False:
                row=row+4
                return row,col
            else:
                return False
        else:
            row=row-1
            return row,col
    elif position=="left to right":
        if emptySpace(row-1,col-1,board)==False:
            if emptySpace(row+4,col+4,board)!=False:
                row=row+4
                col=col+4
                return row,col
            else:
                return False
        else:
            row=row-1
            col=col-1
            return row,col
    elif position=="right to left":
        if emptySpace(row-1,col+1,board)==False:
            if emptySpace(row+4,col-4,board)==False:
                row=row+4
                col=col-4
                return row,col
            else:
                return False
        else:
            row=row-1
            col=col+1
            return row,col
    else:
        return False

##def chooseMove(board):
##    for row in range(15):
##        for col in range(15):
##            if board[row][col]==1 or board[row][col]==2:
##                newRow=row+random.randint(-1,1)
##                newCol=col+random.randint(-1,1)
##                while emptySpace(newRow,newCol,board)==False:
##                    newRow=row+random.randint(-1,1)
##                    newCol=col+random.randint(-1,1)
##                    return newRow,newCol

def emptySpace(mrow,mcol,board):
    emptyCellsList=[]
    default=chr(65+mrow)+str(mcol)
    for row in range(15):
        for col in range(15):
            if board[row][col]==0:
                emptyCellsList.append(chr(65+row)+str(col))
    if default in emptyCellsList:
        move=default
        row=ord(move[0])-65
        col=int(move[1:])
        return row,col
    else:
        return False

def generateMove(board):
    emptyCellsList=[]
    for row in range(15):
        for col in range(15):
            if board[row][col]==0:
                emptyCellsList.append(chr(65+row)+str(col))
    move=emptyCellsList[random.randrange(0,len(emptyCellsList))]
    row=ord(move[0])-65
    col=int(move[1:])
    return row,col

def Four_in_a_row(board):
    for row in range(15):
        for col in range(15):
            if board[row][col]==1:
                #horizontal
                if col<11:
                    count=1
                    for offset in range(1,4,1):
                        if board[row][col]==board[row][col+offset]:
                            count+=1
                    if count==4:
                        return row,col,"horizontal"
                #vertical
                if row<11:
                    count=1
                    for offset in range(1,4,1):
                        if board[row][col]==board[row+offset][col]:
                            count+=1
                    if count==4:
                        return row,col,"vertical"
                #CHECK DIAGONALS
                #left to right
                if row<11 and col<11:
                    count=1
                    for offset in range(1,4,1):
                        if board[row][col]==board[row+offset][col+offset]:
                            count+=1
                    if count==4:
                        return row,col,"left to right"
                #right to left
                if row<11 and col>3:
                    count=1
                    for offset in range(1,4,1):
                        if board[row][col]==board[row+offset][col-offset]:
                            count+=1
                    if count==4:
                        return row,col,"right to left"
    return False

