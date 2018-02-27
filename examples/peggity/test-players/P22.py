import random
def manualMove(pcolors,currentPlayer,board):
    diff=["manual","random","thinker","logical","decisive"]
    mode=diff[3]
    if mode=="manual":
        answer=input("Enter row and column for player "+pcolors[currentPlayer]+" (e.g. A0) => ")
        if answer=="quit" or answer=="QUIT": #save current game to file and quit
            fileName=input("Enter the name of a file to save this game (just hit enter to exit) => ")
            if fileName != "":
                outFile = open(fileName,"w")
                for r in range(15):
                    for c in range(15):
                        outFile.write(str(board[r][c]))
                    outFile.write("\n")
                outFile.write(pcolors[1] + " " + pcolors[2] + " " + str(currentPlayer))
                outFile.close()
            exit()
        else: #convert their input and see if good move
            if answer[0] in ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o']:
                row=ord(answer[0].upper())-65
            else:
                return -1,-1
            if answer[1:] in ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14']:
                col=int(answer[1:])
            else:
                return -1,-1
            if row>=0 and row<=14 and col>=0 and col<=14 and board[row][col]==0:
                return row, col
            else:
                return -1,-1
    if mode=="random":
        emptyCellsList=[]
        for row in range(15):
            for col in range(15):
                if board[row][col]==0:
                    emptyCellsList.append(chr(65+row)+str(col))
        move=emptyCellsList[random.randrange(0,len(emptyCellsList))]
        row=ord(move[0])-65
        col=int(move[1:])
        return row,col
    elif mode=="thinker":
        myCells=[]
        opCells=[]
        emptyCellsList=[]
        for row in range(15):
            for col in range(15):
                if board[row][col]==currentPlayer:
                    myCells.append(chr(65+row)+str(col))
                elif board[row][col]!=0:
                    opCells.append(chr(65+row)+str(col))
                else:
                    emptyCellsList.append(chr(65+row)+str(col))
        row,col=nextToPeg(myCells,opCells,emptyCellsList,board)
        return row,col
    elif mode=="logical":
        myCells=[]
        opCells=[]
        emptyCellsList=[]
        for row in range(15):
            for col in range(15):
                if board[row][col]==currentPlayer:
                    myCells.append(chr(65+row)+str(col))
                elif board[row][col]!=0:
                    opCells.append(chr(65+row)+str(col))
                else:
                    emptyCellsList.append(chr(65+row)+str(col))
        myWin=checkWinMove(myCells,board,currentPlayer,4)
        if myWin is not None:
            row,col=checkWinMove(myCells,board,currentPlayer,4)
            return row,col
        if currentPlayer==1:
            checkP=2
        else:
            checkP=1
        opWin=checkWinMove(opCells,board,checkP,4)
        if opWin is not None:
            row,col=checkWinMove(opCells,board,checkP,4)
            return row,col
        row,col=nextToPeg(myCells,opCells,emptyCellsList,board)
        return row,col
    elif mode=="decisive":
        myCells=[]
        opCells=[]
        emptyCellsList=[]
        for row in range(15):
            for col in range(15):
                if board[row][col]==currentPlayer:
                    myCells.append(chr(65+row)+str(col))
                elif board[row][col]!=0:
                    opCells.append(chr(65+row)+str(col))
                else:
                    emptyCellsList.append(chr(65+row)+str(col))
        myWin=checkWinMove(myCells,board,currentPlayer,4)
        if myWin is not None:
            row,col=checkWinMove(myCells,board,currentPlayer,4)
            return row,col
        if currentPlayer==1:
            checkP=2
        else:
            checkP=1
        opWin=checkWinMove(opCells,board,checkP,4)
        if opWin is not None:
            row,col=checkWinMove(opCells,board,checkP,4)
            return row,col
        myScore=checkWinMove(myCells,board,currentPlayer,3)
        if myScore is not None:
            row,col=checkWinMove(myCells,board,currentPlayer,3)
            return row,col
        opScore=checkWinMove(opCells,board,checkP,3)
        if opScore is not None:
            row,col=checkWinMove(opCells,board,checkP,3)
            return row,col
        row,col=nextToPeg(myCells,opCells,emptyCellsList,board)
        return row,col

def nextToPeg(myCells,opCells,emptyCellsList,board):
    if len(myCells) + len(opCells) > 0:
        valid=False
        while(valid==False):
            move=emptyCellsList[random.randrange(0,len(emptyCellsList))]
            row=ord(move[0])-65
            col=int(move[1:])
            if row==14 and col!=14:
                if board[row-1][col+1]!=0 or board[row][col+1]!=0 or board[row-1][col]!=0 or board[row-1][col-1]!=0 or board[row][col-1]!=0:
                    valid=True
            elif row!=14 and col==14:
                if board[row-1][col]!=0 or board[row+1][col]!=0 or board[row-1][col-1]!=0 or board[row][col-1]!=0 or board[row+1][col-1]!=0:
                    valid=True
            elif row==14 and col==14:
                if board[row-1][col]!=0 or board[row-1][col-1]!=0 or board[row][col-1]!=0:
                    valid=True
            elif row==0 and col>0:
                if board[row][col+1]!=0 or board[row+1][col+1]!=0 or board[row+1][col]!=0 or board[row][col-1]!=0 or board[row+1][col-1]!=0:
                    valid=True
            elif row>0 and col==0:
                if board[row-1][col+1]!=0 or board[row][col+1]!=0 or board[row+1][col+1]!=0 or board[row-1][col]!=0 or board[row+1][col]!=0:
                    valid=True
            elif row==0 and col==0:
                if board[row][col+1]!=0 or board[row+1][col+1]!=0 or board[row+1][col]!=0:
                    valid=True
            else:
                if board[row-1][col+1]!=0 or board[row][col+1]!=0 or board[row+1][col+1]!=0 or board[row-1][col]!=0 or board[row+1][col]!=0 or board[row-1][col-1]!=0 or board[row][col-1]!=0 or board[row+1][col-1]!=0:
                    valid=True
    else:
        row=random.randrange(0,14)
        col=random.randrange(0,14)
    return row,col

def checkWinMove(cellList,board,checkP,pegs):
    for cell in cellList:
            row=ord(cell[0])-65
            col=int(cell[1:])
            horz=[]
            vert=[]
            diag1=[]
            diag2=[]
            for i in range(-4,5):
                if row-i>=0 and row-i<=14 and col-i>=0 and col-i<=14:
                    diag2.append([row-i,col-i,board[row-i][col-i]])
                if row+i>=0 and row+i<=14 and col-i>=0 and col-i<=14:
                    diag1.append([row+i,col-i,board[row+i][col-i]])
                if row+i>=0 and row+i<=14:
                    horz.append([row+i,col,board[row+i][col]])
                if col+i>=0 and col+i<=14:
                    vert.append([row,col+i,board[row][col+i]])
            lines=[horz,vert,diag1,diag2]
            for line in lines:
                score=0
                emptyCell=False
                for c in line:
                    if c[2]==checkP:
                        score+=1
                    elif c[2]==0 and emptyCell==False:
                        nRow=c[0]
                        nCol=c[1]
                        emptyCell=True
                    elif c[2]==0 and emptyCell==True:
                        nRow=c[0]
                        nCol=c[1]
                        score=0
                        emptyCell=True
                    elif c[2]!=checkP:
                        emptyCell=False
                        score=0
                    if score==pegs and emptyCell==True:
                        return nRow,nCol
