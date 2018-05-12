###Notes

#Remember to Check Diagnols
#5/10/16:  Issue with diagnol
#
import random
def manualMove(pcolors,currentPlayer,board):
    emptyCellsList=[]
    takenCellsList=[]
    celloptionslist=[]
    newlist=[]
    for row in range(15):
        for col in range(15):
            if board[row][col]==0:
                emptyCellsList.append([row,col])
            else:
                takenCellsList.append([row,col])
            if row <11 and board[row][col]==board[row+1][col] and board[row][col]!=0 and board[row][col]==board[row+2][col] and board[row][col]==board[row+3][col]:
                if  board[row+4][col]==0:
                    return row+4,col
                elif row>0 and board[row-1][col]==0:
                    return row-1,col
            if col <11 and board[row][col]==board[row][col+1] and board[row][col]!=0 and board[row][col]==board[row][col+2] and board[row][col]==board[row][col+3]:
                if board[row][col+4]==0:
                    return row,col+4
                elif col>0 and board[row][col-1]==0:
                    return row,col-1
            if row<11 and col <11 and board[row][col]==board[row+1][col+1] and board[row][col]!=0 and board[row][col]==board[row+2][col+2] and board[row][col]==board[row+3][col+3]:
                if board[row+4][col+4]==0:
                    return row+4,col+4    
                elif row>0 and col>0 and board[row-1][col-1]==0:
                    return row-1,col-1
            if row<11 and col>3 and board[row][col]==board[row+1][col-1] and board[row][col]!=0 and board[row][col]==board[row+2][col-2] and board[row][col]==board[row+3][col-3]:
                if board[row+4][col-4]==0:
                    return row+4,col-4
                elif col<14 and row>0 and board[row-1][col+1]==0:
                    return row-1,col+1
    if takenCellsList==[]:
        move=emptyCellsList[random.randrange(0,len(emptyCellsList)-2)]
        row=move[0]
        col=move[1]
        return row,col
    else:
        while True:
            move=takenCellsList[random.randrange(0,len(takenCellsList))]
            row=move[0]
            col=move[1]
            rnd=random.randrange(4)
            
            if row>0 and rnd==0:
                row-=1
            elif col>0 and rnd ==1:
                col-=1
            elif row<14 and rnd==2:
                row+=1
            elif col<14 and rnd==3:
                 col+=1
            if [row,col] in emptyCellsList:
                return row,col