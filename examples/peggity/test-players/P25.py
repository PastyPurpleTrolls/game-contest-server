import random
def manualMove(pcolors,currentPlayer,board):
    emptyCellsList=[]
    for row in range(15):
        for col in range(15):
            if board[row][col]==0:
                emptyCellsList.append(chr(65+row)+str(col))
    x=random.randrange(0,len(emptyCellsList))
    if x+1==1 or x-1==1:
        move=emptyCellsList[x]
        row=ord(move[0])-65
        col=int(move[1:])
    return row,col
