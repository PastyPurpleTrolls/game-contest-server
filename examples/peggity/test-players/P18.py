#first move random, second move next to other players peg
import random
def manualMove(pcolors,currentPlayer,board):
    for row in range(15):
        for col in range(15):
            if board[row][col]!=0:
                #horizontal
                if col<11:
                    count=1
                    for offset in range(1,5,1):
                        if board[row][col]==board[row][col+offset]:
                            count+=1
                            if count==3:
                                count3=[]
                                count3.append(row)
                                count3.append(col+offset)
                            if count==4:
                                count4=[]
                                count4.append(row)
                                count4.append(col+offset)
                    if count==3:
                        return count3[0],count3[1:]
                    if count==4:
                        return count4[0],count4[1:]
                #vertical
                if row<11:
                    count=1
                    for offset in range(1,5,1):
                        if board[row][col]==board[row+offset][col]:
                            count+=1
                            if count==3:
                                count3=[]
                                count3.append(row+offset)
                                count3.append(col)
                            if count==4:
                                count4=[]
                                count4.append(row+offset)
                                count4.append(col)
                    if count==3:
                        return count3[0],count3[1:]
                    if count==4:
                        return count4[0],count4[1:]
                #CHECK DIAGONALS
                #left to right
                if row<11 and col<11:
                    count=1
                    for offset in range(1,5,1):
                        if board[row][col]==board[row+offset][col+offset]:
                            count+=1
                            if count==3:
                                count3=[]
                                count3.append(row+offset)
                                count3.append(col+offset)
                            if count==4:
                                count4=[]
                                count4.append(row+offset)
                                count4.append(col+offset)
                    if count==3:
                        return count3[0],count3[1:]
                    if count==4:
                        return count4[0],count4[1:]
                #right to left
                if row<11 and col>3:
                    count=1
                    for offset in range(1,5,1):
                        if board[row][col]==board[row+offset][col-offset]:
                            count+=1
                            if count==3:
                                count3=[]
                                count3.append(row+offset)
                                count3.append(col+offset)
                            if count==4:
                                count4=[]
                                count4.append(row+offset)
                                count4.append(col+offset)
                    if count==3:
                        return count3[0],count3[1:]
                    if count==4:
                        return count4[0],count4[1:]
                        
    for ranNum in range(15):
        for row in range(15):
            for col in range(15):
                #print(row,col,ranNum)
                if (board[row][col]==currentPlayer) and board[row][col+ranNum]==0:
                    return row,(col+ranNum)
                elif (board[row][col]==currentPlayer) and board[row][col-ranNum]==0:
                    return row,(col-ranNum)
                elif (board[row][col]==currentPlayer) and board[row+1][col]==0:
                    return (row+1),col
                elif (board[row][col]==currentPlayer) and board[row-1][col]==0:
                    return (row-1),col
                elif (board[row][col]==currentPlayer) and board[row+1][col+ranNum]==0:
                    return row+1,col+ranNum
                elif (board[row][col]==currentPlayer) and board[row-1][col+ranNum]==0:
                    return row-1,col+ranNum
                elif (board[row][col]==currentPlayer) and board[row+1][col-ranNum]==0:
                    return row+1,col-ranNum
                elif (board[row][col]==currentPlayer) and board[row-1][col-ranNum]==0:
                    return row-1,col-ranNum
    print("test")
    emptyCellsList=[]
    for row in range(15):
        for col in range(15):
            if board[row][col]==0:
                emptyCellsList.append(chr(65+row+1)+str(col+1))
    move=emptyCellsList[random.randrange(0,len(emptyCellsList))]
    row=ord(move[0])-65
    col=int(move[1:])
    return row,col
