#! /usr/bin/env python3

#Pegity Board
import cTurtle
import random
import P1
import P2

BOARD_SIZE = 15
BOARD_COLOR = "LightSteelBlue"

def drawPolygon(t,Len,numSides):
    turnAngle=360/numSides
    for i in range(numSides):
        t.forward(Len)
        t.right(turnAngle)

def drawCircleCentered(t,radius):
    pos=t.position()
    t.up()
    t.forward(radius)
    t.down()
    t.right(90)
    circumference=2*3.14159 * radius
    Len=circumference/360
    drawPolygon(t,Len,360)
    t.up()
    t.setpos(pos)
    t.down()

def drawSquare(t,size):
    for i in range(4):
        t.forward(size)
        t.lt(90)

def drawRow(t,size):
    t.up()
    for i in range(BOARD_SIZE):
        t.dot(7)
        t.fd(1)

def drawHoles(t,size):
    t.up()
    for i in range(BOARD_SIZE):
        t.goto(0,i)
        drawRow(t,BOARD_SIZE)

def drawLines(t,BOARD_SIZE):
    t.up()
    for i in range(BOARD_SIZE - 1):
        t.goto(-0.75,i + 0.5)
        t.down()
        t.fd(BOARD_SIZE + 0.5)
        t.up()
    t.lt(90)
    for j in range(BOARD_SIZE - 1):
        t.goto(j + 0.5, -0.75)
        t.down()
        t.forward(BOARD_SIZE + 0.5)
        t.up()
    t.rt(90)

def labelBoard(t,size):
    t.up()
    t.color("black")
    t.goto(0,-.8)
    for c in range(0,BOARD_SIZE,1):
        t.write(c,False,align="center",font=("Arial",12,"bold"))
        t.fd(1)
    s = .3
    for r in range(0,BOARD_SIZE,1):
        t.goto(-1.5,s)
        t.write(chr(r+65),False,align="center",font=("Arial",12,"bold"))
        s += 1

def drawBoard(t,size,color):
    pSize = t.pensize()
    t.setWorldCoordinates(-5,BOARD_SIZE+2,BOARD_SIZE+6,-2.5)
    t.ht()
    t.tracer(False)
    t.up()
    t.color(color)
    t.goto(-0.75,-0.75)
    t.down()
    t.pensize(5)
    t.begin_fill()
    drawSquare(t,size+0.5)
    t.end_fill()
    labelBoard(t,size)
    t.up()
    t.color("Navy")
    drawHoles(t,size)
    t.color("SlateGray")
    t.pensize(2)
    drawLines(t,size)
    t.color("black")
    t.goto(-0.75,-0.75)
    t.pensize(5)
    t.down()
    drawSquare(t,size+0.5)
    t.up()
    t.tracer(True)
    t.showturtle()
    t.pensize(1)

def getPlayerColor(player,colorList):
    for i in range(len(colorList)):
        print(i+1,"- "+colorList[i])
    answer=int(input("Please enter a number for the color for player "+str(player)+" => "))
    while answer<1 or answer>len(colorList):
        answer=int(input("Please enter a number for the color for player "+str(player)+" => "))
    color=colorList.pop(answer-1)
    return color

def placePeg(t,row,column,pcolors,board,player):
    board[row][column]=player
    t.tracer(False)
    t.up()
    t.goto(column,row)
    t.color("black",pcolors[player])
    t.begin_fill()
    drawCircleCentered(t,.5)
    t.end_fill()
    t.tracer(True)

def showInternalBoard(board):
    for row in board:
        for col in row:
            print(col,end="")
        print()

def win(board):
    for row in range(15):
        for col in range(15):
            if board[row][col]!=0:
                #horizontal
                if col<11:
                    count=1
                    for offset in range(1,5,1):
                        if board[row][col]==board[row][col+offset]:
                            count+=1
                    if count==5:
                        print("WINNER IS PLAYER",board[row][col])
                        return [True, board[row][col]]
                #vertical
                if row<11:
                    count=1
                    for offset in range(1,5,1):
                        if board[row][col]==board[row+offset][col]:
                            count+=1
                    if count==5:
                        print("WINNER IS PLAYER",board[row][col])
                        return [True, board[row][col]]
                #CHECK DIAGONALS
                #left to right
                if row<11 and col<11:
                    count=1
                    for offset in range(1,5,1):
                        if board[row][col]==board[row+offset][col+offset]:
                            count+=1
                    if count==5:
                        print("WINNER IS PLAYER",board[row][col])
                        return [True, board[row][col]]
                #right to left
                if row<11 and col>3:
                    count=1
                    for offset in range(1,5,1):
                        if board[row][col]==board[row+offset][col-offset]:
                            count+=1
                    if count==5:
                        print("WINNER IS PLAYER",board[row][col])
                        return [True, board[row][col]]
    return [False,0]


def readFile(fName,board):
    inFile=open(fName,"r")
    for index in range(15):
        line=inFile.readline()
        row=[]
        for col in range(15):
            row.append(int(line[col]))
        board.append(row)
    line=inFile.readline() #Now read player and color information
    lnLst=line.split()
    p1Color=lnLst[0]
    p2Color=lnLst[1]
    currentPlayer=int(lnLst[2])
    if currentPlayer==1:
        pColor=p1Color
    else:
        pColor=p2Color
    inFile.close()
    return currentPlayer,p1Color,p2Color

def Peggity():
    #create the starting physical board
    phil = cTurtle.Turtle()
    drawBoard(phil,BOARD_SIZE,BOARD_COLOR)
    phil.up()
    phil.hideturtle()
    #create the starting logical board
    board=[]
    fName=input("Enter a file name (or just hit enter for a new game)=> ")
    if fName=="":
        for rows in range(15):
            row=[]
            for cols in range(15):
                row.append(0)
            board.append(row)
        #get player colors
        colorList=["blue","green","yellow","orange","black","white","purple"]
        P1Color=getPlayerColor(1,colorList)
        P2Color=getPlayerColor(2,colorList)
        pcolors=[0,P1Color,P2Color]
        #randomly pick starting player
        if random.randint(0,1)==0:
            currentPlayer=1
            #currentPlayerColor=P1Color
        else:
            currentPlayer=2
            #currentPlayerColor=P2Color
    else: #get game from file
        currentPlayer,P1Color,P2Color=readFile(fName,board)
        pcolors=[0,P1Color,P2Color]
        #Draw the board contents based on file contents
        for row in range(15):
            for col in range(15):
                if board[row][col]!=0:
                    placePeg(phil,row,col,pcolors,board,board[row][col])
    #Start the game
    pegCount=0
    while not win(board)[0]: #MAIN GAME LOGIC
        goodMoveSpecified=False
        while not goodMoveSpecified:
            if currentPlayer==1:
                row,col=P1.manualMove(pcolors,currentPlayer,board)
            else:
                row,col=P2.manualMove(pcolors,currentPlayer,board)
            if row>=0 and row<=14 and col>=0 and col<=14 and board[row][col]==0:
                goodMoveSpecified=True
            else:

                goodMoveSpecified=False
        #a good move has been entered or selected, so make it so!
        placePeg(phil,row,col,pcolors,board,currentPlayer)
        pegCount=pegCount+1
        phil.up()
        phil.goto(16,2)
        phil.circle(5)
        phil.write("Peg Count: " + str(pegCount))
        if currentPlayer==1: #now switch the current player
            currentPlayer=2
            #currentPlayerColor=P2Color
        else:
            currentPlayer=1
            #currentPlayerColor=P1Color


Peggity()