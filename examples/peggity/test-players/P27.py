import random
def manualMove(pcolors,currentPlayer,board):
    emptyCellsList=[]
    nextTo=[]
    both=[]
    move=""
    boardEmpty=True
    for row in range(15):
        for col in range(11):
            if board[row][col]==board[row][col+1] and board[row][col]==board[row][col+2] and board[row][col]==board[row][col+3] and board[row][col]!=0:
                move=(chr(65+row)+str(col+4))
            if board[row][14]==board[row][12] and board[row][14]==board[row][13] and board[row][11]==board[row][14] and board[row][11]!=0:
                move=(chr(65+row)+str(10))
    for row in range(11):
        for col in range(15):
            if board[row][col]==board[row+1][col] and board[row][col]==board[row+2][col] and board[row][col]==board[row+3][col] and board[row][col]!=0:
                move=(chr(69+row)+str(col))
            if board[13][col]==board[14][col] and board[14][col]==board[12][col] and board[14][col]==board[11][col] and board[11][col]!=0:
                move=(chr(75)+str(col))
    for row in range(11):
        for col in range(11):
            if board[row][col]==board[row+1][col+1] and board[row][col]==board[row+2][col+2] and board[row][col]==board[row+3][col+3] and board[row][col]!=0:
                move=(chr(69+row)+str(col+4))
    for col in range(1,11):   
        if board[13][col+2]==board[14][col+3] and board[14][col+3]==board[12][col+1] and board[14][col+3]==board[11][col] and board[11][col]!=0:
            move=(chr(75)+str(col-1))
    for row in range(1,11):
        if board[row+2][13]==board[row+3][14] and board[row+3][14]==board[row+1][12] and board[row+3][14]==board[row][11] and board[row][11]!=0:
            move=(chr(64+row)+str(10))
    for row in range(15):
        for col in range(15):
            if board[row][col]==0:
                emptyCellsList.append(chr(65+row)+str(col))
            else:
                boardEmpty=False
    if board[0][0]!=0:
        nextTo.append(chr(65)+str(1))
        nextTo.append(chr(66)+str(1))
        nextTo.append(chr(66)+str(0))
    if board[0][14]!=0:
        nextTo.append(chr(66)+str(14))
        nextTo.append(chr(65)+str(13))
        nextTo.append(chr(66)+str(13))
    if board[14][0]!=0:
        nextTo.append(chr(79)+str(1))
        nextTo.append(chr(78)+str(1))
        nextTo.append(chr(78)+str(0))
    if board[14][14]!=0:
        nextTo.append(chr(78)+str(14))
        nextTo.append(chr(78)+str(13))
        nextTo.append(chr(79)+str(13))
    for col in range(1,14):
        if board[0][col]!=0:
            nextTo.append(chr(65)+str(col-1))
            nextTo.append(chr(66)+str(col-1))
            nextTo.append(chr(66)+str(col))
            nextTo.append(chr(65)+str(col+1))
            nextTo.append(chr(66)+str(col+1))
        if board[14][col]!=0:
            nextTo.append(chr(79)+str(col-1))
            nextTo.append(chr(78)+str(col-1))
            nextTo.append(chr(78)+str(col))
            nextTo.append(chr(79)+str(col+1))
            nextTo.append(chr(78)+str(col+1))
    for row in range(1,14):
        if board[row][0]!=0:
            nextTo.append(chr(65+row)+str(1))
            nextTo.append(chr(66+row)+str(1))
            nextTo.append(chr(64+row)+str(1))
            nextTo.append(chr(65+row)+str(0))
            nextTo.append(chr(64+row)+str(0))
        if board[row][14]!=0:
            nextTo.append(chr(65+row)+str(13))
            nextTo.append(chr(66+row)+str(13))
            nextTo.append(chr(64+row)+str(13))
            nextTo.append(chr(65+row)+str(14))
            nextTo.append(chr(64+row)+str(14))
        for col in range(1,14):
            if board[row][col]!=0:
                nextTo.append(chr(65+row)+str(col+1))
                nextTo.append(chr(66+row)+str(col+1))
                nextTo.append(chr(64+row)+str(col+1))
                nextTo.append(chr(65+row)+str(col-1))
                nextTo.append(chr(64+row)+str(col-1))
                nextTo.append(chr(66+row)+str(col-1))
                nextTo.append(chr(66+row)+str(col))
                nextTo.append(chr(64+row)+str(col))
    if boardEmpty==True and move=="":
        move=emptyCellsList[random.randrange(0,len(emptyCellsList))]
    elif move=="":
        for i in nextTo:
            if i in emptyCellsList:
                both+=[i]
        move=both[random.randrange(0,len(both))]
    row=ord(move[0])-65
    col=int(move[1:])
    return row,col
