#! /usr/bin/env python3

import cTurtle
import random
import os
import sys
import copy
import datetime
import time
import pickle
import json
import importlib
from checkers_helper import *

EMPTY=0
INCs=[-1,1]
VALID_RANGE= range(8)
DEBUG=False
VISIBLE=True

ITERS=1

#Set timeout for round
timeout = time.time() + options.time
print(timeout, options.time)
    
#Send results to manager
def report_results(resulttype, p1wins,p2wins):
    p1result = "Win"
    p2result = "Loss"
    if p2wins >= p1wins:
        if p2wins != p1wins:
            p1result = "Loss"
            p2result = "Win"
        else:
            p1result = "Tie"
            p2result = "Tie"
    manager.send(resulttype, [P1.name, p1result, str(p1wins)])
    manager.send(resulttype, [P2.name, p2result, str(p2wins)])

#Fake player using socket connection instead
class Player():
    def __init__(self, server):
        self.connection = Connection(server)
        self.name = self.connection.listen(1024).decode()

    def getMove(self, b,playerIndex,playerColors,playerSymbols,opponentSymbols,rowInc):
        sys.stderr.write(str(playerIndex))
        self.connection.send(pickle.dumps((b,playerIndex,playerColors,playerSymbols,opponentSymbols,rowInc)))
        return pickle.loads(self.connection.listen(4096))

#Create players
P1 = Player(playerServer)
P2 = Player(playerServer)

def drawSquareWithFill(t,lengthOfSide,color):
    t.begin_fill()
    t.color(color)
    for x in range(4):
        t.forward(lengthOfSide)
        t.left(90)
    t.end_fill()
    
def drawRow(turtle,lengthOfSide,color,boardColorList,rowsAndCols):
    for reps in range(rowsAndCols):        
        drawSquareWithFill(turtle,lengthOfSide,color)
        turtle.forward(lengthOfSide)
        if color==boardColorList[0]:
            color=boardColorList[1]
        else:
            color=boardColorList[0]

def drawPolygon(t,sideLength,numSides):
    angle=360/numSides
    for reps in range(numSides):
        t.forward(sideLength)
        t.left(angle)
    
def drawCircle(t,radius):
    circumference=2 * 3.1415 * radius
    sideLength=circumference/360
    drawPolygon(t,sideLength,360)

def drawChecker(t,color,toRow,toCol,length,board,isKing):
    reduce=.05
    length=(1-reduce)*length
    t.up()
    t.color("black",color)
    t.goto((toCol+length/2)+reduce/2,toRow+reduce/2)
    t.down()
    t.begin_fill()
    ps=t.pensize()
    t.pensize(2)
    drawCircle(t,length/2)
    t.end_fill()
    t.color("black")
    t.up()
    t.goto((toCol+length/2)+reduce/2,(toRow+length/6)+reduce/2)
    t.down()
    drawCircle(t,length/3)
    t.up()
    t.goto((toCol+length/2)+reduce/2,(toRow+length/3)+reduce/2)
    t.down()
    if isKing:
        t.color("yellow")
    drawCircle(t,length/6)
    t.pensize(ps)
    t.color("black")

def labelBoard(t,upperLeftBoardX,upperLeftBoardY,length):
    t.up()
    t.goto(upperLeftBoardX+length/2,upperLeftBoardY)
    for i in range(8):
        t.write(i,font=("Arial",12,"bold"))
        t.forward(length)
    t.goto(upperLeftBoardX-length/2,upperLeftBoardY)
    for i in range(8):
        t.goto(upperLeftBoardX-length/2,upperLeftBoardY+length/1.5 + i)
        t.write((chr(ord("A")+i)),font=("Arial",12,"bold"))

