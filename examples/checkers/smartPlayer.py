#! /usr/bin/env python3

EMPTY = 0
INCs = [-1,1]
VALID_RANGE = range(8)
import random
def getPossibles(CB,player):
    possibles={}
    if player=="black":
        playerTokens=[3,4]
        opponentTokens=[1,2]
        rowInc=-1
    else:
        playerTokens=[1,2]
        opponentTokens=[3,4]
        rowInc=1
    possibles["moves"]=findMoves(CB,player,playerTokens,opponentTokens,rowInc)  #puts moves right into possibles D
    oldJumps=findJumps(CB,player,playerTokens,opponentTokens,rowInc)
    newJumps=expandJumps(CB,player,oldJumps,playerTokens,opponentTokens,rowInc)
    while newJumps != oldJumps:
        oldJumps=newJumps
        newJumps=expandJumps(CB,player,oldJumps,playerTokens,opponentTokens,rowInc)
    possibles["jumps"]=newJumps
    possibles["crownings"]=findCrownings(CB,player,possibles)
    possibles["blocks"]=findBlocks(CB,player, possibles["moves"] + possibles["jumps"])
    return possibles
def findBlocks(CB, player, playerMoves) :
    #Bascially I'm calling a block a move that prevents a jump, this means that a block can include moving away from the opponent.
    blocks = []
    if player=="black":
        player="red"
        playerTokens=[1,2]
        opponentTokens=[3,4]
        rowInc=1
    else:
        player="black"
        playerTokens=[3,4]
        opponentTokens=[1,2]
        rowInc=-1
    #Find jumps for opposing player
    oldJumps=findJumps(CB,player,playerTokens,opponentTokens,rowInc)
    jumps=expandJumps(CB,player,oldJumps,playerTokens,opponentTokens,rowInc)
    while jumps != oldJumps:
        oldJumps=jumps
        jumps=expandJumps(CB,player,oldJumps,playerTokens,opponentTokens,rowInc)
    #start looping through the jumps
    for jump in jumps :
        #Future proof, can handle multiple jumps
        moves = jump.split(":")
        #loop through each part of the jump, starting at the second part (I only want the "resting" place of the jump, so I can move to it and block it)
        #This will work for ANY part of a multi-jump, so I could perhaps turn a multi-jump into a normal jump.
        for i in range(1, len(moves)) :
            #loop through the moves that my player can make
            for playerMove in playerMoves :
                #check if final resting place of this move is also the finishing location of the jump
                if playerMove[-2:] == moves[i] :
                    #Hey, put it in the blocks list
                    if (playerMove not in blocks) :
                        blocks.append(playerMove)
    return blocks
def findCrownings(CB,player,possibles):
    crownings=[]
    empties=[]
    singleCheckerPositions=[]
    if player=="black":
        for col in range(1,8,2):
            if CB[0][col]==EMPTY:
                empties.append("A"+str(col))
        for row in range(8):
            for col in range(8):
                if CB[row][col]==3:
                    singleCheckerPositions.append(chr(row+65)+str(col))
    else:
        for col in range(0,8,2):
            if CB[7][col]==EMPTY:
                empties.append("H"+str(col))
        for row in range(8):
            for col in range(8):
                if CB[row][col]==1:
                    singleCheckerPositions.append(chr(row+65)+str(col))
    if len(empties)!=0:
        for move in possibles["moves"]:
            if move[3:] in empties and move[0:2] in singleCheckerPositions:
                crownings.append(move)
        for jump in possibles["jumps"]:
            if jump[-2:]in empties and jump[0:2] in singleCheckerPositions:
                crownings.append(jump)
    return crownings
def findMoves(CB,player,playerTokens,opponentTokens,rowInc):
    moves=[]
    #process all board positions
    for row in range(8):
        for col in range(8):
            if CB[row][col] in playerTokens:
                if CB[row][col] not in [2,4]: #not a king
                    for colInc in INCs:
                        toRow=row+rowInc
                        toCol=col+colInc
                        if toRow in VALID_RANGE and toCol in VALID_RANGE and CB[toRow][toCol]==EMPTY:
                                moves.append(chr(row+65)+str(col)+":"+chr(toRow+65)+str(toCol))
                else: #a king
                    for rInc in INCs:
                        for colInc in INCs:
                            toRow=row+rInc
                            toCol=col+colInc
                            if toRow in VALID_RANGE and toCol in VALID_RANGE and CB[toRow][toCol]==EMPTY:
                                    moves.append(chr(row+65)+str(col)+":"+chr(toRow+65)+str(toCol))

    return moves
