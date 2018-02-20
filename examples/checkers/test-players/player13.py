#! /usr/bin/env python3

import time
import random
import copy

EMPTY=0
INCs=[-1,1]
VALID_RANGE=range(8)
DEBUG=False
VISIBLE=True

def listValidMoves(CB,player,playerTokens,opponentTokens,rowInc):
    validMoves=[]
    for row in range(8):
        for col in range(8):
            if CB[row][col] in playerTokens: #it is the specified player's checker
                if CB[row][col] not in ["R","B"]: #not a king checker
                    for colInc in INCs:
                        toRow=row+rowInc
                        toCol=col+colInc
                        if toRow in VALID_RANGE and toCol in VALID_RANGE and CB[toRow][toCol]==EMPTY:
                            validMoves.append(chr(row+65)+str(col)+":"+chr(toRow+65)+str(toCol))
                else: #is a king checker
                    for rInc in INCs:
                        for colInc in INCs:
                            toRow=row+rInc
                            toCol=col+colInc
                            if toRow in VALID_RANGE and toCol in VALID_RANGE and CB[toRow][toCol]==EMPTY:
                                validMoves.append(chr(row+65)+str(col)+":"+chr(toRow+65)+str(toCol))
    return validMoves

def listValidJumps(CB,player,playerTokens,opponentTokens,rowInc):
    validJumps=[]
    for row in range(8):
        for col in range(8):
            if CB[row][col] in playerTokens: #it is the specified player's checker
                if CB[row][col] not in ["R","B"]: #not a king checker
                    for colInc in INCs:
                        toRow=row+(rowInc*2)
                        toCol=col+(colInc*2)
                        jumpRow=row+rowInc
                        jumpCol=col+colInc
                        if toRow in VALID_RANGE and toCol in VALID_RANGE and CB[toRow][toCol]==EMPTY and CB[jumpRow][jumpCol] in opponentTokens:
                            validJumps.append(chr(row+65)+str(col)+":"+chr(toRow+65)+str(toCol))
                else: #is a king checker
                    for rInc in INCs:
                        for colInc in INCs:
                            toRow=row+(rInc*2)
                            toCol=col+(colInc*2)
                            jumpRow=row+rInc
                            jumpCol=col+colInc
                            if toRow in VALID_RANGE and toCol in VALID_RANGE and CB[toRow][toCol]==EMPTY and CB[jumpRow][jumpCol] in opponentTokens:
                                validJumps.append(chr(row+65)+str(col)+":"+chr(toRow+65)+str(toCol))
    return validJumps

def getManualMove(validMoves,validJumps,playerIndex,playerColors):
    move=input("Enter a move " + playerColors[playerIndex] + " => ")
    if move=="exit":
        return move
    if len(validJumps)>0:
        while move not in validJumps:
            print("You must take the jump!")
            print(validJumps)
            move=input("Enter a jump " + playerColors[playerIndex] + " => ")
        return move
    while move not in validMoves:
        print(move, "is invalid!  Please try again from the following:")
        print(validMoves)
        move=input("Enter a move " + playerColors[playerIndex] + " => ")
    return move

def expandJumps(CB,player,oldJumps,playerTokens,opponentTokens,rowInc):
    newJumps=[]
    for oldJump in oldJumps:
        row=ord(oldJump[-2])-65
        col=int(oldJump[-1])
        newJumps.append(oldJump)
        startRow=ord(oldJump[0])-65
        startCol=int(oldJump[1])
        if CB[startRow][startCol] not in ["R","B"]: #not a king
            for colInc in INCs:
                jumprow=row+rowInc
                jumpcol=col+colInc
                torow=row+2*rowInc
                tocol=col+2*colInc
                if jumprow in VALID_RANGE and jumpcol in VALID_RANGE and torow in VALID_RANGE and tocol in VALID_RANGE \
                and CB[jumprow][jumpcol] in opponentTokens and CB[torow][tocol]==EMPTY:
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
                    and CB[jumprow][jumpcol] in opponentTokens and (CB[torow][tocol]==EMPTY or oldJump[0:2]==chr(torow+65)+str(tocol)) \
                    and ((oldJump[-2:]+":"+chr(torow+65)+str(tocol)) not in oldJump) and ((chr(torow+65)+str(tocol)+':'+oldJump[-2:] not in oldJump)) and (chr(torow+65)+str(tocol)!=oldJump[-5:-3]):
                        newJumps.append(oldJump+":"+chr(torow+65)+str(tocol))
                        if oldJump in newJumps:
                            newJumps.remove(oldJump)
    return newJumps