def moveChecker(t,fromTo,playerColor,length,boardColorList,board,playerTokens,opponentTokens,playerIndex):
    if playerIndex==0:
        kingRow=7
    else:
        kingRow=0
    while len(fromTo)>=5:
        fromRow=ord(fromTo[0])-65
        fromCol=int(fromTo[1])
        toRow=ord(fromTo[3])-65
        toCol=int(fromTo[4])
        if toRow==kingRow or board[fromRow][fromCol] in ["R","B"]:
            isKing=True
        else:
            isKing=False
        #whether move or jump, remove from current and draw in new
        t.up()
        t.goto(fromCol,fromRow)
        t.down()
        drawSquareWithFill(t,length,boardColorList[0])
        if isKing:
            board[toRow][toCol]=board[fromRow][fromCol].upper()
        else:
            board[toRow][toCol]=board[fromRow][fromCol]
        board[fromRow][fromCol]=0
        t.up()
        t.goto(toCol,toRow)
        t.down()
        drawChecker(t,playerColor,toRow,toCol,length,board,isKing)
        if abs(fromRow-toRow)==2: #if a jump, also blank intervening cell
            t.up()
            t.goto((fromCol+toCol)//2,(fromRow+toRow)//2)
            t.down()
            drawSquareWithFill(t,length,boardColorList[0])
            board[(fromRow+toRow)//2][(fromCol+toCol)//2]=0
        fromTo=fromTo[3:]

       
def writeGameState(cBoard,playerIndex):
    fileName=input("Enter name to save game (just name, e.g. Test1) => ")
    if fileName!="":
        outFile=open(fileName+".chkrs","w")
        if playerIndex==0:
            playerIndex=1
        else:
            playerIndex=0
        outFile.write(str(playerIndex)+"\n")
        for row in cBoard:
            for item in row:
                outFile.write(str(item))
            outFile.write("\n")
        outFile.close()
    else:
        print("Game not saved")
    
def fillBoardWithCheckers(t,lengthOfSide,playerColors,board,autoGames):
    fileIndex=""
    if not autoGames:
        lstOfGames = []
        for entry in os.scandir('.'):
            if entry.is_file() and entry.name.endswith(".chkrs"):
                lstOfGames.append(entry.name)
        for i in range(len(lstOfGames)):
            print(i, lstOfGames[i])
        fileIndex=input("Enter an index for the file to load, or just hit ENTER to start a new game => ")
    if fileIndex=="":
        fileName=""
    else:
        fileName=lstOfGames[int(fileIndex)]
    if fileName=="":
        for i in range(8):
            row=["*"]*8
            board.append(row)
        board[3]=["*",0,"*",0,"*",0,"*",0]
        board[4]=[0,"*",0,"*",0,"*",0,"*"]
        offset=0
        for row in range(3):
            for col in range(0,8,2):
                drawChecker(t,playerColors[0],row,col+offset,lengthOfSide,board,False)
                board[row][col+offset]="r"
            if offset==0:
                offset=1
            else:
                offset=0
        offset=1
        for row in range(5,8):
            for col in range(0,8,2):
                drawChecker(t,playerColors[1],row,col+offset,lengthOfSide,board,False)
                board[row][col+offset]="b"
            if offset==0:
                offset=1
            else:
                offset=0
        playerIndex=random.randint(0,1)
        return playerIndex
    else:
        inFile=open(fileName,"r")
        player=inFile.readline()
        for row in inFile:
            newRow=[]
            for item in row:
                if item !="\n":
                    if item=="0":
                        newRow.append(int(item))
                    else:
                        newRow.append(item)
            board.append(newRow)
        inFile.close()
        for row in range(8):
            for col in range(8):
                if board[row][col]!="*" and board[row][col]!=0:
                    if board[row][col] in ["r","R"]:
                        playerIndex=0
                    else:
                        playerIndex=1
                    king=False
                    if board[row][col] in ["R","B"]:
                        king=True
                    drawChecker(t,playerColors[playerIndex],row,col,lengthOfSide,board,king)
        return int(player[:-1])
    
def showLogicalBoard(board):
    for row in board:
        for col in row:
            print(col,end="")
        print()
    
def drawBoard(t,upperLeftBoardX,upperLeftBoardY,rowsAndCols,lengthOfSide,boardColorList):
    x=upperLeftBoardX
    y=upperLeftBoardY
    t.goto(x,y)
    color=boardColorList[0]
    for i in range(rowsAndCols):
        drawRow(t,lengthOfSide,color,boardColorList,rowsAndCols)
        y=y+lengthOfSide
        t.up()
        t.goto(x,y)
        t.down()
        if color==boardColorList[0]:
            color=boardColorList[1]
        else:
            color=boardColorList[0]
    
def swapPlayer(playerIndex):
    if playerIndex==0:
        playerIndex=1
        rowInc=-1
        playerSymbols=["b","B"]
        opponentSymbols=["r","R"]
    else:
        playerIndex=0
        rowInc=1
        playerSymbols=["r","R"]
        opponentSymbols=["b","B"]
    return playerIndex,playerSymbols,opponentSymbols,rowInc
       
def listValidMoves(cBoard,player,playerTokens,opponentTokens,rowInc):
    validMoves=[]
    for row in range(8):
        for col in range(8):
            if cBoard[row][col] in playerTokens: #it is the specified player's checker
                if cBoard[row][col] not in ["R","B"]: #not a king checker
                    for colInc in INCs:
                        toRow=row+rowInc
                        toCol=col+colInc
                        if toRow in VALID_RANGE and toCol in VALID_RANGE and cBoard[toRow][toCol]==EMPTY:
                            validMoves.append(chr(row+65)+str(col)+":"+chr(toRow+65)+str(toCol))
                else: #is a king checker
                    for rInc in INCs:
                        for colInc in INCs:
                            toRow=row+rInc
                            toCol=col+colInc
                            if toRow in VALID_RANGE and toCol in VALID_RANGE and cBoard[toRow][toCol]==EMPTY:
                                validMoves.append(chr(row+65)+str(col)+":"+chr(toRow+65)+str(toCol))
    return validMoves

def listValidJumps(cBoard,player,playerTokens,opponentTokens,rowInc):
    validJumps=[]
    for row in range(8):
        for col in range(8):
            if cBoard[row][col] in playerTokens: #it is the specified player's checker
                if cBoard[row][col] not in ["R","B"]: #not a king checker
                    for colInc in INCs:
                        toRow=row+(rowInc*2)
                        toCol=col+(colInc*2)
                        jumpRow=row+rowInc
                        jumpCol=col+colInc
                        if toRow in VALID_RANGE and toCol in VALID_RANGE and cBoard[toRow][toCol]==EMPTY and cBoard[jumpRow][jumpCol]in opponentTokens:
                            validJumps.append(chr(row+65)+str(col)+":"+chr(toRow+65)+str(toCol))
                else: #is a king checker
                    for rInc in INCs:
                        for colInc in INCs:
                            toRow=row+(rInc*2)
                            toCol=col+(colInc*2)
                            jumpRow=row+rInc
                            jumpCol=col+colInc
                            if toRow in VALID_RANGE and toCol in VALID_RANGE and cBoard[toRow][toCol]==EMPTY and cBoard[jumpRow][jumpCol]in opponentTokens:
                                validJumps.append(chr(row+65)+str(col)+":"+chr(toRow+65)+str(toCol))
    return validJumps

def isWinner(board,playerSymbols,opponentSymbols,playerIndex,rowInc,playerColors,numMoves):
    validMoves=listValidMoves(board,playerIndex,playerSymbols,opponentSymbols,rowInc)
    validJumps=listValidJumps(board,playerIndex,playerSymbols,opponentSymbols,rowInc)
    if len(validMoves)==0 and len(validJumps)==0:
        if playerIndex==1:
            winner=0
        else:
            winner=1
        #print(playerColors[winner] + " is the winner!")
        return True, playerColors[winner]
    if numMoves > 200:
        scoresList=rateBoard(board)
        if scoresList[0]>scoresList[1]:
            winner="red"
        elif scoresList[0]<scoresList[1]:
            winner="gray"
        else:
            winner="TIE"
        return True,winner
    return False, None

def expandJumps(cBoard,player,oldJumps,playerTokens,opponentTokens,rowInc):
    newJumps=[]
    for oldJump in oldJumps:
        row=ord(oldJump[-2])-65
        col=int(oldJump[-1])
        newJumps.append(oldJump)
        startRow=ord(oldJump[0])-65
        startCol=int(oldJump[1])
        if cBoard[startRow][startCol] not in ["R","B"]: #not a king
            for colInc in INCs:
                jumprow=row+rowInc
                jumpcol=col+colInc
                torow=row+2*rowInc
                tocol=col+2*colInc
                if jumprow in VALID_RANGE and jumpcol in VALID_RANGE and torow in VALID_RANGE and tocol in VALID_RANGE \
                and cBoard[jumprow][jumpcol] in opponentTokens and cBoard[torow][tocol]==EMPTY:
                    newJumps.append(oldJump+":"+chr(torow+65)+str(tocol))
                    if oldJump in newJumps:
                        newJumps.remove(oldJump)
        else: #is a king
            for colInc in INCs:
                for newRowInc in INCs:
                    jumprow=row+newRowInc
                    jumpcol=col+colInc
                    torow=row+2*newRowInc
                    tocol=col+2*colInc
                    if jumprow in VALID_RANGE and jumpcol in VALID_RANGE and torow in VALID_RANGE and tocol in VALID_RANGE \
                    and cBoard[jumprow][jumpcol] in opponentTokens and (cBoard[torow][tocol]==EMPTY or oldJump[0:2]==chr(torow+65)+str(tocol)) \
                    and ((oldJump[-2:]+":"+chr(torow+65)+str(tocol)) not in oldJump) and ((chr(torow+65)+str(tocol)+':'+oldJump[-2:] not in oldJump)) and (chr(torow+65)+str(tocol)!=oldJump[-5:-3]):
                        newJumps.append(oldJump+":"+chr(torow+65)+str(tocol))
                        if oldJump in newJumps:
                            newJumps.remove(oldJump)
    return newJumps          

def labelGameStats(t,size,PlayerB,PlayerR,bWins,rWins,total):
    t.tracer(False)
    t.up()
    t.goto((3.5*size)+5,(1.3*size))
    #t.goto((4*size)+2,(2*size))
    t.down()
    t.pencolor("red")
    t.write("RED",font=("Arial",12,"bold"))
    t.up()
    t.goto((3.5*size)+5,(1*size))
    #t.goto((4*size)+1,(2*size))
    t.down()
    t.write(PlayerR +  "  " + str(rWins) + "/" + str(total),font=("Arial",12,"bold"))
    t.up()
    t.goto((3.5*size)+5,(7.3*size))
    t.down()
    t.pencolor('#000000')
    t.write("BLACK",font=("Arial",12,"bold"))
    t.up()
    t.goto((3.5*size)+5,(7*size))
    t.down()
    t.write(PlayerB + "  " + str(bWins) + "/" + str(total),font=("Arial",12,"bold"))
    t.tracer(True)




def main(PlayerB,PlayerR,bWins,rWins,totalPlayed,bob,board,upperLeftBoardX,upperLeftBoardY,lengthOfSide,rowsAndCols,boardColorList,delayMoves,moveWaitLimit,autoGames):
    #board=[]
    #bob=cTurtle.Turtle()
    #bob.setWorldCoordinates(-1.0,9,11,-.5)
    #bob.ht()
    bob.tracer(False)
    drawBoard(bob,upperLeftBoardX,upperLeftBoardY,rowsAndCols,lengthOfSide,boardColorList)
    labelBoard(bob,upperLeftBoardX,upperLeftBoardY,lengthOfSide)
    bob.tracer(True)
    playerColors=["gray","red"]
    bob.tracer(False)
    playerIndex=fillBoardWithCheckers(bob,lengthOfSide,playerColors,board,autoGames)
    bob.tracer(True)
    labelGameStats(bob,lengthOfSide,PlayerB,PlayerR,bWins,rWins,totalPlayed)
    if DEBUG:showLogicalBoard(board)
    
    playerIndex,playerSymbols,opponentSymbols,rowInc=swapPlayer(playerIndex)
    numMoves=0
    while not isWinner(board,playerSymbols,opponentSymbols,playerIndex,rowInc,playerColors,numMoves)[0]:
        validMoves=listValidMoves(board,playerIndex,playerSymbols,opponentSymbols,rowInc)
        validJumps=listValidJumps(board,playerIndex,playerSymbols,opponentSymbols,rowInc)
        oldJumps=validJumps[:]
        newJumps=expandJumps(board,playerIndex,oldJumps,playerSymbols,opponentSymbols,rowInc)
        while newJumps != oldJumps:
            oldJumps=newJumps[:]
            newJumps=expandJumps(board,playerIndex,oldJumps,playerSymbols,opponentSymbols,rowInc)
        validJumps=newJumps[:]
        if DEBUG:print("MOVES:",validMoves)
        if DEBUG:print("JUMPS:",validJumps)
        if DEBUG:input("PRESS ENTER TO CONTINUE")

        move=""
        forfeitWinner=False
        while not ((len(validJumps)>0 and move in validJumps) or (len(validJumps)==0 and move in validMoves) or (move=="exit")):
            b=copy.deepcopy(board)
            strt=datetime.datetime.now()
            if DEBUG:print(strt)

            if playerIndex==0:
                move=P1.getMove(b,playerIndex,playerColors,playerSymbols,opponentSymbols,rowInc)
            else:
                move=P2.getMove(b,playerIndex,playerColors,playerSymbols,opponentSymbols,rowInc)

            if len(validJumps)>0 and move not in validJumps:
                print("Game over due to",playerColors[playerIndex],"not taking an available jump!", )
                return "forfeit "+playerColors[playerIndex]
            if len(validJumps)==0 and move not in validMoves:
                print("Game over due to",playerColors[playerIndex],"not taking a valid move")
                return "forfeit "+playerColors[playerIndex]

            elapsed=datetime.datetime.now()-strt
            if DEBUG:print("%15.13f" % elapsed.total_seconds())
            print(time.time())
            if time.time() >= timeout-0.1:
                print("Game over due to delayed play by ", playerColors[playerIndex])
                return "forfeit "+playerColors[playerIndex]

        if move=="exit":
            writeGameState(board,playerIndex)
            print("Saving game")
            return

        bob.tracer(False)
        moveChecker(bob,move,playerColors[playerIndex],lengthOfSide,boardColorList,board,playerSymbols,opponentSymbols,playerIndex)
        bob.tracer(True)

        playerIndex,playerSymbols,opponentSymbols,rowInc=swapPlayer(playerIndex)
        if DEBUG:showLogicalBoard(board)
        numMoves+=1
    #Game is over due to win
    return isWinner(board,playerSymbols,opponentSymbols,playerIndex,rowInc,playerColors,numMoves)[1]


def rateBoard(cBoard):
    Rscore=0
    Bscore=0
    for row in cBoard:
        for col in row:
            if col in ["r","R"]:
                if col=="r":
                    Rscore += 1
                else:
                    Rscore+=2
            elif col in ["b","B"]:
                if col=="b":
                    Bscore += 1
                else:
                    Bscore+=2
    return ([Rscore,Bscore])

def alarm_response(signum, frame):
    global rWins
    global bWins
    global cBoard
    global manager
    
    if cBoard != []:
        roundScore = rateBoard(cBoard)
        redScore = roundScore[0]
        blackScore=roundScore[1]
        if redScore > blackScore:
            rWins += 1
        if blackScore > redScore:
            bWins += 1

    report_results("roundresult", bWins,rWins)
    manager.send("match", "end")
    report_results("matchresult", bWins, rWins)
    del(manager)
    os.exit(0)

rWins=0
bWins=0
cBoard=[]
def tourney(PlayerB,PlayerR):
    global rWins
    global bWins
    global cBoard
    
    i=1
    ITERS=1
    manager.send("match", "start")
    while i < ITERS+1:
        cBoard=[]
        manager.send("round", ["start", json.dumps({P1.name: PlayerB, P2.name: PlayerR})])
        print("Game:",str(i)+"/"+str(ITERS))
        bob=cTurtle.Turtle()
        bob.setWorldCoordinates(-1.0,9,11,-.5)
        bob.ht()
        bob.winsize(900,700)
        bob.speed(0)
        print("gray=",PlayerB,"red=",PlayerR)
        result=main(PlayerB,PlayerR,bWins,rWins,i-1,bob,board=cBoard,upperLeftBoardX=0,upperLeftBoardY=0,lengthOfSide=1,rowsAndCols=8,boardColorList=["black","red"],delayMoves=0,moveWaitLimit=15,autoGames=True)
        manager.send("round", "end")
        bob.bye()
        if result=="gray" or result=="forfeit red":
            print("Black wins!")
            bWins+=1
        elif result=="red" or result=="forfeit gray":
            print("Red wins!")
            rWins+=1
        else: #result=="TIE":
            print("Tie")
            i-=1
        i+=1
        report_results("roundresult", bWins,rWins)
    manager.send("match", "end")
    report_results("matchresult", bWins, rWins)
    return bWins,rWins

set_alarm_response(alarm_response)
tourney("Player 1","Player 2")
stop_alarm()

