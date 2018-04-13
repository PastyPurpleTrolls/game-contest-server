import random
def manualMove(pcolors,currentPlayer,board):
    preventWin=[]
    winMoves=[]
    emptyCellsList=[]
    movesList=[]
    for row in range(15):
        for col in range(15):
            if board[row][col]==0:
                emptyCellsList.append(chr(65+row)+str(col))
    takenCellsList=[]
    P1CellsList=[]
    for row in range(15):
        for col in range(15):
            if board[row][col]==1:
                takenCellsList.append(chr(65+row)+str(col))
                P1CellsList.append(chr(65+row)+str(col))
                thing1=chr(65+row)+str(col)
                if thing1 not in movesList:
                    movesList.append(chr(64+row)+str(col-1))
                    movesList.append(chr(64+row)+str(col))
                    movesList.append(chr(64+row)+str(col+1))
                    movesList.append(chr(65+row)+str(col-1))
                    movesList.append(chr(65+row)+str(col+1))
                    movesList.append(chr(66+row)+str(col-1))
                    movesList.append(chr(66+row)+str(col))
                    movesList.append(chr(66+row)+str(col+1))
                

    P2CellsList=[]
    for row in range(15):
        for col in range(15):
            if board[row][col]==2:
                takenCellsList.append(chr(65+row)+str(col))
                P2CellsList.append(chr(65+row)+str(col))
                thing2=chr(65+row)+str(col)
                if  thing2 not in movesList:
                    movesList.append(chr(64+row)+str(col-1))
                    movesList.append(chr(64+row)+str(col))
                    movesList.append(chr(64+row)+str(col+1))
                    movesList.append(chr(65+row)+str(col-1))
                    movesList.append(chr(65+row)+str(col+1))
                    movesList.append(chr(66+row)+str(col-1))
                    movesList.append(chr(66+row)+str(col))
                    movesList.append(chr(66+row)+str(col+1))

    
    if P2CellsList==[]:
        move=emptyCellsList[random.randrange(0,len(emptyCellsList))]

   
    else:
        #To win
        winMoves=[]
        for row in range(15):
            for col in range(15):
                if board[row][col]==1:
                    #horizontal
                    if col<12:
                        count=1
                        for offset in range(1,4,1):
                            if board[row][col]==board[row][col+offset]:
                                count+=1
                        winMove1=chr(65+row)+str(col-1)
                        winMove3=chr(65+row)+str(col+4)
                        if count==4:
                            if winMove1 not in winMoves and winMove1 in emptyCellsList:
                                winMoves.append(chr(65+row)+str(col-1))
                            if winMove3 not in winMoves and winMove3 in emptyCellsList:
                                winMoves.append(chr(65+row)+str(col+4))
     
                    #vertical
                    if row<12:
                        count=1
                        for offset in range(1,4,1):
                            if board[row][col]==board[row+offset][col]:
                                count+=1
                        winMove1=chr(65+row-1)+str(col)
                        winMove4=chr(65+row+4)+str(col)
                        if count==4:
                            if winMove1 not in winMoves and winMove1 in emptyCellsList:
                                winMoves.append(chr(65+row-1)+str(col))
                            if winMove4 not in winMoves and winMove4 in emptyCellsList:
                                winMoves.append(chr(65+row+4)+str(col))

     
                            
                    #CHECK DIAGONALS
                    #left to right
                    if row<12 and col<12:
                        count=1
                        for offset in range(1,4,1):
                            if board[row][col]==board[row+offset][col+offset]:
                                count+=1
                        winMove1=chr(65+row-1)+str(col-1)
                        winMove4=chr(65+row+4)+str(col+4)
                        if count==4:
                            if winMove1 not in winMoves and winMove1 in emptyCellsList:
                                winMoves.append(chr(65+row-1)+str(col-1))
                            if winMove4 not in winMoves and winMove4 in emptyCellsList:
                                winMoves.append(chr(65+row+4)+str(col+4))

                    #right to left
                    if row<12 and col>2:
                        count=1
                        for offset in range(1,4,1):
                            if board[row][col]==board[row+offset][col-offset]:
                                count+=1
                        winMove1=chr(65+row+1)+str(col-1)
                        winMove3=chr(65+row-4)+str(col+4)
                        if count==4:
                            if winMove1 not in winMoves and winMove1 in emptyCellsList:
                                winMoves.append(chr(65+row+1)+str(col-1))
                            if winMove3 not in winMoves and winMove3 in emptyCellsList:
                                winMoves.append(chr(65+row-4)+str(col+4))

        #To prevent win
        preventWin=[]                               
        for row in range(15):
            for col in range(15):
                if board[row][col]==2:
                    #horizontal
                    if col<13:
                        count=1
                        for offset in range(1,3,1):
                            if board[row][col]==board[row][col+offset]:
                                count+=1
                        preventWinMove1=chr(65+row)+str(col-1)
                        preventWinMove3=chr(65+row)+str(col+3)
                        if count==3:
                            if preventWinMove1 not in preventWin and preventWinMove1 in emptyCellsList:
                                preventWin.append(chr(65+row)+str(col-1))
                            if preventWinMove3 not in preventWin and preventWinMove3 in emptyCellsList:
                                preventWin.append(chr(65+row)+str(col+3))
     
                    #vertical
                    if row<13:
                        count=1
                        for offset in range(1,3,1):
                            if board[row][col]==board[row+offset][col]:
                                count+=1
                        preventWinMove1=chr(65+row-1)+str(col)
                        preventWinMove4=chr(65+row+3)+str(col)
                        if count==3:
                            if preventWinMove1 not in preventWin and preventWinMove1 in emptyCellsList:
                                preventWin.append(chr(65+row-1)+str(col))
                            if preventWinMove4 not in preventWin and preventWinMove4 in emptyCellsList:
                                preventWin.append(chr(65+row+3)+str(col))

     
                            
                    #CHECK DIAGONALS
                    #left to right
                    if row<13 and col<13:
                        count=1
                        for offset in range(1,3,1):
                            if board[row][col]==board[row+offset][col+offset]:
                                count+=1
                        preventWinMove1=chr(65+row-1)+str(col-1)
                        preventWinMove4=chr(65+row+3)+str(col+3)
                        if count==3:
                            if preventWinMove1 not in preventWin and preventWinMove1 in emptyCellsList:
                                preventWin.append(chr(65+row-1)+str(col-1))
                            if preventWinMove4 not in preventWin and preventWinMove4 in emptyCellsList:
                                preventWin.append(chr(65+row+3)+str(col+3))

                    #right to left
                    if row<13 and col>2:
                        count=1
                        for offset in range(1,3,1):
                            if board[row][col]==board[row+offset][col-offset]:
                                count+=1
                        preventWinMove1=chr(65+row+3)+str(col-3)
                        preventWinMove3=chr(65+row-1)+str(col+1)
                        if count==3:
                            if preventWinMove1 not in preventWin and preventWinMove1 in emptyCellsList:
                                preventWin.append(chr(65+row+3)+str(col-3))
                            if preventWinMove3 not in preventWin and preventWinMove3 in emptyCellsList:
                                preventWin.append(chr(65+row-1)+str(col+1))
                                
        move=movesList[random.randrange(0,len(movesList))]
    while move in takenCellsList:
        move=movesList[random.randrange(0,len(movesList))]
    
    if winMoves!=[]:
        move=winMoves[random.randrange(0,len(winMoves))]
        winMoves.remove(move)
        row=ord(move[0])-65
        col=int(move[1:])
        return row,col
        
    elif preventWin!=[]:
        move=preventWin[random.randrange(0,len(preventWin))]
        preventWin.remove(move)
        row=ord(move[0])-65
        col=int(move[1:])
        return row,col
    while move not in takenCellsList and preventWin==[] and winMoves==[]:
        row=ord(move[0])-65
        col=int(move[1:])
        return row,col