def findJumps(CB,player,playerTokens,opponentTokens,rowInc):
    jumps=[]
    for row in range(8):
        for col in range(8):
            if CB[row][col] in playerTokens: #if this is a player piece
                if CB[row][col] not in [2,4]: #not a king
                    for colInc in INCs: #-1 and 1
                        jump=chr(row+65)+str(col)+":"
                        jumprow=row+rowInc
                        jumpcol=col+colInc
                        torow=row+2*rowInc
                        tocol=col+2*colInc
                        if jumprow in VALID_RANGE and jumpcol in VALID_RANGE and torow in VALID_RANGE and tocol in VALID_RANGE \
                        and CB[jumprow][jumpcol] in opponentTokens and CB[torow][tocol]==EMPTY:
                            jumps.append(jump+chr(torow+65)+str(tocol))
                else: #is a king
                    for colInc in INCs: #-1 and 1
                        for newRowInc in INCs:
                            jump=chr(row+65)+str(col)+":"
                            jumprow=row+newRowInc
                            jumpcol=col+colInc
                            torow=row+2*newRowInc
                            tocol=col+2*colInc
                            if jumprow in VALID_RANGE and jumpcol in VALID_RANGE and torow in VALID_RANGE and tocol in VALID_RANGE \
                            and CB[jumprow][jumpcol] in opponentTokens and CB[torow][tocol]==EMPTY:
                                jumps.append(jump+chr(torow+65)+str(tocol))
    return jumps
