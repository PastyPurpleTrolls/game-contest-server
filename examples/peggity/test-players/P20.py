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
##                if board[row][col] == 2:
##                    x=(chr(65+row)+str(col))
##                    celloptionslist.append(x)
##                    print(celloptionslist.append(x))
            if row <11 and board[row][col]==board[row+1][col] and board[row][col]!=0 and board[row][col]==board[row+2][col] and board[row][col]==board[row+3][col]:
##                print("1!")
                if  board[row+4][col]==0:
                    return row+4,col
                elif row>0 and board[row-1][col]==0:
                    return row-1,col
            if col <11 and board[row][col]==board[row][col+1] and board[row][col]!=0 and board[row][col]==board[row][col+2] and board[row][col]==board[row][col+3]:
##                print("2!")
                if board[row][col+4]==0:
                    return row,col+4
                elif col>0 and board[row][col-1]==0:
                    return row,col-1
            if row<11 and col <11 and board[row][col]==board[row+1][col+1] and board[row][col]!=0 and board[row][col]==board[row+2][col+2] and board[row][col]==board[row+3][col+3]:
##                print("3!")
                if board[row+4][col+4]==0:
                    return row+4,col+4
                elif row>0 and col>0 and board[row-1][col-1]==0:
                    return row-1,col-1
            if row<11 and col>3 and board[row][col]==board[row+1][col-1] and board[row][col]!=0 and board[row][col]==board[row+2][col-2] and board[row][col]==board[row+3][col-3]:
##                print("4!")
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
##      x=takenCellsList[-1]
##        a=chr(ord(x[0])+1)+(str(int(x[1:])+1))
##        b=chr(ord(x[0])+1)+(str(int(x[1:])))
##        c=chr(ord(x[0])+1)+(str(int(x[1:])-1))
##        d=chr(ord(x[0])-1)+(str(int(x[1:])+1))
##        e=chr(ord(x[0])-1)+(str(int(x[1:])))
##        f=chr(ord(x[0])-1)+(str(int(x[1:])-1))
##        g=chr(ord(x[0]))+(str(int(x[1:])+1))
##        h=chr(ord(x[0]))+(str(int(x[1:])-1))
##        newlist=[a,b,c,d,e,f,g,h]
##        move=newlist[random.randrange(0,len(newlist))]
        
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
            
##    move=emptyCellsList[random.randrange(0,len(emptyCellsList))]

    

    
    



##
