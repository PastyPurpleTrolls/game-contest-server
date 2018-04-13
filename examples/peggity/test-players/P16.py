import random
def manualMove(pcolors,currentPlayer,board):
    emptyCellsList=[]
    pegLocations=[]
    myPegLocations=[]
    for row in range(15):
        for col in range(15):
            if board[row][col]==0:
                emptyCellsList.append(chr(65+row)+str(col))
            else:
                pegLocations.append(chr(65+row)+str(col))
                if board[row][col] == currentPlayer:
                    myPegLocations.append(chr(65+row)+str(col))
    fourFound = False
    for eachLocation in myPegLocations:
        chosenPegRow = ord(eachLocation[0])-65
        chosenPegCol = int(eachLocation[1:])
        #HORIZONTAL AND VERTICAL PLACEMENT#
        upCheckForFour1=chr(65+chosenPegRow-1)+str(chosenPegCol)
        upCheckForFour2=chr(65+chosenPegRow-2)+str(chosenPegCol)
        upCheckForFour3=chr(65+chosenPegRow-3)+str(chosenPegCol)
        upCheckForFour4=chr(65+chosenPegRow-4)+str(chosenPegCol)
        if((upCheckForFour1 in myPegLocations) and (upCheckForFour2 in myPegLocations) and (upCheckForFour3 in myPegLocations) and (upCheckForFour4 in emptyCellsList)):
            fourFound = True
            move = upCheckForFour4
            break
        downCheckForFour1=chr(65+chosenPegRow+1)+str(chosenPegCol)
        downCheckForFour2=chr(65+chosenPegRow+2)+str(chosenPegCol)
        downCheckForFour3=chr(65+chosenPegRow+3)+str(chosenPegCol)
        downCheckForFour4=chr(65+chosenPegRow+4)+str(chosenPegCol)
        if((downCheckForFour1 in myPegLocations) and (downCheckForFour2 in myPegLocations) and (downCheckForFour3 in myPegLocations) and (downCheckForFour4 in emptyCellsList)):
            fourFound = True
            move = downCheckForFour4
            break
        rightCheckForFour1=chr(65+chosenPegRow)+str(chosenPegCol+1)
        rightCheckForFour2=chr(65+chosenPegRow)+str(chosenPegCol+2)
        rightCheckForFour3=chr(65+chosenPegRow)+str(chosenPegCol+3)
        rightCheckForFour4=chr(65+chosenPegRow)+str(chosenPegCol+4)
        if((rightCheckForFour1 in myPegLocations) and (rightCheckForFour2 in myPegLocations) and (rightCheckForFour3 in myPegLocations) and (rightCheckForFour4 in emptyCellsList)):
            fourFound = True
            move = rightCheckForFour4
            break
        leftCheckForFour1=chr(65+chosenPegRow)+str(chosenPegCol-1)
        leftCheckForFour2=chr(65+chosenPegRow)+str(chosenPegCol-2)
        leftCheckForFour3=chr(65+chosenPegRow)+str(chosenPegCol-3)
        leftCheckForFour4=chr(65+chosenPegRow)+str(chosenPegCol-3)
        if((leftCheckForFour1 in myPegLocations) and (leftCheckForFour2 in myPegLocations) and (leftCheckForFour3 in myPegLocations) and (leftCheckForFour4 in emptyCellsList)):
            fourFound = True
            move = leftCheckForFour4
            break
        #DIAGONAL PLACEMENT#
        diaCheck1 =chr(65+chosenPegRow+1)+str(chosenPegCol+1)
        diaCheck2 =chr(65+chosenPegRow+2)+str(chosenPegCol+2)
        diaCheck3 =chr(65+chosenPegRow+3)+str(chosenPegCol+3)
        diaCheck4 =chr(65+chosenPegRow+4)+str(chosenPegCol+4)
        if((diaCheck1 in myPegLocations) and (diaCheck2 in myPegLocations) and (diaCheck3 in myPegLocations) and (diaCheck4 in emptyCellsList)):
            fourFound = True
            move = diaCheck4
            break
        RdiaCheck1 =chr(65+chosenPegRow+1)+str(chosenPegCol-1)
        RdiaCheck2 =chr(65+chosenPegRow+2)+str(chosenPegCol-2)
        RdiaCheck3 =chr(65+chosenPegRow+3)+str(chosenPegCol-3)
        RdiaCheck4 =chr(65+chosenPegRow+4)+str(chosenPegCol-4)
        if((RdiaCheck1 in myPegLocations) and (RdiaCheck2 in myPegLocations) and (RdiaCheck3 in myPegLocations) and (RdiaCheck4 in emptyCellsList)):
            fourFound = True
            move = RdiaCheck4
            break
        NdiaCheck1 =chr(65+chosenPegRow-1)+str(chosenPegCol+1)
        NdiaCheck2 =chr(65+chosenPegRow-2)+str(chosenPegCol+2)
        NdiaCheck3 =chr(65+chosenPegRow-3)+str(chosenPegCol+3)
        NdiaCheck4 =chr(65+chosenPegRow-4)+str(chosenPegCol+4)
        if((NdiaCheck1 in myPegLocations) and (NdiaCheck2 in myPegLocations) and (NdiaCheck3 in myPegLocations) and (NdiaCheck4 in emptyCellsList)):
            fourFound = True
            move = NdiaCheck4
            break
        NRdiaCheck1 =chr(65+chosenPegRow-1)+str(chosenPegCol-1)
        NRdiaCheck2 =chr(65+chosenPegRow-2)+str(chosenPegCol-2)
        NRdiaCheck3 =chr(65+chosenPegRow-3)+str(chosenPegCol-3)
        NRdiaCheck4 =chr(65+chosenPegRow-4)+str(chosenPegCol-4)
        if((NRdiaCheck1 in myPegLocations) and (NRdiaCheck2 in myPegLocations) and (NRdiaCheck3 in myPegLocations) and (NRdiaCheck4 in emptyCellsList)):
            fourFound = True
            move = NRdiaCheck4
            break
        
    if(len(pegLocations) > 0 and not fourFound):
        validMove = False
        while(not validMove):
            chosenPeg=pegLocations[random.randrange(0,len(pegLocations))]
            chosenPegRow = ord(chosenPeg[0])-65
            chosenPegCol = int(chosenPeg[1:])
            
            upCheck = chr(65+chosenPegRow-1)+str(chosenPegCol)
            rightCheck = chr(65+chosenPegRow)+str(chosenPegCol + 1)
            downCheck = chr(65+chosenPegRow+1)+str(chosenPegCol)
            leftCheck = chr(65+chosenPegRow)+str(chosenPegCol - 1)
            if(upCheck in emptyCellsList):
                move = upCheck
                validMove = True
            elif(rightCheck in emptyCellsList):
                move = rightCheck
                validMove = True
            elif(downCheck in emptyCellsList):
                move = downCheck
                validMove = True
            elif(leftCheck in emptyCellsList):
                move = leftCheck
                validMove = True
            else:
                validMove = False
    elif(not fourFound):
        move=emptyCellsList[random.randrange(0,len(emptyCellsList))]
            
    row=ord(move[0])-65
    col=int(move[1:])
    return row,col

