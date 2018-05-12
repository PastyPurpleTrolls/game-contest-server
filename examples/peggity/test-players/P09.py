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
def check1(row,col,board):
    if row < len(board)-1 and col<len(board)-1 and row>=0 and col>=0 and board[row][col] == 0:
        return True
    else:
        return False
def manualMove(pcolors,currentPlayer,board):
    emptylist=[]
    bestmove= []
    for x in range(len(board)):
        for y in range(len(board)):
            if board[x][y]!=0:
                emptylist.append([x,y])
            else:
                pass
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col]!=0:
                #horizontal
                if col<11:
                    count=1
                    for offset in range(1,4,1):
                        if board[row][col]==board[row][col+offset]:
                            count+=1
                    if count==4:
                        if(board[row][col+4]==0):
                            bestmove.append([row,col+4])
                        if(check1(row,col-1,board)):
                            if(board[row][col-1]==0):
                                bestmove.append([row,col-1])
                #vertical
                if row<11:
                    count=1
                    for offset in range(1,4,1):
                        if board[row][col]==board[row+offset][col]:
                            count+=1
                    if count==4:
                        if(board[row+4][col]==0):
                            bestmove.append([row+4,col])
                        if(check1(row-1,col,board)):
                            if(board[row-1][col]==0):
                                bestmove.append([row-1,col])
                #CHECK DIAGONALS
                #left to right
                if row<11 and col<11:
                    count=1
                    for offset in range(1,4,1):
                        if board[row][col]==board[row+offset][col+offset]:
                            count+=1
                    if count==4:
                        if(board[row+4][col+4]==0):
                            bestmove.append([row+4,col+4])
                        if(check1(row-1,col-1,board)):
                            if(board[row-1][col-1]==0):
                                bestmove.append([row-1,col-1])
                #right to left
                if row<11 and col>3:
                    count=1
                    for offset in range(1,4,1):
                        if board[row][col]==board[row+offset][col-offset]:
                            count+=1
                    if count==4:
                        if(board[row+4][col-4]==0):
                            bestmove.append([row+4,col-4])
                        if(check1(row-1,col+1,board)):
                            if(board[row-1][col+1]==0):
                                bestmove.append([row-1,col+1])
    moveList=[]
    if(len(bestmove)==0):
        for something in emptylist:
            if check1(something[0]+1,something[1],board):
                moveList.append([something[0]+1,something[1]])
            if check1(something[0]-1,something[1],board):
                moveList.append([something[0]-1,something[1]])
            if check1(something[0]+1,something[1]+1,board):
                moveList.append([something[0]+1,something[1]+1])
            if check1(something[0]+1,something[1]-1,board):
                moveList.append([something[0]+1,something[1]-1])
            if check1(something[0]-1,something[1]+1,board):
                moveList.append([something[0]-1,something[1]+1])
            if check1(something[0]-1,something[1]-1,board):
                moveList.append([something[0]-1,something[1]-1])
            if check1(something[0],something[1]+1,board):
                moveList.append([something[0],something[1]+1])
            if check1(something[0],something[1]-1,board):
                moveList.append([something[0],something[1]-1])
        if(len(moveList)>0):
            rand1= random.randint(0,len(moveList)-1)
        else:
            rand1 = 0
            moveList = [[0,0]]
    else:
        rand1 = 0
        moveList = [[bestmove[0][0],bestmove[0][1]]]
    return moveList[rand1][0], moveList[rand1][1]
            