#*********************************************************************************
#************************* Heuristics Helpers *************************************
#*********************************************************************************
def between(jmp,location):
    fromRow=ord(jmp[0:1])-65
    fromCol=int(jmp[1:2])
    betweenRow=ord(location[0])-65
    betweenCol=int(location[1])
    toRow=ord(jmp[-2])-65
    toCol=int(jmp[-1])
    if (fromRow + toRow)//2 == betweenRow and (fromCol+toCol)//2 == betweenCol:
        if DEBUG:print(location, "is between jump",jmp)
        return True
    else:
        if DEBUG:print(location, "is NOT between jump",jmp)
        return False   

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

#*********************************************************************************
#***************************** Heuristics ****************************************
#*********************************************************************************
def jumpsIntoSafeSpot(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    enemyIndex,enemySymbols,mySymbols,enemyRowInc=swapPlayer(playerIndex)
    lst=copy.deepcopy(validJumps)
    for jmp in validJumps:
        #As though we were going to make the move . . .
        fromRow=ord(jmp[0:1])-65
        fromCol=int(jmp[1:2])
        toRow=ord(jmp[-2])-65
        toCol=int(jmp[-1])
        betweenRow=(fromRow + toRow)//2
        betweenCol=(fromCol + toCol)//2
        testBoard=copy.deepcopy(board)
        testBoard[toRow][toCol]=testBoard[fromRow][fromCol]
        testBoard[fromRow][fromCol]=0
        testBoard[betweenRow][betweenCol]=0
        enemyJumps=listValidJumps(testBoard,enemyIndex,enemySymbols,mySymbols,enemyRowInc)
        for jmpe in enemyJumps:
            if between(jmpe,jmp[-2:]):
                if jmp in lst:
                    lst.remove(jmp)
    return lst    

def kingRow(board,validPlay,playerTokens,rowInc):
    board=copy.deepcopy(board)
    kingRowList=[]
    if rowInc == 1:
        kingRow=7
    else:
        kingRow=0
    for play in validPlay:
        fromRow=ord(play[0:1])-65
        fromCol=int(play[1:2])
        if board[fromRow][fromCol] == playerTokens[0]: #Not a king checker
            if (ord(play[-2])-65) == kingRow:
                kingRowList.append(play)
    return kingRowList

def jumpsFromPossibleJump(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    enemyIndex,enemySymbols,mySymbols,enemyRowInc=swapPlayer(playerIndex)
    testBoard=copy.deepcopy(board)
    lst=[]
    enemyJumps=listValidJumps(testBoard,enemyIndex,enemySymbols,mySymbols,enemyRowInc)
    #Are any of my starting points the in between point for any of his jumps?
    for jmp in validJumps:
        for jmpe in enemyJumps:
            if between(jmpe,jmp[0:2]):
                lst.append(jmp)
    return lst

def jumpsIntoSideSquare(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    lst=[]
    for jmp in validJumps:
        if jmp[-1]in ['0','7']:
            lst.append(jmp)
    return lst

def movesIntoSafeSpot(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    enemyIndex,enemySymbols,mySymbols,enemyRowInc=swapPlayer(playerIndex)
    lst=copy.deepcopy(validMoves)
    for mv in validMoves:
        #As though we were going to make the move . . .
        fromRow=ord(mv[0:1])-65
        fromCol=int(mv[1:2])
        toRow=ord(mv[3:4])-65
        toCol=int(mv[4:5])
        testBoard=copy.deepcopy(board)
        testBoard[toRow][toCol]=testBoard[fromRow][fromCol]
        testBoard[fromRow][fromCol]=0
        enemyJumps=listValidJumps(testBoard,enemyIndex,enemySymbols,mySymbols,enemyRowInc)
        if DEBUG:print("ENEMY JUMPS for move",mv,enemyJumps)
        for jmp in enemyJumps:
            if between(jmp,mv[3:5]):
                if mv in lst:
                    lst.remove(mv)
    return lst

#*********************************************************************************
#*************************** New Heuristics **************************************
#*********************************************************************************

#Hueristic 1
def protectBackRow(movesIntoSafeSpotList,board,playerIndex,playerTokens,opponentTokens,rowInc):
    protectBackRowList=movesIntoSafeSpotList[:]
    if rowInc == 1:
        backRow=0
    else:
        backRow=7
    for mv in movesIntoSafeSpotList:
        fromRow=ord(mv[0:1])-65
        fromCol=int(mv[1:2])
        if board[fromRow][fromCol] == playerTokens[0]: #Not a king checker
            fromRow=ord(mv[0:1])-65
            if fromRow == backRow:
                protectBackRowList.remove(mv)
    return protectBackRowList

#Heuristic 2
def protectSecondRow(protectBackRowList,board,playerIndex,playerTokens,opponentTokens,rowInc):
    protectSecondRowList=protectBackRowList[:]
    if rowInc == 1:
        secondRow=1
    else:
        secondRow=6
    for mv in protectBackRowList:
        fromRow=ord(mv[0:1])-65
        fromCol=int(mv[1:2])
        if board[fromRow][fromCol] == playerTokens[0]: #Not a king checker
            fromRow=ord(mv[0:1])-65
            if fromRow == secondRow:
                protectSecondRowList.remove(mv)
    return protectSecondRowList

#Hueristic 3
def kingMoveUpBoard(movesIntoSafeSpotList,board,playerIndex,playerColors,playerTokens,opponentTokens,rowInc):
    board=copy.deepcopy(board)
    kingMoveList=[]
    for move in movesIntoSafeSpotList:
        fromRow=ord(move[0:1])-65
        fromCol=int(move[1:2])
        toRow=ord(move[3:4])-65
        toCol=int(move[4:5])
        if board[fromRow][fromCol] == playerTokens[1]: #is a king checker
            if (fromRow-toRow) == (rowInc):
                kingMoveList.append(move)
    return kingMoveList

#Hueristic 4
def multJump(jumpsIntoSafeSpotList,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc):
    multJumpList=[]
    for jump in validJumps:
        if len(jump) > 5 and jump in jumpsIntoSafeSpotList:
            multJumpList.append(jump)
    return multJumpList

#Hueristic 5
def preventJump(validMoves,board,playerIndex,playerColors,playerTokens,opponentTokens,rowInc):
    board=copy.deepcopy(board)
    preventJumpList=[]
    for move in validMoves:
        fromRow=ord(move[0:1])-65
        fromCol=int(move[1:2])
        toRow=ord(move[3:4])-65
        toCol=int(move[4:5])
        oppIndex,oppTokens,playerTokens,opprowInc=swapPlayer(playerIndex)
        oppValidJumpsPre=listValidJumps(board,oppIndex,oppTokens,playerTokens,opprowInc)
        board[toRow][toCol]=board[fromRow][fromCol]
        board[fromRow][fromCol]=0
        board[(fromRow+toRow)//2][(fromCol+toCol)//2]=0
        oppValidJumpsPost=listValidJumps(board,oppIndex,oppTokens,playerTokens,opprowInc)
        if len(oppValidJumpsPost) < len(oppValidJumpsPre) and oppValidJumpsPre != []:
            preventJumpList.append(move)
    return preventJumpList

def getMove(board,playerIndex,playerColors,playerTokens,opponentTokens,rowInc):
    validMoves=listValidMoves(board,playerIndex,playerTokens,opponentTokens,rowInc)
    validJumps=listValidJumps(board,playerIndex,playerTokens,opponentTokens,rowInc)
    oldJumps=validJumps[:]
    newJumps=expandJumps(board,playerIndex,oldJumps,playerTokens,opponentTokens,rowInc)
    while newJumps != oldJumps:
        oldJumps=newJumps[:]
        newJumps=expandJumps(board,playerIndex,oldJumps,playerTokens,opponentTokens,rowInc)
    validJumps=newJumps[:]
    if DEBUG:print("MOVES:",validMoves)
    if DEBUG:print("JUMPS:",validJumps)
    jumpsIntoSafeSpotList=jumpsIntoSafeSpot(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    jumpsIntoKingRowList=kingRow(board,validJumps,playerTokens,rowInc)
    jumpsFromPossibleJumpList=jumpsFromPossibleJump(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    jumpsIntoSideSquareList=jumpsIntoSideSquare(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    preventJumpList=preventJump(validJumps,board,playerIndex,playerColors,playerTokens,opponentTokens,rowInc)
    multJumpList=multJump(jumpsIntoSafeSpotList,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    movesIntoKingRowList=kingRow(board,validMoves,playerTokens,rowInc)
    movesIntoSafeSpotList=movesIntoSafeSpot(validMoves,validJumps,board,playerIndex,playerTokens,opponentTokens,rowInc)
    protectBackRowList=protectBackRow(movesIntoSafeSpotList,board,playerIndex,playerTokens,opponentTokens,rowInc)
    protectSecondRowList=protectSecondRow(protectBackRowList,board,playerIndex,playerTokens,opponentTokens,rowInc)
    kingMoveUpBoardList=kingMoveUpBoard(movesIntoSafeSpotList,board,playerIndex,playerColors,playerTokens,opponentTokens,rowInc)
    preventMoveList=preventJump(validMoves,board,playerIndex,playerColors,playerTokens,opponentTokens,rowInc)

    combinedJumps=jumpsIntoSafeSpotList+jumpsIntoKingRowList+jumpsFromPossibleJumpList+jumpsIntoSideSquareList+preventJumpList+multJumpList
    combinedMoves=movesIntoKingRowList+movesIntoSafeSpotList+protectBackRowList+protectSecondRowList+kingMoveUpBoardList+preventMoveList
    bestMoves=[]
    bestJumps=[]
    
    for move in combinedMoves:
        if combinedMoves.count(move) > 2 and move not in bestMoves:
            bestMoves.append(move)
    for jump in combinedJumps:
        if combinedJumps.count(jump) > 1 and jump not in bestJumps:
            bestJumps.append(jump)
            
    if DEBUG:
        print("jumpsIntoSafeSpotList",jumpsIntoSafeSpotList)
        print("jumpsIntoKingRowList",jumpsIntoKingRowList)
        print("jumpsFromPossibleJumpList",jumpsFromPossibleJumpList)
        print("jumpsIntoSideSquareList",jumpsIntoSideSquareList)
        print("movesIntoKingRowList",movesIntoKingRowList)
        print("movesIntoSafeSpotList",movesIntoSafeSpotList)
        print("protectBackRowList",protectBackRowList)
        print("protectSecondRowList",protectSecondRowList)
        print("kingMoveUpBoardList",kingMoveUpBoardList)
        print("multJumpList",multJumpList)
        print("combinedJumps",bestJumps)
        print("combinedMoves",bestMoves)
        print("preventJumpList",preventJumpList)
        print("preventMoveList",preventMoveList)

    if len(validJumps)==0:
        if movesIntoKingRowList != []:
            move = movesIntoKingRowList[random.randrange(0,len(movesIntoKingRowList))]
        elif kingMoveUpBoardList != []:
            move = kingMoveUpBoardList[random.randrange(0,len(kingMoveUpBoardList))]
        elif bestMoves != []:
            move = bestMoves[random.randrange(0,len(bestMoves))]
        elif preventMoveList != []:
            move = preventMoveList[random.randrange(0,len(preventMoveList))]
        elif protectBackRowList != []:
            move = protectBackRowList[random.randrange(0,len(protectBackRowList))]
        elif movesIntoSafeSpotList != []:
            move = movesIntoSafeSpotList[random.randrange(0,len(movesIntoSafeSpotList))]
            if DEBUG:print("MADE SAFE MOVE")
            if DEBUG:print(movesIntoSafeSpotList)
            time.sleep(0)
        else:
            move=validMoves[random.randrange(0,len(validMoves))]
    else:
        if jumpsIntoKingRowList !=[]:
            move=jumpsIntoKingRowList[random.randrange(0,len(jumpsIntoKingRowList))]
        elif multJumpList !=[]:
            move=multJumpList[random.randrange(0,len(multJumpList))]
        elif bestJumps != []:
            move = bestJumps[random.randrange(0,len(bestJumps))]
        elif preventJumpList != []:
            move = preventJumpList[random.randrange(0,len(preventJumpList))]
        elif jumpsFromPossibleJumpList !=[]:
            move=jumpsFromPossibleJumpList[random.randrange(0,len(jumpsFromPossibleJumpList))]
        elif jumpsIntoSideSquareList !=[]:
            move=jumpsIntoSideSquareList[random.randrange(0,len(jumpsIntoSideSquareList))]
        elif jumpsIntoSafeSpotList != []:
            move=jumpsIntoSafeSpotList[random.randrange(0,len(jumpsIntoSafeSpotList))]
        else:
            move=validJumps[random.randrange(0,len(validJumps))]
#    print("MOVE: ",move)
    return move


































##                               .....'',;;::cccllllllllllllcccc:::;;,,,''...'',,'..
##                            ..';cldkO00KXNNNNXXXKK000OOkkkkkxxxxxddoooddddddxxxxkkkkOO0XXKx:.
##                      .':ok0KXXXNXK0kxolc:;;,,,,,,,,,,,;;,,,''''''',,''..              .'lOXKd'
##                 .,lx00Oxl:,'............''''''...................    ...,;;'.             .oKXd.
##              .ckKKkc'...'',:::;,'.........'',;;::::;,'..........'',;;;,'.. .';;'.           'kNKc.
##           .:kXXk:.    ..       ..................          .............,:c:'...;:'.         .dNNx.
##          :0NKd,          .....''',,,,''..               ',...........',,,'',,::,...,,.        .dNNx.
##         .xXd.         .:;'..         ..,'             .;,.               ...,,'';;'. ...       .oNNo
##         .0K.         .;.              ;'              ';                      .'...'.           .oXX:
##        .oNO.         .                 ,.              .     ..',::ccc:;,..     ..                lXX:
##       .dNX:               ......       ;.                'cxOKK0OXWWWWWWWNX0kc.                    :KXd.
##     .l0N0;             ;d0KKKKKXK0ko:...              .l0X0xc,...lXWWWWWWWWKO0Kx'                   ,ONKo.
##   .lKNKl...'......'. .dXWN0kkk0NWWWWWN0o.            :KN0;.  .,cokXWWNNNNWNKkxONK: .,:c:.      .';;;;:lk0XXx;
##  :KN0l';ll:'.         .,:lodxxkO00KXNWWWX000k.       oXNx;:okKX0kdl:::;'',;coxkkd, ...'. ...'''.......',:lxKO:.
## oNNk,;c,'',.                      ...;xNNOc,.         ,d0X0xc,.     .dOd,           ..;dOKXK00000Ox:.   ..''dKO,
##'KW0,:,.,:..,oxkkkdl;'.                'KK'              ..           .dXX0o:'....,:oOXNN0d;.'. ..,lOKd.   .. ;KXl.
##;XNd,;  ;. l00kxoooxKXKx:..ld:         ;KK'                             .:dkO000000Okxl;.   c0;      :KK;   .  ;XXc
##'XXdc.  :. ..    '' 'kNNNKKKk,      .,dKNO.                                   ....       .'c0NO'      :X0.  ,.  xN0.
##.kNOc'  ,.      .00. ..''...      .l0X0d;.             'dOkxo;...                    .;okKXK0KNXx;.   .0X:  ,.  lNX'
## ,KKdl  .c,    .dNK,            .;xXWKc.                .;:coOXO,,'.......       .,lx0XXOo;...oNWNXKk:.'KX;  '   dNX.
##  :XXkc'....  .dNWXl        .';l0NXNKl.          ,lxkkkxo' .cK0.          ..;lx0XNX0xc.     ,0Nx'.','.kXo  .,  ,KNx.
##   cXXd,,;:, .oXWNNKo'    .'..  .'.'dKk;        .cooollox;.xXXl     ..,cdOKXXX00NXc.      'oKWK'     ;k:  .l. ,0Nk.
##    cXNx.  . ,KWX0NNNXOl'.           .o0Ooldk;            .:c;.':lxOKKK0xo:,.. ;XX:   .,lOXWWXd.      . .':,.lKXd.
##     lXNo    cXWWWXooNWNXKko;'..       .lk0x;       ...,:ldk0KXNNOo:,..       ,OWNOxO0KXXNWNO,        ....'l0Xk,
##     .dNK.   oNWWNo.cXK;;oOXNNXK0kxdolllllooooddxk00KKKK0kdoc:c0No        .'ckXWWWNXkc,;kNKl.          .,kXXk,
##      'KXc  .dNWWX;.xNk.  .kNO::lodxkOXWN0OkxdlcxNKl,..        oN0'..,:ox0XNWWNNWXo.  ,ONO'           .o0Xk;
##      .ONo    oNWWN0xXWK, .oNKc       .ONx.      ;X0.          .:XNKKNNWWWWNKkl;kNk. .cKXo.           .ON0;
##      .xNd   cNWWWWWWWWKOkKNXxl:,'...;0Xo'.....'lXK;...',:lxk0KNWWWWNNKOd:..   lXKclON0:            .xNk.
##      .dXd   ;XWWWWWWWWWWWWWWWWWWNNNNNWWNNNNNNNNNWWNNNNNNWWWWWNXKNNk;..        .dNWWXd.             cXO.
##      .xXo   .ONWNWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWNNK0ko:'..OXo          'l0NXx,              :KK,
##      .OXc    :XNk0NWXKNWWWWWWWWWWWWWWWWWWWWWNNNX00NNx:'..       lXKc.     'lONN0l.              .oXK:
##      .KX;    .dNKoON0;lXNkcld0NXo::cd0NNO:;,,'.. .0Xc            lXXo..'l0NNKd,.              .c0Nk,
##      :XK.     .xNX0NKc.cXXl  ;KXl    .dN0.       .0No            .xNXOKNXOo,.               .l0Xk;.
##     .dXk.      .lKWN0d::OWK;  lXXc    .OX:       .ONx.     . .,cdk0XNXOd;.   .'''....;c:'..;xKXx,
##     .0No         .:dOKNNNWNKOxkXWXo:,,;ONk;,,,,,;c0NXOxxkO0XXNXKOdc,.  ..;::,...;lol;..:xKXOl.
##     ,XX:             ..';cldxkOO0KKKXXXXXXXXXXKKKKK00Okxdol:;'..   .';::,..':llc,..'lkKXkc.
##     :NX'    .     ''            ..................             .,;:;,',;ccc;'..'lkKX0d;.
##     lNK.   .;      ,lc,.         ................        ..,,;;;;;;:::,....,lkKX0d:.
##    .oN0.    .'.      .;ccc;,'....              ....'',;;;;;;;;;;'..   .;oOXX0d:.
##    .dN0.      .;;,..       ....                ..''''''''....     .:dOKKko;.
##     lNK'         ..,;::;;,'.........................           .;d0X0kc'.
##     .xXO'                                                 .;oOK0x:.
##      .cKKo.                                    .,:oxkkkxk0K0xc'.
##        .oKKkc,.                         .';cok0XNNNX0Oxoc,.
##          .;d0XX0kdlc:;,,,',,,;;:clodkO0KK0Okdl:,'..
##              .,coxO0KXXXXXXXKK0OOxdoc:,..
