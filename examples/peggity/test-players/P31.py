import random
def manualMove(pcolors,currentPlayer,board):
    emptyCells=[]
    pegs=[]
    myPegs=[]
    for row in range(15):
        for col in range(15):
            if board[row][col]==0:
                emptyCells.append(chr(65+row)+str(col))
            else:
                pegs.append(chr(65+row)+str(col))
                if board[row][col] == currentPlayer:
                    myPegs.append(chr(65+row)+str(col))
    fourFound = False
    for locations in myPegs:
        pegrow = ord(locations[0])-65
        chosenPegCol = int(locations[1:])
        upCheckForFour1=chr(65+pegrow-1)+str(chosenPegCol)
        upCheckForFour2=chr(65+pegrow-2)+str(chosenPegCol)
        upCheckForFour3=chr(65+pegrow-3)+str(chosenPegCol)
        upCheckForFour4=chr(65+pegrow-4)+str(chosenPegCol)
        if((upCheckForFour1 in myPegs) and (upCheckForFour2 in myPegs) and (upCheckForFour3 in myPegs) and (upCheckForFour4 in emptyCells)):
            fourFound = True
            move = upCheckForFour4
            break
        downCheckForFour1=chr(65+pegrow+1)+str(chosenPegCol)
        downCheckForFour2=chr(65+pegrow+2)+str(chosenPegCol)
        downCheckForFour3=chr(65+pegrow+3)+str(chosenPegCol)
        downCheckForFour4=chr(65+pegrow+4)+str(chosenPegCol)
        if((downCheckForFour1 in myPegs) and (downCheckForFour2 in myPegs) and (downCheckForFour3 in myPegs) and (downCheckForFour4 in emptyCells)):
            fourFound = True
            move = downCheckForFour4
            break
        rightCheckForFour1=chr(65+pegrow)+str(chosenPegCol+1)
        rightCheckForFour2=chr(65+pegrow)+str(chosenPegCol+2)
        rightCheckForFour3=chr(65+pegrow)+str(chosenPegCol+3)
        rightCheckForFour4=chr(65+pegrow)+str(chosenPegCol+4)
        if((rightCheckForFour1 in myPegs) and (rightCheckForFour2 in myPegs) and (rightCheckForFour3 in myPegs) and (rightCheckForFour4 in emptyCells)):
            fourFound = True
            move = rightCheckForFour4
            break
        leftCheckForFour1=chr(65+pegrow)+str(chosenPegCol-1)
        leftCheckForFour2=chr(65+pegrow)+str(chosenPegCol-2)
        leftCheckForFour3=chr(65+pegrow)+str(chosenPegCol-3)
        leftCheckForFour4=chr(65+pegrow)+str(chosenPegCol-3)
        if((leftCheckForFour1 in myPegs) and (leftCheckForFour2 in myPegs) and (leftCheckForFour3 in myPegs) and (leftCheckForFour4 in emptyCells)):
            fourFound = True
            move = leftCheckForFour4
            break
        diaCheck1 =chr(65+pegrow+1)+str(chosenPegCol+1)
        diaCheck2 =chr(65+pegrow+2)+str(chosenPegCol+2)
        diaCheck3 =chr(65+pegrow+3)+str(chosenPegCol+3)
        diaCheck4 =chr(65+pegrow+4)+str(chosenPegCol+4)
        if((diaCheck1 in myPegs) and (diaCheck2 in myPegs) and (diaCheck3 in myPegs) and (diaCheck4 in emptyCells)):
            fourFound = True
            move = diaCheck4
            break
        RdiaCheck1 =chr(65+pegrow+1)+str(chosenPegCol-1)
        RdiaCheck2 =chr(65+pegrow+2)+str(chosenPegCol-2)
        RdiaCheck3 =chr(65+pegrow+3)+str(chosenPegCol-3)
        RdiaCheck4 =chr(65+pegrow+4)+str(chosenPegCol-4)
        if((RdiaCheck1 in myPegs) and (RdiaCheck2 in myPegs) and (RdiaCheck3 in myPegs) and (RdiaCheck4 in emptyCells)):
            fourFound = True
            move = RdiaCheck4
            break
        NdiaCheck1 =chr(65+pegrow-1)+str(chosenPegCol+1)
        NdiaCheck2 =chr(65+pegrow-2)+str(chosenPegCol+2)
        NdiaCheck3 =chr(65+pegrow-3)+str(chosenPegCol+3)
        NdiaCheck4 =chr(65+pegrow-4)+str(chosenPegCol+4)
        if((NdiaCheck1 in myPegs) and (NdiaCheck2 in myPegs) and (NdiaCheck3 in myPegs) and (NdiaCheck4 in emptyCells)):
            fourFound = True
            move = NdiaCheck4
            break
        NRdiaCheck1 =chr(65+pegrow-1)+str(chosenPegCol-1)
        NRdiaCheck2 =chr(65+pegrow-2)+str(chosenPegCol-2)
        NRdiaCheck3 =chr(65+pegrow-3)+str(chosenPegCol-3)
        NRdiaCheck4 =chr(65+pegrow-4)+str(chosenPegCol-4)
        if((NRdiaCheck1 in myPegs) and (NRdiaCheck2 in myPegs) and (NRdiaCheck3 in myPegs) and (NRdiaCheck4 in emptyCells)):
            fourFound = True
            move = NRdiaCheck4
            break
        
    if(len(myPegs) > 0 and not fourFound):
        validMove = False
        while(not validMove):
            chosenPeg=pegs[random.randrange(0,len(pegs))]
            chosenPegRow = ord(chosenPeg[0])-65
            chosenPegCol = int(chosenPeg[1:])
            
            upCheck = chr(65+pegrow-1)+str(chosenPegCol)
            rightCheck = chr(65+pegrow)+str(chosenPegCol + 1)
            downCheck = chr(65+pegrow+1)+str(chosenPegCol)
            leftCheck = chr(65+pegrow)+str(chosenPegCol - 1)
            if(upCheck in emptyCells):
                move = upCheck
                validMove = True
            elif(rightCheck in emptyCells):
                move = rightCheck
                validMove = True
            elif(downCheck in emptyCells):
                move = downCheck
                validMove = True
            elif(leftCheck in emptyCells):
                move = leftCheck
                validMove = True
            else:
                validMove = False
    elif(not fourFound):
        move=emptyCells[random.randrange(0,len(emptyCells))]
            
    row=ord(move[0])-65
    col=int(move[1:])
    return row,col

