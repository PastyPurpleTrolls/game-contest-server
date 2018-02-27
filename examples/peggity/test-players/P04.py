import random
def manualMove(pcolors,currentPlayer,board):
    emptyCellsList=[]
    possibleMoves=[]
    lstWith2=[]
    for row in range(15):  #makes list of empty spaces
        for col in range(15):
            if board[row][col]==0:
                emptyCellsList.append(chr(65+row)+str(col)) 
    for r in range(15):   #makes list with the places taken by the other player
        for c in range(15):
            if board[r][c]==2:
                lstWith2.append(chr(65+r)+str(c))
    print(lstWith2)

    if len(lstWith2)<=0:
        move=emptyCellsList[random.randrange(0,len(emptyCellsList))]
        row=ord(move[0])-65
        col=int(move[1:])
        return row,col
#chooses spot to block a 4 in a row
    else:
        for row in range(15):
            for col in range(15):
                if board[row][col]!=0:
                    #horizontal
                    if col<12 and col>0:
                        count=1
                        for offset in range(1,3,1):
                            if board[row][col]==board[row][col+offset]:
                                count+=1
                        if count>=3:
                            for move in emptyCellsList:
                                r=ord(move[0])-65
                                c=int(move[1:])
                                if (r==row and c==col-1) or (r==row and c==col+count):
                                    return r,c
                    #vertical
                    if row<12 and row>0:
                        count=1
                        for offset in range(1,3,1):
                            if board[row][col]==board[row+offset][col]:
                                count+=1
                        if count>=3:
                            for move in emptyCellsList:
                                r=ord(move[0])-65
                                c=int(move[1:])
                                if (r==row-1 and c==col) or (r==row+count and c==col):
                                    return r,c
                              #CHECK DIAGONALS
                    #left to right
                    if row<12 and col<12 and row>0 and col>0:
                        count=1
                        for offset in range(1,3,1):
                            if board[row][col]==board[row+offset][col+offset]:
                                count+=1
                        if count>=3:
                            for move in emptyCellsList:
                                r=ord(move[0])-65
                                c=int(move[1:])
                                if (r==row-1 and c==col-1) or (r==row+count and c==col+count):
                                    return r,c
                            
                    #right to left
                    if row<12 and col>3:
                        count=1
                        for offset in range(1,3,1):
                            if board[row][col]==board[row+offset][col-offset]:
                                count+=1
                        if count>=3:
                            for move in emptyCellsList:
                                r=ord(move[0])-65
                                c=int(move[1:])
                                if (r==row-1 and c==col+1) or (r==row+count and c==col-count):
                                    return r,c
    
#chooses random spot next to opposite colored peg
    #else:
    takenSpot=lstWith2[random.randrange(0,len(lstWith2))]
    row=ord(takenSpot[0])-65
    col=int(takenSpot[1:])
    move=chr(65+row-1)+str(col-1)# top left
    if move in emptyCellsList:
        possibleMoves.append(move)
    move=chr(65+row-1)+str(col) #top
    if move in emptyCellsList:
        possibleMoves.append(move)
    move=chr(65+row-1)+str(col+1) #top right
    if move in emptyCellsList:
        possibleMoves.append(move)
    move=chr(65+row)+str(col+1)#right
    if move in emptyCellsList:
        possibleMoves.append(move)
    move=chr(65+row+1)+str(col+1) #bottom right
    if move in emptyCellsList:
        possibleMoves.append(move)
    move=chr(65+row+1)+str(col)  #bottom
    if move in emptyCellsList:
        possibleMoves.append(move)
    move=chr(65+row+1)+str(col-1)#bottom left
    if move in emptyCellsList:
        possibleMoves.append(move)
    move=chr(65+row)+str(col-1)#left
    if move in emptyCellsList:
        possibleMoves.append(move)
    if len(possibleMoves)<=0:
        row,col = manualMove(pcolors,currentPlayer,board)
        return row,col
    move=possibleMoves[random.randrange(0,len(possibleMoves))]
    row=ord(move[0])-65
    col=int(move[1:])
    return row,col

