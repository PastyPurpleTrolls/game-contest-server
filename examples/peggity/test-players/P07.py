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

def bestMove(board):
    takenSpaces=spaceTaken(board)
    for eachRow in range(len(board)-4):
        for eachCol in range(len(board[eachRow])-4):
            if board[eachRow][eachCol]==board[eachRow+1][eachCol] and board[eachRow+1][eachCol]==board[eachRow+2][eachCol]\
               and board[eachRow+2][eachCol]==board[eachRow+3][eachCol] and board[eachRow][eachCol]!=0:
                if insideBoard(eachRow-1,eachCol):
                    if [eachRow-1,eachCol] not in takenSpaces:
                        return (eachRow-1),eachCol
                elif insideBoard(board[eachRow+4],eachCol):
                    if [eachRow+4,eachCol] not in takenSpaces:
                        return (eachRow+4,eachCol)
            elif board[eachRow][eachCol]==board[eachRow][eachCol+1] and board[eachRow][eachCol+1]==board[eachRow][eachCol+2]\
               and board[eachRow][eachCol+2]==board[eachRow][eachCol+3] and board[eachRow][eachCol]!=0:
                if insideBoard(eachRow,eachCol-1):
                    if [eachRow,eachCol-1] not in takenSpaces:
                        return eachRow,(eachCol-1)
                elif insideBoard(eachRow,eachCol+4):
                    if [eachRow,eachCol+4] not in takenSpaces:
                        return eachRow,(eachCol+4)
            elif board[eachRow][eachCol]==board[eachRow+1][eachCol+1] and board[eachRow+1][eachCol+1]==board[eachRow+2][eachCol+2]\
               and board[eachRow+2][eachCol+2]==board[eachRow+3][eachCol+3] and board[eachRow][eachCol]!=0:
                if insideBoard(eachRow-1,eachCol-1):
                    if [eachRow-1,eachCol-1] not in takenSpaces:
                        return (eachRow-1),(eachCol-1)
                elif insideBoard(eachRow+4,eachCol+4):
                    if [eachRow+4,eachCol+4] not in takenSpaces:
                        return (eachRow+4),(eachCol+4)
    for eachRow in range(len(board)-3):
        for eachCol in range(3,len(board)):
            if board[eachRow][eachCol]==board[eachRow+1][eachCol-1] and board[eachRow+1][eachCol-1]==board[eachRow+2][eachCol-2]\
               and board[eachRow+2][eachCol-2]==board[eachRow+3][eachCol-3] and board[eachRow][eachCol]!=0:
                if insideBoard(eachRow-1,eachCol+1):
                    if [eachRow-1,eachCol+1] not in takenSpaces:
                        return (eachRow-1),(eachCol+1)
                elif insideBoard(eachRow+4,eachCol-4):
                    if [eachRow+4,eachCol-4] not in takenSpaces:
                        return (eachRow+4),(eachCol-4)
    return False

def insideBoard(row,col):
    if row>=0 and row<15 and col>=0 and col<15:
        return True
    return False

def spaceTaken(board):
    takenSpacesList=[]
    for eachRow in range(len(board)-1):
        for eachCol in range(len(board)-1):
            if board[eachRow][eachCol]!=0:
                takenSpacesList.append([eachRow,eachCol])
    return takenSpacesList

def checkAround(board,moves):
    moveOptions=[]
    for eachSpace in moves:
        if (insideBoard(eachSpace[0]-1,eachSpace[1])):
            moveOptions.append([eachSpace[0]-1,eachSpace[1]])
        elif (insideBoard(eachSpace[0]+1,eachSpace[1])):
            moveOptions.append([eachSpace[0]+1,eachSpace[1]])
        elif (insideBoard(eachSpace[0],eachSpace[1]-1)):
            moveOptions.append([eachSpace[0],eachSpace[1]-1])
        elif (insideBoard(eachSpace[0]+1,eachSpace[1]+1)):
            moveOptions.append([eachSpace[0]+1,eachSpace[1]+1])
        elif (insideBoard(eachSpace[0]+1,eachSpace[1]+1)):
            moveOptions.append([eachSpace[0]+1,eachSpace[1]+1])
        elif (insideBoard(eachSpace[0]-1,eachSpace[1]-1)):
            moveOptions.append([eachSpace[0]-1,eachSpace[1]-1])
        elif (insideBoard(eachSpace[0]+1,eachSpace[1]-1)):
            moveOptions.append([eachSpace[0]+1,eachSpace[1]-1])
        elif (insideBoard(eachSpace[0]-1,eachSpace[1]+1)):
            moveOptions.append([eachSpace[0]-1,eachSpace[1]+1])
    return moveOptions

def chooseValidMove(board,pcolors,currentPlayer):
    takenSpaces=spaceTaken(board)
    aList=checkAround(board,takenSpaces)
    if len(aList)>2:
        B=random.randint(0,int(len(aList)-1))
        move=aList[B]
        return move[0],move[1]
    elif len(aList)!=0:
        move=aList[0]
        return move
    elif len(aList)==0:
        row,col=manualMove(pcolors,currentPlayer,board)
        return row,col
        

        
        
              
