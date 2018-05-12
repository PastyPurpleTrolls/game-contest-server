import random
def manualMove(pcolors,currentPlayer,board):
    filledCellsList=[]
    emptyCellsList=[]
    
    
    for row in range(15):
        for col in range(15):
            if board[row][col]==0:
                emptyCellsList.append(chr(65+row)+str(col))
            elif board[row][col]==1 or board[row][col]==2:
                filledCellsList.append(chr(65+row)+str(col))

    for row in range(15):
        for col in range(15):
            if board[row][col]!=0:
                #horizontal
                if col<12:
                    count=1
                    for offset in range(1,4,1):
                        if board[row][col]==board[row][col+offset]:
                            count+=1
                    if count==4:
                        if col<11 and board[row][col+4]==0 and col != 14:
                            return row,col+4
                        elif board[row][col-1]==0 and col != 0:
                            print("here")
                            return row,col-1
                #vertical
                if row<12:
                    count=1
                    for offset in range(1,4,1):
                        if board[row][col]==board[row+offset][col]:
                            count+=1
                    if count==4:
                        if row<11 and board[row+4][col]==0 and col != 14:
                            return row+4,col
                        elif board[row-1][col]==0 and col != 0:
                            print("here")
                            return row-1,col
                #CHECK DIAGONALS
                #left to right
                if row<12 and col<12:
                    count=1
                    for offset in range(1,4,1):
                        if board[row][col]==board[row+offset][col+offset]:
                            count+=1
                    if count==4:
                        if row<11 and col<11 and board[row+4][col+4]==0 and col != 14 and row != 14:
                            return row+4,col+4
                        elif board[row-1][col-1]==0 and col != 0 and row != 0:
                            print("here")
                            return row-1,col-1
                #right to left
                if row<12 and col>2:
                    count=1
                    for offset in range(1,4,1):
                        if board[row][col]==board[row+offset][col-offset]:
                            count+=1
                    if count==4:
                        #print(board[row-1][col+1])
                        if row<11 and col>3 and board[row+4][col-4]==0 and col != 0 and row != 14:
                            print("here First")
                            return row+4,col-4
                        if row>0 and col<14 and board[row-1][col+1]==0:
                            print("here")
                            return row-1,col+1


    if len(filledCellsList)==0:
        move=emptyCellsList[random.randrange(0,len(emptyCellsList))]
        row=ord(move[0])-65
        col=int(move[1:])
        return row,col

    else:
        valid=False
        while not valid:
            move=filledCellsList[random.randrange(0,len(filledCellsList))]
            row=ord(move[0])-65
            col=int(move[1:])
            row=row+(random.randint(-1,1))
            col=col+(random.randint(-1,1))
            if row>=0 and row<=14 and col>=0 and col<=14 and board[row][col]==0:
                valid=True
                return row,col


           


