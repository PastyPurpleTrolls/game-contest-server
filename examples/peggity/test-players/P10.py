import random

def autoMove(pcolors,currentPlayer,board):
    if currentPlayer==1:
        otherPlayer=2
    else:
        otherPlayer=1
        
    otherCellsList=[]
    myCellsList=[]
    emptyCellsList=[]
    for row in range(15):
        for col in range(15):
            if board[row][col]==0:
                emptyCellsList.append(chr(65+row)+str(col))
            if board[row][col]==currentPlayer:
                myCellsList.append(chr(65+row)+str(col))
            if board[row][col]!=currentPlayer and board[row][col]!=0:
                otherCellsList.append(chr(65+row)+str(col))

    turnCounter=1

    # check for My win horizontally               
    for Row in range(15):
        for Col in range(12):           
            if board[Row][Col]==board[Row][Col+1]==board[Row][Col+2]==board[Row][Col+3]==currentPlayer:
                if (Col-1)>=0 and board[Row][Col-1]==0:
                    row=Row
                    col=Col-1
                    turnCounter+=1
                    return row,col
                if (Col+4)<=14 and board[Row][Col+4]==0:
                    row=Row
                    col=Col+4
                    turnCounter+=1
                    return row,col
            pass

    # check for My win vert
    for Col in range(15):
        for Row in range(12):           
            if board[Row][Col]==board[Row+1][Col]==board[Row+2][Col]==board[Row+3][Col]==currentPlayer:
                if (Row-1)>=0 and board[Row-1][Col]==0:
                    row=Row-1
                    col=Col
                    turnCounter+=1
                    return row,col
                if (Row+4)<=14 and board[Row+4][Col]==0:
                    row=Row+4
                    col=Col
                    turnCounter+=1
                    return row,col

    # check for MY win Lhigh to Rlow
    for Row in range(12):
        for Col in range(12):                          
            if board[Row][Col]==board[Row+1][Col+1]==board[Row+2][Col+2]==board[Row+3][Col+3]==currentPlayer:
                if (Row-1)>=0 and (Col-1)>=0 and board[Row-1][Col-1]==0:
                    row=Row-1
                    col=Col-1
                    turnCounter+=1
                    return row,col
                if (Row+4)<=14 and (Col+4)<=14 and board[Row+4][Col+4]==0:
                    row=Row+4
                    col=Col+4
                    turnCounter+=1
                    return row,col
      
    # ck for MY win diag Llow to Rhigh
    for Row in range(12):
        for Col in range(14,2,-1):                          
            if board[Row][Col]==board[Row+1][Col-1]==board[Row+2][Col-2]==board[Row+3][Col-3]==currentPlayer:
                if (Row-1)>=0 and (Col+1)>=0 and board[Row-1][Col+1]==0:
                    row=Row-1
                    col=Col+1
                    turnCounter+=1
                    return row,col
                if (Row+4)<=14 and (Col-4)<=14 and board[Row+4][Col-4]==0:
                    row=Row+4
                    col=Col-4
                    turnCounter+=1
                    return row,col

    # check for Blocking horizontally               
    for Row in range(15):
        for Col in range(12):           
            if board[Row][Col]==board[Row][Col+1]==board[Row][Col+2]==board[Row][Col+3]==otherPlayer:
                if (Col-1)>=0 and board[Row][Col-1]==0:
                    row=Row
                    col=Col-1
                    turnCounter+=1
                    return row,col
                if (Col+4)<=14 and board[Row][Col+4]==0:
                    row=Row
                    col=Col+4
                    turnCounter+=1
                    return row,col           

    # check for Blocking vert
    for Col in range(15):
        for Row in range(12):           
            if board[Row][Col]==board[Row+1][Col]==board[Row+2][Col]==board[Row+3][Col]==otherPlayer:
                if (Row-1)>=0 and board[Row-1][Col]==0:
                    row=Row-1
                    col=Col
                    turnCounter+=1
                    return row,col
                if (Row+4)<=14 and board[Row+4][Col]==0:
                    row=Row+4
                    col=Col
                    turnCounter+=1
                    return row,col

    # check for Blocking Lhigh to Rlow
    for Row in range(12):
        for Col in range(12):                          
            if board[Row][Col]==board[Row+1][Col+1]==board[Row+2][Col+2]==board[Row+3][Col+3]==otherPlayer:
                if (Row-1)>=0 and (Col-1)>=0 and board[Row-1][Col-1]==0:
                    row=Row-1
                    col=Col-1
                    turnCounter+=1
                    return row,col
                if (Row+4)<=14 and (Col+4)<=14 and board[Row+4][Col+4]==0:
                    row=Row+4
                    col=Col+4
                    turnCounter+=1
                    return row,col
      
    # ck for Blocking diag Llow to Rhigh
    for Row in range(12):
        for Col in range(14,2,-1):                          
            if board[Row][Col]==board[Row+1][Col-1]==board[Row+2][Col-2]==board[Row+3][Col-3]==otherPlayer:
                if (Row-1)>=0 and (Col+1)>=0 and board[Row-1][Col+1]==0:
                    row=Row-1
                    col=Col+1
                    turnCounter+=1
                    return row,col
                if (Row+4)<=14 and (Col-4)<=14 and board[Row+4][Col-4]==0:
                    row=Row+4
                    col=Col-4
                    turnCounter+=1
                    return row,col
      


    # otherwise choose random cell
    turnCounter=0
    if len(myCellsList)==0 and len(otherCellsList)==0:
        firstPlayer=currentPlayer
        move=emptyCellsList[random.randrange(0,len(emptyCellsList)-4)]
        turnCounter+=1
    else:
        if turnCounter%2==1:
            playerList=myCellsList
        else:
            playerList=otherCellsList
            
        moves=[]
        for oldMove in playerList:
            Row=ord(oldMove[0])-65
            Col=int(oldMove[1:])
            if Row<14 and Col>0 and board[Row+1][Col-1]==0:
                moves.append(chr(Row+1+65)+str(Col-1))
            if Row<14 and Col<14 and board[Row+1][Col+1]==0:
                moves.append(chr(Row+1+65)+str(Col+1))
            if Row>0 and Col>0 and board[Row-1][Col-1]==0:
                moves.append(chr(Row-1+65)+str(Col-1))
            if Row>0 and Col<14 and board[Row-1][Col+1]==0:
                moves.append(chr(Row-1+65)+str(Col+1))
            if Row<14 and board[Row+1][Col]==0:
                moves.append(chr(Row+1+65)+str(Col))
            if Row>0 and board[Row-1][Col]==0:
                moves.append(chr(Row-1+65)+str(Col))
            if Col>0 and board[Row][Col-1]==0:
                moves.append(chr(Row+65)+str(Col-1))
            if Col<14 and board[Row][Col+1]==0:
                moves.append(chr(Row+65)+str(Col+1))

        move=moves[random.randrange(0,len(moves))]
        turnCounter+=1


    row=ord(move[0])-65
    col=int(move[1:])
    return row,col
