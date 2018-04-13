#THIS IS THE AUTOMATED PLAYER! meow...

import random



def fourInARow(pcolors,currentPlayer,board):
    for col in range(12):
        for row in range(15):
            #print(board[row][col],currentPlayer)
            if int(board[row][col])==int(currentPlayer) and board[row][col]==board[row][col+1] and board[row][col+1]==board[row][col+2] and board[row][col+2]==board[row][col+3] and board[row][col+3]==board[row][col+4]:
                if col!=0: #everybody look left
                    if board[row][col-1]==0:
                        return row,col-1
                if col!=14:         #everybody look right
                    if board[row][col+1]==0:
                        return row,col+1
    #print('No possible wins in rows')
    for row in range(12):
        for col in range(15):
            if int(board[row][col])==int(currentPlayer) and board[row][col]==board[row+1][col] and board[row+1][col]==board[row+2][col] and board[row+2][col]==board[row+3][col] and board[row+3][col]==board[row+4][col]:
                if row!=0: #everybody look up
                    if board[row-1][col]==0:
                        return row-1,col
                if row!=14:         #everybody look down
                    if board[row+1][col]==0:
                        return row+1,col
    #print('No possible wins in cols')
         
    return False,False

def manualMove(pcolors,currentPlayer,board):
    emptyCellsList=[]
    isBoardOccupied=False

    for eachRow in range(15):
        for eachCol in range(15):
            if board[eachRow][eachCol]==0:
                pass
            else:
                isBoardOccupied=True
    
    if isBoardOccupied==False:
        col=int(random.randint(0,14))
        row=int(random.randint(0,14))
        return row,col


    victoryRow,victoryCol=fourInARow(pcolors,currentPlayer,board)
    #print(victoryRow,victoryCol)
    if victoryRow!=False and victoryCol!=False:
        return victoryRow,victoryCol

        
    for row in range(15):
        for col in range(15):
            
            if board[row][col]>0 and row!=0 and row!=14 and col!=0 and col!=14:
                if board[row][col+1]==0:
                    emptyCellsList.append(chr(65+row)+str(col+1))#east
                    
                if board[row][col-1]==0:
                    emptyCellsList.append(chr(65+row)+str(col-1))#west
                    
                if board[row+1][col]==0:
                    emptyCellsList.append(chr(65+row+1)+str(col))#south
                    
                if board[row-1][col]==0:
                    emptyCellsList.append(chr(65+row-1)+str(col))#north
                    
                if board[row+1][col-1]==0:
                    emptyCellsList.append(chr(65+row+1)+str(col-1))#southwest
                    
                if board[row-1][col-1]==0:
                    emptyCellsList.append(chr(65+row-1)+str(col-1))#northwest
                    
                if board[row-1][col+1]==0:
                    emptyCellsList.append(chr(65+row-1)+str(col+1))#northeast
                    
                if board[row+1][col+1]==0:
                    emptyCellsList.append(chr(65+row+1)+str(col+1))#southeast
                    
            if board[row][col]>0 and row!=0 and row!=14 and col==0:#left side +
                
                if board[row-1][col]==0:
                    emptyCellsList.append(chr(65+row-1)+str(col))#north
                    
                if board[row-1][col+1]==0:
                    emptyCellsList.append(chr(65+row-1)+str(col+1))#northeast
                    
                if board[row][col+1]==0:
                    emptyCellsList.append(chr(65+row)+str(col+1))#east
                    
                if board[row+1][col+1]==0:
                    emptyCellsList.append(chr(65+row+1)+str(col+1))#southeast
                    
                if board[row+1][col]==0:
                    emptyCellsList.append(chr(65+row+1)+str(col))#south
                    
            if board[row][col]>0 and row!=14 and row!=0 and col==14:#right side +
                if board[row-1][col]==0:
                    emptyCellsList.append(chr(65+row-1)+str(col))#north
                    
                if board[row-1][col-1]==0:
                    emptyCellsList.append(chr(65+row-1)+str(col-1))#northwest
                    
                if board[row][col-1]==0:
                    emptyCellsList.append(chr(65+row)+str(col-1))#west
                    
                if board[row+1][col-1]==0:
                    emptyCellsList.append(chr(65+row+1)+str(col-1))#southwest
                    
                if board[row+1][col]==0:
                    emptyCellsList.append(chr(65+row+1)+str(col))#south
                    
            if board[row][col]>0 and row==0 and col!=0 and col!=14:#top +
                
                if board[row][col-1]==0:
                    emptyCellsList.append(chr(65+row)+str(col-1))#west
                    
                if board[row+1][col-1]==0:
                    emptyCellsList.append(chr(65+row+1)+str(col-1))#southwest
                    
                if board[row+1][col]==0:
                    emptyCellsList.append(chr(65+row+1)+str(col))#south
                    
                if board[row+1][col+1]==0:
                    emptyCellsList.append(chr(65+row+1)+str(col+1))#southeast
                    
                if board[row][col+1]==0:
                    emptyCellsList.append(chr(65+row)+str(col+1))#east
                    
            if board[row][col]>0 and row==14 and col!=0 and col!=14:#bottom +
                
                if board[row][col-1]==0:
                    emptyCellsList.append(chr(65+row)+str(col-1))#west
                    
                if board[row-1][col-1]==0:
                    emptyCellsList.append(chr(65+row-1)+str(col-1))#northwest
                    
                if board[row-1][col]==0:
                    emptyCellsList.append(chr(65+row-1)+str(col))#north
                    
                if board[row-1][col+1]==0:
                    emptyCellsList.append(chr(65+row-1)+str(col+1))#northeast
                    
                if board[row][col+1]==0:
                    emptyCellsList.append(chr(65+row)+str(col+1))#east
                    
            if board[row][col]>0 and row==0 and col==0:#upper left +
                
                if board[row+1][col]==0:
                    emptyCellsList.append(chr(65+row+1)+str(col))#south
                    
                if board[row+1][col+1]==0:
                    emptyCellsList.append(chr(65+row+1)+str(col+1))#southeast
                    
                if board[row][col+1]==0:
                    emptyCellsList.append(chr(65+row)+str(col+1))#east
                    
            if board[row][col]>0 and row==0 and col==14:#upper right +
                
                if board[row][col-1]==0:
                    emptyCellsList.append(chr(65+row)+str(col-1))#west
                    
                if board[row+1][col-1]==0:
                    emptyCellsList.append(chr(65+row+1)+str(col-1))#southwest
                    
                if board[row+1][col]==0:
                    emptyCellsList.append(chr(65+row+1)+str(col))#south
                    
            if board[row][col]>0 and row==14 and col==0:#lower left +
                
                if board[row-1][col]==0:
                    emptyCellsList.append(chr(65+row-1)+str(col))#north
                    
                if board[row-1][col+1]==0:
                    emptyCellsList.append(chr(65+row-1)+str(col+1))#northeast
                    
                if board[row][col+1]==0:
                    emptyCellsList.append(chr(65+row)+str(col+1))#east
                    
            if board[row][col]>0 and row==14 and col==14:#lower right
                
                if board[row][col-1]==0:
                    emptyCellsList.append(chr(65+row)+str(col-1))#west
                    
                if board[row-1][col-1]==0:
                    emptyCellsList.append(chr(65+row-1)+str(col-1))#northwest
                    
                if board[row-1][col]==0:
                    emptyCellsList.append(chr(65+row-1)+str(col))#north
##    print(emptyCellsList)
    move=emptyCellsList[random.randrange(0,len(emptyCellsList))]
    row=ord(move[0])-65
    col=int(move[1:])
    return row,col
