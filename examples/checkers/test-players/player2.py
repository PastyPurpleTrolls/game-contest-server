EMPTY=0
INCs=[-1,1]
VALID_RANGE=range(8)
DEFAULT_DEPTH = 5
KING_VALUE = 2
SPACE_MULTIPLIER  = .01
KINGS = ["R", "B"]

def listValidMoves(CB,playerTokens,opponentTokens,rowInc):
    validMoves=[]
    for row in VALID_RANGE:
        for col in range(row%2, 8, 2):
            if CB[row][col] == playerTokens[0]: #it is the specified player's checker
                for colInc in INCs:
                    toRow=row+rowInc
                    toCol=col+colInc
                    if toRow in VALID_RANGE and toCol in VALID_RANGE and CB[toRow][toCol]==EMPTY:
                        validMoves.append(chr(row+65)+str(col)+":"+chr(toRow+65)+str(toCol))
            elif CB[row][col] == playerTokens[1]: #is a king checker
                for rInc in INCs:
                    for colInc in INCs:
                        toRow=row+rInc
                        toCol=col+colInc
                        if toRow in VALID_RANGE and toCol in VALID_RANGE and CB[toRow][toCol]==EMPTY:
                            validMoves.append(chr(row+65)+str(col)+":"+chr(toRow+65)+str(toCol))
    return validMoves

def expandJumps(CB,oldJump,playerTokens,opponentTokens,rowInc):
    newJumps=[]
    row=ord(oldJump[-2])-65
    col=int(oldJump[-1])
    newJump = False
    startRow=ord(oldJump[0])-65
    startCol=int(oldJump[1])
    if CB[startRow][startCol] == playerTokens[0]: #not a king
        for colInc in INCs:
            jumprow=row+rowInc
            jumpcol=col+colInc
            torow=row+2*rowInc
            tocol=col+2*colInc
            if torow in VALID_RANGE and tocol in VALID_RANGE and CB[jumprow][jumpcol] in opponentTokens and CB[torow][tocol]==EMPTY:
                newJumps+=expandJumps(CB, oldJump+":"+chr(torow+65)+str(tocol), playerTokens,opponentTokens,rowInc)
                newJump = True
    elif CB[startRow][startCol] == playerTokens[1]: #is a king
        for colInc in INCs:
            for newRowInc in INCs:
                jumprow=row+newRowInc
                jumpcol=col+colInc
                torow=row+2*newRowInc
                tocol=col+2*colInc
                if torow in VALID_RANGE and tocol in VALID_RANGE \
                and CB[jumprow][jumpcol] in opponentTokens and (CB[torow][tocol]==EMPTY or oldJump[0:2]==chr(torow+65)+str(tocol)) \
                and ((oldJump[-2:]+":"+chr(torow+65)+str(tocol)) not in oldJump) and ((chr(torow+65)+str(tocol)+':'+oldJump[-2:] not in oldJump)):
                    newJumps+=expandJumps(CB, oldJump+":"+chr(torow+65)+str(tocol),playerTokens,opponentTokens,rowInc)
                    newJump = True
    if not newJump:
        newJumps.append(oldJump)
    return newJumps

def listValidJumps(CB,playerTokens,opponentTokens,rowInc):
    validJumps=[]
    for row in range(8):
        for col in range(row%2, 8, 2):
            if CB[row][col] == playerTokens[0]: #it is the specified player's checker
                for colInc in INCs:
                    toRow=row+(rowInc*2)
                    toCol=col+(colInc*2)
                    jumpRow=row+rowInc
                    jumpCol=col+colInc
                    if toRow in VALID_RANGE and toCol in VALID_RANGE and CB[toRow][toCol]==EMPTY and CB[jumpRow][jumpCol]in opponentTokens:
                        validJumps.append(chr(row+65)+str(col)+":"+chr(toRow+65)+str(toCol))
            elif CB[row][col] == playerTokens[1]: #is a king checker
                for rInc in INCs:
                    for colInc in INCs:
                        toRow=row+(rInc*2)
                        toCol=col+(colInc*2)
                        jumpRow=row+rInc
                        jumpCol=col+colInc
                        if toRow in VALID_RANGE and toCol in VALID_RANGE and CB[toRow][toCol]==EMPTY and CB[jumpRow][jumpCol]in opponentTokens:
                            validJumps.append(chr(row+65)+str(col)+":"+chr(toRow+65)+str(toCol))
    totalJumps = []
    for a in validJumps:
        newJumps = expandJumps(CB,a,playerTokens,opponentTokens,rowInc)
        totalJumps +=newJumps
    return totalJumps

def getMove(board,playerIndex,playerColors,playerTokens,opponentTokens,rowInc):
    validMoves=listValidJumps(board,playerTokens,opponentTokens,rowInc)
    if len(validMoves) == 0:
        validMoves=listValidMoves(board,playerTokens,opponentTokens,rowInc)
    moves_list = {}
    for move in validMoves:
        moves_list[getBestMove(moveBoard(board, move), opponentTokens, playerTokens, rowInc*-1)] = move
    return moves_list[min(moves_list.keys())]

def getBestMove(board,playerTokens,opponentTokens,rowInc, depth = DEFAULT_DEPTH):
    if depth==0:
        return(get_piece_ratio(board,playerTokens,opponentTokens, rowInc))
    else:
        validMoves=listValidJumps(board,playerTokens,opponentTokens,rowInc)
        if len(validMoves) == 0:
            validMoves=listValidMoves(board,playerTokens,opponentTokens,rowInc)
            if len(validMoves) == 0:
                return 1/(100+depth)
        moves_list = []
        for move in validMoves:
            moves_list.append(getBestMove(moveBoard(board, move), opponentTokens, playerTokens, rowInc*-1, depth-1))
        return 1/max(moves_list)

def get_piece_ratio(board,playerTokens,opponentTokens, Inc):
    player_pieces = 0
    opponent_pieces = 0
    for row in range(len(board)):
        for square in board[row][row%2::2]:
            if square == playerTokens[0]:
                player_pieces +=1 + row*SPACE_MULTIPLIER*Inc
            elif square == playerTokens[1]:
                player_pieces +=KING_VALUE + (3.5-abs(3.5-row))*SPACE_MULTIPLIER
            elif square == opponentTokens[0]:
                opponent_pieces +=1 + (7-row)*SPACE_MULTIPLIER*Inc
            elif square == opponentTokens[1]:
                opponent_pieces +=KING_VALUE + (3.5-abs(3.5-row))*SPACE_MULTIPLIER
    if opponent_pieces == 0:
        return 100
    elif player_pieces == 0:
        return .01
    else:
        return player_pieces/opponent_pieces

def moveBoard(orig_board, fromTo):
    board = []
    for a in orig_board:
        board.append(a[:])
    while len(fromTo)>=5:
        fromRow=ord(fromTo[0])-65
        fromCol=int(fromTo[1])
        toRow=ord(fromTo[3])-65
        toCol=int(fromTo[4])
        if toRow in [0, 7]:
            board[toRow][toCol]=board[fromRow][fromCol].upper()
        else:
            board[toRow][toCol]=board[fromRow][fromCol]
        board[fromRow][fromCol]=0
        if abs(fromRow-toRow)==2: #if a jump, also blank intervening cell
            board[(fromRow+toRow)//2][(fromCol+toCol)//2]=0
        fromTo=fromTo[3:]
    return board