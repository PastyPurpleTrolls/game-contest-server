import random
def manualMove(pcolors,currentPlayer,board):
    emptyCellsList=[]
    for row in range(15):
        for col in range(15):
            if board[row][col]==0:
                emptyCellsList.append(chr(65+row)+str(col))
    move=emptyCellsList[random.randrange(0,len(emptyCellsList))]
    row=ord(move[0])-65
    col=int(move[1:])
    return row,col

def fourInARow(board):
    move=["",""]
    for row in range(len(board)):       #Horizontal
        for col in range(len(board[row])-4):
            if board[row][col]==board[row][col+1] and board[row][col+1]==board[row][col+2] and board[row][col+2]==board[row][col+3] and board[row][col+1]!=0:
                if board[row][col+4]==0:
                    move[0]=row
                    move[1]=col+4
                    return move
                else:
                    return move
    for row in range(len(board)):       #HorizontalEdge
        for col in range(len(board[row])-3):
            if board[row][col]==board[row][col+1] and board[row][col+1]==board[row][col+2] and board[row][col+2]==board[row][col+3] and board[row][col+1]!=0:
                if board[row][col-1]==0:
                    move[0]=row
                    move[1]=col-1
                    return move
                else:
                    return move
    for col in range(len(board)):       #Vertical
        for row in range(len(board)-4):
            if board[row][col]==board[row+1][col] and board[row+1][col]==board[row+2][col] and board[row+2][col]==board[row+3][col] and board[row+1][col]!=0:
                if board[row+4][col]==0:
                    move[0]=row+4
                    move[1]=col
                    return move
                else:
                    return move
    for col in range(len(board)):       #VerticalEdge
        for row in range(len(board)-3):
            if board[row][col]==board[row+1][col] and board[row+1][col]==board[row+2][col] and board[row+2][col]==board[row+3][col] and board[row+1][col]!=0:
                if board[row-1][col]==0:
                    move[0]=row-1
                    move[1]=col
                    return move
                else:
                    return move
    for row in range(len(board)-4):       #DiagProg
        for col in range(len(board)-3):
            if board[row][col]==board[row+1][col+1] and board[row+1][col+1]==board[row+2][col+2] and board[row+2][col+2]==board[row+3][col+3] and board[row+1][col+1]!=0:
                if board[row+4][col+4]==0:
                    move[0]=row+4
                    move[1]=col+4
                    return move
                else:
                    return move
    for row in range(len(board)-3):       #DiagProgCorner
        for col in range(len(board)-3):
            if board[row][col]==board[row+1][col+1] and board[row+1][col+1]==board[row+2][col+2] and board[row+2][col+2]==board[row+3][col+3] and board[row+1][col+1]!=0:
                if board[row-1][col-1]==0:
                    move[0]=row-1
                    move[1]=col-1
                    return move
                else:
                    return move
    for row in range(len(board)-3):       #DiagDecrease
        for col in range(4,len(board)):
            if board[row][col]==board[row+1][col-1] and board[row+1][col-1]==board[row+2][col-2] and board[row+2][col-2]==board[row+3][col-3] and board[row+1][col-1]!=0:
                if board[row+4][col-4]==0:
                    move[0]=row+4
                    move[1]=col-4
                    return move
                else:
                    return move
    for row in range(len(board)-3):       #DiagDecreaseCorner
        for col in range(0,len(board)-3):
            if board[row][col]==board[row+1][col-1] and board[row+1][col-1]==board[row+2][col-2] and board[row+2][col-2]==board[row+3][col-3] and board[row+1][col-1]!=0:
                if board[row-1][col+1]==0:
                    move[0]=row-1
                    move[1]=col+1
                    return move
                else:
                    return move
    return move

def automatedMove(pcolors,currentPlayer,board):
    possibleMovesList=[]
    rowCount=0
    move=fourInARow(board)
