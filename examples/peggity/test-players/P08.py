import random
def manualMove(pcolors,currentPlayer,board):
    emptyCellsList=[]
    manualMoveList=[]
    finishWinList=[]
    for row in range(15):
        for col in range(15):
            if board[row][col]==0:
                emptyCellsList.append(chr(65+row)+str(col))
            if board[row][col]!=0:
                #horizontal
                if col<11:
                    count=1
                    for offset in range(1,4):
                        if board[row][col]==board[row][col+offset]:
                            count+=1
                    if count==4:
                        finishWinList.append([row,col-1])
                        finishWinList.append([row,col+4])
                #vertical
                if row<11:
                    count=1
                    for offset in range(1,4):
                        if board[row][col]==board[row+offset][col]:
                            count+=1
                    if count==4:
                        finishWinList.append([row-1,col])
                        finishWinList.append([row+4,col])
                #CHECK DIAGONALS
                #left to right
                if row<11 and col<11:
                    count=1
                    for offset in range(1,4):
                        if board[row][col]==board[row+offset][col+offset]:
                            count+=1
                    if count==4:
                        finishWinList.append([row-1,col-1])
                        finishWinList.append([row+4,col+4])
                #right to left
                if row<11 and col>3:
                    count=1
                    for offset in range(1,4):
                        if board[row][col]==board[row+offset][col-offset]:
                            count+=1
                    if count==4:
                        finishWinList.append([row-1,col+1])
                        finishWinList.append([row+4,col-4])
            if board[row][col]!=0:
                manualMoveList.append([row,col])
    if finishWinList!=[]:
        newFWL=[]
        for point in finishWinList:
            row=(chr(65+point[0]))
            cell=row+str(point[1])
            if cell in emptyCellsList:
                newFWL.append(point)
        if newFWL==[]:
            posMove=random.choice(emptyCellsList)
        else:
            posMove=random.choice(newFWL)
        if posMove in emptyCellsList:
            move=posMove
        else:
            row=(chr(65+posMove[0]))
            cell=row+str(posMove[1])
            move=cell
    elif manualMoveList!=[]:
        randCell=random.choice(manualMoveList)
        row=(chr(65+randCell[0]))
        cell=row+str(randCell[1])
        tempList=[]
        acc=0
        att=0
        app=0
        for i in range(3):
            newRow=chr(ord(row)-1)
            if acc==0:
                tempList.append(newRow+str((randCell[1])-1))
            if acc==1:
                tempList.append(newRow+str(randCell[1]))
            if acc==2:
                tempList.append(newRow+str((randCell[1])+1))
            acc+=1
        for i in range(2):
            newRow=chr(ord(row))
            if att==0:
                tempList.append(newRow+str((randCell[1])-1))
            if att==1:
                tempList.append(newRow+str((randCell[1])+1))
            att+=1
        for i in range(3):
            newRow=chr(ord(row)+1)
            if app==0:
                tempList.append(newRow+str((randCell[1])-1))
            if app==1:
                tempList.append(newRow+str(randCell[1]))
            if app==2:
                tempList.append(newRow+str((randCell[1])+1))
            app+=1
        posMove=random.choice(tempList)
        if posMove not in emptyCellsList:
            posMove=tempList[random.randrange(0,2)]
        move=posMove
    else:
        move=emptyCellsList[random.randrange(0,len(emptyCellsList))]
    row=ord(move[0])-65
    col=int(move[1:])
    return row,col



