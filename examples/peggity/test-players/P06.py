import random
def manualMove(pcolors,currentPlayer,board):
    if inboard(currentPlayer,board)==False:
        y=random.randint(4,10)
        x=random.randint(4,10)
        return x,x
    for i in range (len(board)):
        for x in range (len(board[i])):
            if i<=11 and i>=1 and board[i][x]==1 and board[i+1][x]==1 and board[i+2][x]==1:
                if board[i+3][x]==0:
                    return (i+3,x)
                elif board[i-1][x]==0:
                    return (i-1,x)
                else:
                    ifNoMove(currentPlayer,board)
            elif x<=11 and x>=1 and board[i][x]==1 and board[i][x+1]==1 and board[i][x+2]==1:
                if board[i][x+3]==0:
                    return (i,x+3)
                elif board[i-1][x]==0:
                    return (i,x-1)
                else:
                    ifNoMove(currentPlayer,board)
            elif x<=11 and i<=11 and x>=1 and i>=1 and board[i][x]==1 and board[i+1][x+1]==1 and board[i+2][x+2]==1:
                if board[i+3][x+3]==0:
                    return (i+3,x+3)
                elif board[i-1][x-1]==0:
                    return (i-1,x-1)
                else:
                    ifNoMove(currentPlayer,board)
            elif x<=14 and i<=11 and x>=4 and i>=1 and board[i][x]==1 and board[i+1][x-1]==1 and board[i+2][x-2]==1:
                if board[i+3][x-3]==0:
                    return (i+3,x-3)
                elif board[i-1][x-1]==0:
                    return (i-1,x+1)
                else:
                    ifNoMove(currentPlayer,board)
    for i in range (len(board)):
        for x in range (len(board[i])):
            if i<=11 and i>=1 and board[i][x]==2 and board[i+1][x]==2 and board[i+2][x]==2:
                if board[i+3][x]==0:
                    return (i+3,x)
                elif board[i-1][x]==0:
                    return (i-1,x)
                else:
                    return randomNext(currentPlayer,board)
            elif x<=11 and x>=1 and board[i][x]==2 and board[i][x+1]==2 and board[i][x+2]==2:
                if board[i][x+3]==0:
                    return (i,x+3)
                elif board[i-1][x]==0:
                    return (i,x-1)
                else:
                    return randomNext(currentPlayer,board)
            elif x<=11 and x>=1 and i>=1 and i<=11 and board[i][x]==2 and board[i+1][x+1]==2 and board[i+2][x+2]==2:
                if board[i+3][x+3]==0:
                    return (i+3,x+3)
                elif board[i-1][x-1]==0:
                    return (i-1,x-1)
                else:
                    return randomNext(currentPlayer,board)
            elif x<=14 and i<=11 and x>=4 and i>=2 and board[i][x]==2 and board[i+1][x-1]==2 and board[i+2][x-2]==2:
                if board[i+3][x-3]==0:
                    return (i+3,x-3)
                elif board[i-1][x-1]==0:
                    return (i-1,x+1)
                else:
                    return randomNext(currentPlayer,board)
    else:
        for i in range (len(board)):
            for x in range (len(board[i])):
                if board[i][x]==currentPlayer:
                    z=random.randint(1,4)
                    if z==1 and x>=1 and x<14 and i<14 and i>=1:
                        return (i+1,x)
                    elif z==2 and x>=1 and x<14 and i<14 and i>=1:
                        return (i-1,x)
                    elif z==3 and x>=1 and x<14 and i<14 and i>=1:
                        return (i,x+1)
                    elif z==4 and x>=1 and x<14 and i<14 and i>=1:
                        return (i,x-1)

def inboard(currentPlayer,board):
    for i in board:
        if currentPlayer in i:
            return True
    return False

def ifNoMove(currentPlayer,board):
    for i in range (len(board)):
        for x in range (len(board[i])):
            if i<=11 and i>=1 and board[i][x]==2 and board[i+1][x]==2 and board[i+2][x]==2:
                if board[i+3][x]==0:
                    return (i+3,x)
                elif board[i-1][x]==0:
                    return (i-1,x)
                else:
                    return randomNext(currentPlayer,board)
            elif x<=11 and x>=1 and board[i][x]==2 and board[i][x+1]==2 and board[i][x+2]==2:
                if board[i][x+3]==0:
                    return (i,x+3)
                elif board[i-1][x]==0:
                    return (i,x-1)
                else:
                    return randomNext(currentPlayer,board)
            elif x<=11 and x>=1 and i>=1 and i<=11 and board[i][x]==2 and board[i+1][x+1]==2 and board[i+2][x+2]==2:
                if board[i+3][x+3]==0:
                    return (i+3,x+3)
                elif board[i-1][x-1]==0:
                    return (i-1,x-1)
                else:
                    return randomNext(currentPlayer,board)
            elif x<=14 and i<=11 and x>=4 and i>=2 and board[i][x]==2 and board[i+1][x-1]==2 and board[i+2][x-2]==2:
                if board[i+3][x-3]==0:
                    return (i+3,x-3)
                elif board[i-1][x-1]==0:
                    return (i-1,x+1)
                else:
                    return randomNext(currentPlayer,board)

def randomNext(currentPlayer,board):
    for i in range (len(board)):
            for x in range (len(board[i])):
                if board[i][x]==currentPlayer:
                    z=random.randint(1,4)
                    if z==1 and x>=1 and x<14 and i<14 and i>=1:
                        if board[i+1][x]==0:
                            return (i+1,x)
                        else:
                            return genRandom()
                    elif z==2 and x>=1 and x<14 and i<14 and i>=1:
                        if board[i-1][x]==0:
                            return (i-1,x)
                        else:
                            return genRandom()
                    elif z==3 and x>=1 and x<14 and i<14 and i>=1:
                        if board[i][x+1]==0:
                            return (i,x+1)
                        else:
                            return genRandom()
                    elif z==4 and x>=1 and x<14 and i<14 and i>=1:
                        if board[i][x-1]==0:
                            return (i,x-1)
                        else:
                            return genRandom()

def genRandom():
    x=random.randint(2,13)
    y=random.randint(2,13)
    return (x,y)
    
                    