##    print(move)
    if move[0]=="":
        for row in board:
            colCount=0
            for col in row:
                if board[rowCount][colCount]!=0:
                    if rowCount!=0 and rowCount!=len(board)-1 and colCount!=0 and colCount!=len(board)-1:    #Middle
                        possibleMovesList.append([rowCount-1,colCount+1])
                        possibleMovesList.append([rowCount,colCount+1])
                        possibleMovesList.append([rowCount+1,colCount+1])
                        possibleMovesList.append([rowCount-1,colCount])
                        possibleMovesList.append([rowCount+1,colCount])
                        possibleMovesList.append([rowCount-1,colCount-1])
                        possibleMovesList.append([rowCount,colCount-1])
                        possibleMovesList.append([rowCount+1,colCount-1])
                    elif rowCount!=0 and colCount==0 and rowCount!=len(board)-1:   #left
                        possibleMovesList.append([rowCount+1,colCount])
                        possibleMovesList.append([rowCount+1,colCount+1])
                        possibleMovesList.append([rowCount,colCount+1])
                        possibleMovesList.append([rowCount-1,colCount+1])
                        possibleMovesList.append([rowCount-1,colCount])
                    elif rowCount!=len(board)-1 and rowCount!=0 and colCount==len(board)-1:   #right
                        possibleMovesList.append([rowCount+1,colCount])
                        possibleMovesList.append([rowCount+1,colCount-1])
                        possibleMovesList.append([rowCount,colCount-1])
                        possibleMovesList.append([rowCount-1,colCount-1])
                        possibleMovesList.append([rowCount-1,colCount])
                    elif rowCount==0 and colCount!=0 and colCount!=len(board)-1:  #Top
                        possibleMovesList.append([rowCount,colCount-1])
                        possibleMovesList.append([rowCount+1,colCount-1])
                        possibleMovesList.append([rowCount+1,colCount])
                        possibleMovesList.append([rowCount+1,colCount+1])
                        possibleMovesList.append([rowCount,colCount+1])
                    elif rowCount==len(board)-1 and colCount!=0 and colCount!=len(board)-1:  #Bottom
                        possibleMovesList.append([rowCount,colCount-1])
                        possibleMovesList.append([rowCount-1,colCount-1])
                        possibleMovesList.append([rowCount-1,colCount])
                        possibleMovesList.append([rowCount-1,colCount+1])
                        possibleMovesList.append([rowCount,colCount+1])
                    elif rowCount==0 and colCount==0:   #UpperLeft
                        possibleMovesList.append([rowCount,colCount+1])
                        possibleMovesList.append([rowCount+1,colCount+1])
                        possibleMovesList.append([rowCount+1,colCount])
                    elif rowCount==0 and colCount==len(board)-1:   #UpperRight
                        possibleMovesList.append([rowCount,colCount-1])
                        possibleMovesList.append([rowCount+1,colCount-1])
                        possibleMovesList.append([rowCount+1,colCount])
                    elif rowCount==len(board)-1 and colCount==len(board)-1:   #LowerRight
                        possibleMovesList.append([rowCount,colCount-1])
                        possibleMovesList.append([rowCount-1,colCount-1])
                        possibleMovesList.append([rowCount-1,colCount])
                    elif rowCount==0 and colCount==len(board)-1:   #LowerLeft
                        possibleMovesList.append([rowCount,colCount+1])
                        possibleMovesList.append([rowCount-1,colCount+1])
                        possibleMovesList.append([rowCount-1,colCount])
                colCount+=1
            rowCount+=1
##        print(possibleMovesList)
        if possibleMovesList==[]:
            row,col=manualMove(pcolors,currentPlayer,board)
            return row,col
        randomIDX=random.randrange(0,len(possibleMovesList))
        randomMoveList=possibleMovesList[randomIDX]             
        x=randomMoveList[0]
        y=randomMoveList[1]
        return x,y
    else:
        return move
            
                
            
            
