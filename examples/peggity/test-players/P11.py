import random

def whichPlayer(row,col,board,currentPlayer):
    if get(board,row,col)==currentPlayer:
        return 1
    elif get(board,row,col)==0:
        return 0
    else:
        return -1


def check4(board,row,col):
    if get(board,row,col)==0:
        return
    owner=get(board,row,col)
    #Vertical
    Sum=0
    for num in range(1,4):
        if get(board,row-num,col)!=owner:
            break
        Sum+=1
    for num in range(1,4):
        if get(board,row+num,col)!=owner:
            break
        Sum+=1
    if Sum==3:
        for num in range(1,4):
            if get(board,row-num,col)==0:
                return row-num,col
            if get(board,row+num,col)==0:
                return row+num,col

    #Horizontle
    Sum=0
    for num in range(1,4):
        if get(board,row,col-num)!=owner:
            break
        Sum+=1
    for num in range(1,4):
        if get(board,row,col+num)!=owner:
            break
        Sum+=1
    if Sum==3:
        for num in range(1,4):
            if get(board,row,col-num)==0:
                return row,col-num
            if get(board,row,col+num)==0:
                return row,col+num

    #Diag1
    Sum=0
    for num in range(1,4):
        if get(board,row+num,col-num)!=owner:
            break
        Sum+=1
    for num in range(1,4):
        if get(board,row-num,col+num)!=owner:
            break
        Sum+=1
    if Sum==3:
        for num in range(1,4):
            if get(board,row+num,col-num)==0:
                return row+num,col-num
            if get(board,row-num,col+num)==0:
                return row-num,col+num


    #Diag2
    Sum=0
    for num in range(1,4):
        if get(board,row-num,col-num)!=owner:
            break
        Sum+=1
    for num in range(1,4):
        if get(board,row+num,col+num)!=owner:
            break
        Sum+=1
    if Sum==3:
        for num in range(1,4):
            if get(board,row-num,col-num)==0:
                return row-num,col-num
            if get(board,row+num,col+num)==0:
                return row+num,col+num

    return False


def getNeighbor(board,row,col):
    if get(board,row,col-1)==0:
        return row,col-1
    elif get(board,row-1,col)==0:
        return row-1,col
    elif get(board,row-1,col-1)==0:
        return row-1,col-1
    elif get(board,row+1,col+1)==0:
        return row+1,col+1
    elif get(board,row+1,col,)==0:
        return row+1,col
    elif get(board,row,col+1)==0:
        return row,col+1
    elif get(board,row+1,col-1,)==0:
        return row+1,col-1
    elif get(board,row-1,col+1)==0:
        return row-1,col+1
    return False


def get(board,row,col):
    if row<0 or row>14 or col<0 or col>14:
        return -1
    else:
        return board[row][col]


def manualMove(pcolors,currentPlayer,board):
    myPegs=[]
    theirPegs=[]
    
    for row in range(15):
        for col in range(15):
            if get(board,row,col)!=0:
                if get(board,row,col)==currentPlayer:
                    myPegs.append([row,col])
                else:
                    theirPegs.append([row,col])
    for peg in myPegs:
        Win=check4(board,peg[0],peg[1])
        if Win!=False:
            return Win
    for peg in theirPegs:
        Win=check4(board,peg[0],peg[1])
        if Win!=False:
            return Win
        
    random.shuffle(myPegs)
    for peg in myPegs:
        empty=getNeighbor(board,peg[0],peg[1])
        if empty!=False:
            return empty
    random.shuffle(theirPegs)
    for peg in theirPegs:
        empty=getNeighbor(board,peg[0],peg[1])
        if empty!=False:
            return empty
        
        
    if len(myPegs)+len(theirPegs)==0:
        row=random.randint(6,8)
        col=random.randint(6,8)
        return row,col
    else:
        row=random.randint(6,8)
        col=random.randint(6,8)
        return row,col
    
    return row,col