def expandJumps(CB,player,oldJumps,playerTokens,opponentTokens,rowInc):
    newJumps=[]
    for oldJump in oldJumps:
        row=ord(oldJump[-2])-65
        col=int(oldJump[-1])
        newJumps.append(oldJump)
        startRow=ord(oldJump[0])-65
        startCol=int(oldJump[1])
        if CB[startRow][startCol] not in [2,4]: #not a king
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
#The smart one
def automatedMove(CB, player) :
    possibles = getPossibles(CB, player)
    #player piece count
    count = 0
    if player == "black" :
        opponent = "red"
        piece = 3
        opPiece = 1
    else :
        opponent = "black"
        piece = 1
        opPiece = 3
    #Jumps are required, so if there are jumps those are my only options
    if (len(possibles["jumps"]) > 0) :
        options = possibles["jumps"]
        longestJump = options[0]
    else :
        options = possibles["moves"]
    #Okay, I've decided on my best bet so far (jumps or moves)
    #Now I need to actually think ahead, see around corners
    #Pick some moves, more advanced!
    #each move is weighted, the move(s) with the lowest weighting gets to go forward
    weighting = []
    #I only have one option, why bother checking to see if it is good?
    if (len(options) > 1) :
        #All the variables that I take into account:
        #If I'm moving to a "safe" spot (col 0 or 7)
        #If I'm moving to a crowning location
        #If I'm blocking a jump
        #Whether I could be jumped if I move to a particular spot.
        #If I could be jumped in a multi jump if I move
        #Am I a king? Then I don't want to be jumped if possible.
        #If moving would remove a block and enable a jump.
        #If moving would allow a crowning
        #Am I a king? Try to make sure I move towards my closest opponent
        #Is it a long multi-jump?
        #Whether I'm moving towards the nearest piece, this becomes more important towards the end of the game.
        #Trapping the other player into jumping me so I can jump him. Prefer trapping into multiple jumps.
        #What does this get me? A very defensive player that thinks carefully before moving.
        #################
        #Get locations of enemy pieces, also count how many pieces I have.
        locations = []
        for row in VALID_RANGE :
            for col in VALID_RANGE :
                if (CB[row][col] in [opPiece, opPiece + 1]) :
                    locations.append([row, col])
                elif (CB[row][col] != EMPTY) :
                    count += 1
        for i in range(len(options)) :
            weighting.append(0)
            #is the move a crowning or a block?
            if options[i] in possibles["crownings"] :
                weighting[-1] += -2
            if (options[i] in possibles["blocks"]) :
                weighting[-1] += -3
            #Multi jumps
            if (len(options[i]) > 5) :
                weighting[-1] += -1
                #The longest multi-jump?
                if (len(options[i]) > len(longestJump)) :
                    longestJump = options[i]
            #Before I go further, I'd like to check the current state of the board.
            if (options[i] not in possibles["blocks"]) :
                opponentPossibles = getPossibles(CB, opponent)
                for jump in opponentPossibles["jumps"] :
                    movesOp = jump.split(":")
                    currRowOp = ord(movesOp[0][0]) - 65
                    currColOp = int(movesOp[0][1])
                    for move in range(len(movesOp)) :
                        toRowOp = ord(movesOp[move][0]) - 65
                        toColOp = int(movesOp[move][1])
                        #This move could possibly move me out of a jump position
                        if (toRowOp + (currRowOp - toRowOp) // 2 == ord(options[i][0]) - 65) and (toColOp + (currColOp - toColOp) // 2 == int(options[i][1])) :
                            weighting[-1] += -3
                        currRowOp = toRowOp
                        currColOp = toColOp
            #Simulate the move in a copy of the game tracker
            moves = options[i].split(":")
            #Get a copy of the game tracker
            copyCB = copyList(CB)
            #Adjust the game tracker
            currRow = ord(moves[0][0]) - 65
            currCol = int(moves[0][1])
            currSquare = copyCB[currRow][currCol]
            origSquare = currSquare
            for move in range(1, len(moves)) :
                toRow = ord(moves[move][0]) - 65
                toCol = int(moves[move][1])
                copyCB[currRow][currCol] = 0
                if (abs(toRow - currRow) == 2) and (abs(toCol - currCol) == 2) :
                    copyCB[toRow + (currRow - toRow) // 2][toCol + (currCol - toCol) // 2] = 0
                if (toRow in [0, 7]) :
                    currSquare = piece + 1
                copyCB[toRow][toCol] = currSquare
                currRow = toRow
                currCol = toCol
            #If I'm moving to a "safe" spot, prefer it. Only prefer it if it is still early in the game.
            if (currCol in [0, 7] and not(count + len(locations) <= 13 and count >= len(locations))) :
                weighting[-1] += -2
            #Finished adjusting game tracker, let's get down to business
            #Get the opponent moves AFTER I have made my move
            opponentPossibles = getPossibles(copyCB, opponent)
            #This is to make sure two possible jumps on the same location don't trigger as a worse move
            #than one possible jump on one location
            singleJump = False
            multiJump = False
            trap = False
            for jump in opponentPossibles["jumps"] :
                jumpCB = copyList(copyCB)
                #If my jump is better then his, leave my jump in.
                if (len(options[i]) > len(jump)) :
                    weighting[-1] += -3
                else :
                    #Check if jump could result in a crowning
                    if (jump in opponentPossibles["crownings"]) :
                        weighting[-1] += 2
                    movesOp = jump.split(":")
                    currRowOp = ord(movesOp[0][0]) - 65
                    currColOp = int(movesOp[0][1])
                    jumpSquare = jumpCB[currRowOp][currColOp]
                    for move in range(1, len(movesOp)) :
                        toRowOp = ord(movesOp[move][0]) - 65
                        toColOp = int(movesOp[move][1])
                        #execute the jump in the copy
                        jumpCB[currRowOp][currColOp] = 0
                        jumpCB[toRowOp + (currRowOp - toRowOp) // 2][toColOp + (currColOp - toColOp) // 2] = 0
                        jumpCB[toRowOp][toColOp] = jumpSquare
                        #Check to make sure I'm not moving into a jump
                        if (toRowOp + (currRowOp - toRowOp) // 2 == toRow) and (toColOp + (currColOp - toColOp) // 2 == toCol) :
                            if not(singleJump) :
                                weighting[-1] += 3
                                singleJump = True
                            #multi jump, weight it even higher because I would prefer a different move
                            if (len(jump) > 5) and not(multiJump) :
                                weighting[-1] += 2
                                multiJump = True
                            #king, I would prefer this not be jumped
                            if (currSquare in [2, 4]) and (not(multiJump) or not(singleJump)) :
                                weighting[-1] += 1
                        #Check to make sure I'm not removing a block
                        if (toRowOp == ord(moves[0][0]) - 65 and toColOp == int(moves[0][1])) :
                            #check to see if jumped piece is one of my other pieces
                            if (toRowOp + (currRowOp - toRowOp) // 2 != toRow) or (toColOp + (currColOp - toColOp) // 2 != toCol) :
                                weighting[-1] += 3
                                #multi jump, weight it even higher because I would prefer a different move
                                if (len(jump) > 5) :
                                    weighting[-1] += 2
                        currRowOp = toRowOp
                        currColOp = toColOp
                    #Trap
                    #The only reason I limit it to one jump is I would prefer to be certain that he will take this move
                    #I also don't want to take this if there is a block, I don't want a king to be jumped
                    if (len(opponentPossibles["jumps"]) == 1 and (options[i] in possibles["blocks"] or len(possibles["blocks"]) == 0) and (origSquare != piece + 1 or jumpSquare == opPiece + 1)) :
                        countAfterJump = 0
                        for row in VALID_RANGE :
                            for col in VALID_RANGE :
                                if (jumpCB[row][col] in [piece, piece + 1]) :
                                    countAfterJump += 1
                        #Don't bother checking if there would be no pieces left after I get jumped
                        if (countAfterJump > 0) :
                            possiblesFuture = getPossibles(jumpCB, player)
                            for futureJump in possiblesFuture["jumps"] :
                                if (len(futureJump) > len(jump)) or (count > len(locations) and (countAfterJump > len(locations) - 1)) :
                                    weighting[-1] += -4
                                    #Multijump, compensate more
                                    if (len(jump) > 5) :
                                        weighting[-1] += -1
                                    trap = True
            #check if moving would allow a crowning
            for crown in opponentPossibles["crownings"] :
                if (crown.find(moves[0][0] + moves[0][1]) != -1) :
                    weighting[-1] += 2
            #Basic path finding, move in direction of nearest piece
            if (options[i] in possibles["moves"] and options[i] not in possibles["blocks"] and origSquare == piece + 1) :
                if (len(locations) > 0) :
                    closest = [locations[0][0], locations[0][1]]
                    #get the closest piece
                    for location in locations :
                        #is this piece jumpable? Only move towards jumpable pieces
                        if ((location[0] not in [0, 7]) and (location[1] not in [0, 7]) or len(locations) < 2) :
                                rowDiff = abs(location[0] - (ord(moves[0][0]) - 65))
                                colDiff = abs(location[1] - int(moves[0][1]))
                                if (rowDiff <= abs(closest[0] - (ord(moves[0][0]) - 65))) and (colDiff <= abs(closest[1] - int(moves[0][1]))) :
                                    closest[0] = location[0]
                                    closest[1] = location[1]
                    #Detect moving a row away from nearest piece
                    if (closest[0] > ord(moves[0][0]) - 65 and ((ord(moves[0][0]) - 65) - (ord(moves[-1][0]) - 65) > 0)) or (closest[0] < (ord(moves[0][0]) - 65) and ((ord(moves[0][0]) - 65) - (ord(moves[-1][0]) - 65) < 0)) :
                        weighting[-1] += 1
                        #Detect moving a column away from nearest piece
                        if (closest[1] >= int(moves[-1][1]) and (int(moves[0][1]) - int(moves[-1][1]) > 0)) or (closest[1] >= int(moves[-1][1]) and (int(moves[0][1]) - int(moves[-1][1]) < 0)) :
                            weighting[-1] += 1
            #Check how I could move in the future if I made this move.
            possiblesFuture = getPossibles(copyCB, player)
            #I can't move anymore? Don't move into a losing situations
            if (len(possiblesFuture["moves"]) == 0 and len(possiblesFuture["jumps"]) == 0) :
                weighting[-1] += 2
            #Moving would allow some jumps in the future! YEAH!
            if (len(possiblesFuture["jumps"]) > 0 and weighting[-1] <= 0 and not(trap)) :
                weighting[-1] += -1
            #Moving would allow a crowning in future!
            if (len(possiblesFuture["crownings"]) > 0) :
                weighting[-1] += -1
    #It's a long jump!
    if (len(possibles["jumps"]) > 0 and len(weighting) != 0) :
        if (len(longestJump) > 8) :
            weighting[options.index(longestJump)] += -1
    #The final moves list, these are the "best of the best"
    final = []
    if (len(weighting) != 0) :
        for i in range(len(weighting)) :
            #Is the current value the lowest value in the list? If so append the parrell value in the options list to the final moves list
            if (weighting[i] == min(weighting)) :
                final.append(options[i])
    else :
        final = options
    #There could be more than one, but in theory they are all equal in how "good" they are. Pick one randomly
    index = random.randint(0, len(final) - 1)
    return final[index]
#make a complete copy of a list, including internal lists
def copyList(inList):
    if isinstance(inList, list):
        return list( map(copyList, inList) )
    return inList

import checkers_helper
checkers_helper.init(automatedMove)
