// BATTLESHIP AI

#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <ctime>
#include <iomanip>

#include "conio.h"
#include "FergusonHursey.h"

using namespace conio;

// CONSTRUCTOR
FergusonHursey::FergusonHursey( int boardSize )
    :PlayerV2(boardSize)
{}

//DESTRUCTOR
FergusonHursey::~FergusonHursey( ) {}

// START OF GAME INITIALIZATION
void FergusonHursey::initializeBoard() {
    for(int i=0; i<boardSize; i++) {
	    for(int j=0; j<boardSize; j++) {
	        this->board[i][j] = WATER;
            this->shipMatrix[i][j] = WATER;
            this->shotMatrix[i][j] = 0;
        }
    }
}

// FIGURES OUT WHERE TO SHOOT
Message FergusonHursey::getMove() {
    this->updateMatrix();
    int max = 0;
    for(int row = 0; row < boardSize; row++) {
        for(int col = 0; col < boardSize; col++) {
            if (shotMatrix[row][col] > max) {
                max = shotMatrix[row][col];
            }
        }
    }

    for(int row = 0; row < boardSize; row++) {
        for(int col = 0; col < boardSize; col++) {
            cerr << setw(3) << shotMatrix[row][col];
            if (shotMatrix[row][col] == max) {
                maxRow = row;
                maxCol = col;
            }
        } 
        cerr << endl;
    }
    cerr << endl;

    Message result( SHOT, maxRow, maxCol, "Bang", None, 1 );
    return result;
}

// INITIALIZES NEW ROUND (INTER-ROUND LEARNING WOULD GO HERE)
void FergusonHursey::newRound() {
    this->maxRow = -1;
    this->maxCol = -1;
    this->numShipsPlaced = 0;

    this->initializeBoard();
} 


/* THIS CODE DEALS WITH RANDOM SHOT PLACEMENT

bool FergusonHursey::canPlaceShip(int length, Direction dir, int xcoord, int ycoord) {
    if (dir == Horizontal) {
        for (int i = 0; i < length; i++) {
            if (shipMatrix[xcoord][ycoord + i] != WATER) {
                return false;
            }
        }
    }

    else {
        for (int i = 0; i < length; i++) {
            if (shipMatrix[xcoord + i][ycoord] != WATER) {
                return false;
            }
        }
    }

    return true;
}


void FergusonHursey::placeOnBoard(int length, Direction dir, int xcoord, int ycoord) {
    if (dir == Horizontal) {
        for (int i = 0; i < length; i++) {
            shipMatrix[xcoord][ycoord + i] = SHIP;
        }
    }

    else {
        for (int i = 0; i < length; i++) {
            shipMatrix[xcoord + i][ycoord] = SHIP;
        }
    }
}


Message FergusonHursey::placeShip(int length) {
    char shipName[10];
    
    snprintf(shipName, sizeof shipName, "Ship%d", numShipsPlaced);

    while(true) {
        int xcoord = -1;
        int ycoord = -1;
        Direction dir = Direction(rand() % 2 + 1);

        if (dir == Horizontal) {
            xcoord = rand() % (boardSize);
            ycoord = rand() % (boardSize - length);
        }
        else {
            xcoord = rand() % (boardSize - length);
            ycoord = rand() % (boardSize);
        }

        if (canPlaceShip(length, dir, xcoord, ycoord) == true) {
            placeOnBoard(length, dir, xcoord, ycoord);
            Message response( PLACE_SHIP, xcoord, ycoord, shipName, dir, length );
            numShipsPlaced++;
            return response;
        }
    }
}

*/

// HARD-CODED SHIP PLACEMENT (MOSTLY ON EDGES)
Message FergusonHursey::placeShip(int length) {
    char shipName[10];
    
    snprintf(shipName, sizeof shipName, "Ship%d", numShipsPlaced);
    int xcoord = 0;
    int ycoord = 0;
    Direction direction = Horizontal;

    switch(numShipsPlaced) {
        case 0:
            break;
        case 1:
            ycoord = boardSize - 1;
            direction = Vertical;
            break;
        case 2:
            xcoord = boardSize - 1;
            ycoord = boardSize - length;
            break;
        case 3:
            xcoord = boardSize-length;
            direction = Vertical;
            break;
        case 4:
            xcoord = 1;
            ycoord = 1;
            direction = Vertical;
            break;
        case 5:
            xcoord = 1;
            ycoord = boardSize-2;
            direction = Vertical;
            break;
    }

    Message response( PLACE_SHIP, xcoord, ycoord, shipName, direction, length );
    numShipsPlaced++;
    return response;
}


// CALCULATES HORIZONTAL PROBABILITY (EACH ROW)
int FergusonHursey::horizontalProbCalc(int row, int col) {
    if (board[row][col] != WATER) {
        return -1;
    }

    int totalCount = 0;
    int count =0;
    for (int c = col; c < col + 3; c++) {
        if (c - 2 >= 0 && c < boardSize) {
            for (int i = 0; i < 3; i++) {
                char ch = board[row][c-i];
                if (ch == KILL || ch == MISS) {
                    count = 0;
                    break;
                }
                else if (ch == HIT) {
                    count += 10;
                }
                else {
                    count++;
                }
            }
            totalCount += count;
            count = 0;
        }
    }
    return totalCount;
}

// CALCULATES VERTICAL PROBABILITY (EACH COLUMN)
int FergusonHursey::verticalProbCalc(int row, int col) {
    if (board[row][col] != WATER) {
        return -1;
    }

    int totalCount = 0;
    int count = 0;
    for (int r = row; r < row + 3; r++) {
        if (r - 2 >= 0 && r < boardSize) {
            for (int i = 0; i < 3; i++) {
                char ch = board[r-1][col];
                if (ch == KILL || ch == MISS) {
                    count = 0;
                    break;
                }
                else if (ch == HIT) {
                    count += 10;
                }
                else {
                    count++;
                }
            }
            totalCount += count;
            count = 0;
        }
    }
    return totalCount;
}

// CALCULATES TOTAL PROBABILITY OF EACH CELL
int FergusonHursey::totalCalculator(int row, int col) {
    return verticalProbCalc(row, col) + horizontalProbCalc(row, col);
}

// UPDATES SHOT MATRIX
void FergusonHursey::updateMatrix() {
    for(int row = 0; row < boardSize; row++) {
        for(int col = 0; col < boardSize; col++) {
            this->shotMatrix[row][col] = totalCalculator(row, col);
        }
    }
}


// UPDATES THE AI WITH THE RESULTS OF ITS SHOTS AND WHERE THE OPPONENT IS SHOOTING
void FergusonHursey::update(Message msg) {
    switch(msg.getMessageType()) {
	case HIT:
	case KILL:
	case MISS:
	    board[msg.getRow()][msg.getCol()] = msg.getMessageType();
	    break;
	case WIN:
	    break;
	case LOSE:
	    break;
	case TIE:
	    break;
	case OPPONENT_SHOT:
	    break;
    }
}