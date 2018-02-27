import random
def manualMove(pcolors,currentPlayer,board):
    emptyCellsList=[]
    for row in range(15):
        for col in range(15):

            if(board[row][col] == currentPlayer):

                count = 0
                tRow = row
                tCol = col

                while tCol < 14 and board[row][tCol] == currentPlayer:
                    count += 1
                    tCol += 1

                if count >= 4:
                    return row, tCol

                count = 0
                tCol = col

                while tRow < 14 and board[tRow][col] == currentPlayer:
                    count += 1
                    tRow += 1

                if count >= 4:
                    return tRow, col

                count = 0
                tRow = row

                while tCol < 14 and tRow < 14 and board[tRow][tCol] == currentPlayer:
                    count += 1
                    tRow += 1
                    tCol += 1

                if count >= 4:
                    return tRow, tCol
                
                if col + 1 < 15 and board[row][col + 1] == 0:
                    return row, col + 1
                elif row + 1 < 15 and board[row + 1][col] == 0:
                    return row + 1, col
                elif row + 1 < 15 and col + 1 < 15 and board[row + 1][col + 1] == 0:
                    return row + 1, col + 1
            
            if board[row][col]==0:
                emptyCellsList.append(chr(65+row)+str(col))
                
    move=emptyCellsList[random.randrange(0,len(emptyCellsList))]
    row=ord(move[0])-65
    col=int(move[1:])
    
    return row,col
