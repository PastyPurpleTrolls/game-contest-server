#include <iostream>
#include <cstdio>
#include <stdlib.h>
#include <cstdlib>
#include <ctime>

#include "SmarterPlayer.h"

/**
 * @brief Constructor that initializes any inter-round data structures.
 * @param boardSize Indication of the size of the board that is in use.
 *
 * The constructor runs when the AI is instantiated (the object gets created)
 * and is responsible for initializing everything that needs to be initialized
 * before any of the rounds happen. The constructor does not get called 
 * before rounds; newRound() gets called before every round.
 */
SmarterPlayer::SmarterPlayer( int boardSize )
    :PlayerV2(boardSize)
{
    // Could do any initialization of inter-round data structures here.
}

/**
 * @brief Destructor placeholder.
 * If your code does anything that requires cleanup when the object is
 * destroyed, do it here in the destructor.
 */
SmarterPlayer::~SmarterPlayer( ) {}

/*
 * Private internal function that initializes a MAX_BOARD_SIZE 2D array of char to water.
 */
void SmarterPlayer::initializeBoard() {
    for(int row=0; row<boardSize; row++) {
	for(int col=0; col<boardSize; col++) {
	    this->board[row][col] = WATER;
	    this->shipBoard[row][col] = WATER;
	    this->shotMatrix[row][col] = 0;
	}
    }
}

int SmarterPlayer::getNeighbors(int row, int col){
        int sum = 0;
        if (validShot(row-1, col))
            if (shipBoard[row-1][col] != WATER) sum++;
        if (validShot(row+1, col))
            if (shipBoard[row+1][col] != WATER) sum++;
        if (validShot(row, col-1))
            if (shipBoard[row][col-1] != WATER) sum++;
        if (validShot(row, col+1))
            if (shipBoard[row][col+1] != WATER) sum++;

        if (validShot(row-1, col+1))
            if (shipBoard[row-1][col+1] != WATER) sum++;
        if (validShot(row+1, col-1))
            if (shipBoard[row+1][col-1] != WATER) sum++;
        if (validShot(row-1, col-1))
            if (shipBoard[row-1][col-1] != WATER) sum++;
        if (validShot(row+1, col+1))
            if (shipBoard[row+1][col+1] != WATER) sum++;

        return sum;
}

/**
 * @brief Determines if a ship can be placed on given location
 * @param shipSize This size of the ship
 * @param dir Direction of the ship
 * @param row Row location on board
 * @param col Column location on board
 */
bool SmarterPlayer::canPlaceShip(int shipSize, Direction dir, int row, int col) {
    //Write logic
    if ( dir == Horizontal) {
	for (int i = 0; i < shipSize; ++i) {
	    if (shipBoard[row][col+i] != WATER || getNeighbors(row, col+i) > 1)
	        return false;
	}
	return true;
    } else {
	for (int i = 0; i < shipSize; ++i) {
	    if (shipBoard[row+i][col] != WATER || getNeighbors(row+i, col) > 1) {
		return false;
	    }
	}
	return true;
    }
}

/**
 * @brief Places ships on the board
 * @param shipSize This size of the ship
 * @param dir Direction of the ship
 * @param row Row location on board
 * @param col Column location on board
 */
void SmarterPlayer::placeOnBoard(int length, Direction dir, int row, int col) {
    //Write logic
    if (dir == Horizontal) {
	for (int i = 0; i < length; ++i) {
	    shipBoard[row][col+i] = SHIP;
	}
    } else {
	for (int i = 0; i < length; ++i) {
	    shipBoard[row+i][col] = SHIP;
	}
    }
}

/**
 * @brief Checks location for a valid shot
 * @param row Row location on the board
 * @param col Column location on the board
 */
bool SmarterPlayer::checkShot(int row, int col) {
    //Write logic
    if (row < 0 || row >= boardSize || col < 0 || col >= boardSize) return false;
    switch (board[row][col]) {
        case DUPLICATE_SHOT:
        case HIT:
        case KILL:
        case MISS:
            return false;
    }
    return true;
}

bool SmarterPlayer::validShot(int row, int col) {
    if (row < 0 || row >= boardSize) return false;
    if (col < 0 || col >= boardSize) return false;
    return true;

}

/**
 * @brief Searches for other possible HIT locations
 * @param row Row location on the board
 * @param col Column location on the board
 */
int* SmarterPlayer::searchAndDestroy(int row, int col) {
    int* loc = new int[2];
    for (int i = 1; i <= 4; i++){
        if (validShot(row-i, col)){
            char spot = board[row-i][col];
            if (spot == MISS || spot == DUPLICATE_SHOT || spot == KILL) break;
            if (spot == WATER){
                loc[0] = row-i;
                loc[1] = col;
                return loc;
            }
        }
    }
    for (int i = 1; i <= 4; i++){
        if (validShot(row+i, col)){
            char spot = board[row+i][col];
            if (spot == MISS || spot == DUPLICATE_SHOT || spot == KILL) break;
            if (spot == WATER){
                loc[0] = row+i;
                loc[1] = col;
                return loc;
            }
        }
    }

    for (int i = 1; i <= 4; i++){
        if (validShot(row, col-i)){
            char spot = board[row][col-i];
            if (spot == MISS || spot == DUPLICATE_SHOT || spot == KILL) break;
            if (spot == WATER){
                loc[0] = row;
                loc[1] = col-i;
                return loc;
            }
        }
    }

    for (int i = 1; i <= 4; i++){
        if (validShot(row, col+i)){
            char spot = board[row][col+i];
            if (spot == MISS || spot == DUPLICATE_SHOT || spot == KILL) break;
            if (spot == WATER){
                loc[0] = row;
                loc[1] = col+i;
                return loc;
            }
        }
    }

    loc[0] = -1;
    loc[1] = -1;
    return loc;
}

/**
 * @brief Specifies the AI's shot choice and returns the information to the caller.
 * @return Message The most important parts of the returned message are 
 * the row and column values. 
 *
 * See the Message class documentation for more information on the 
 * Message constructor.
 */
Message SmarterPlayer::getMove() {
    int * loc;
    for (int row = 0; row < boardSize; row++)
        for (int col = 0; col < boardSize; col++){
                if (board[row][col] == HIT){
                   loc = searchAndDestroy(row, col);
                   if (loc[0] != -1) {
                        Message outbound(SHOT, loc[0], loc[1], "Bang!", None, 1);
                        return outbound;
                   }
                }
        }

    
    int row = 0;
    int col = 0;
    int startCol = 0;
    while ( row < boardSize) {
        while (col < boardSize) {
            if (board[row][col] == WATER) {
                if (row >= 0 && row < boardSize && col >= 0 && col < boardSize){
                   Message result(SHOT, row, col, "Bang", None, 1);
                   return result;
                }
            }
            col += 3;
            if (col >= boardSize) {
                row++;
                startCol++;
                if (startCol > 2) {
                    startCol = 0;
                }
                col = startCol;
            }
            if (row > boardSize) break;
        }
    }

    for (int r = 0; r < boardSize; r++ ){
        for (int c = 0; c < boardSize; c++){
            if (checkShot(r, c)){
               Message result(SHOT, r, c, "Bang", None, 1);
               return result;
            }
        }
    }
    Message result(SHOT, -1, -1, "Bang", None, 1);
    return result;
}    

/**
 * @brief Tells the AI that a new round is beginning.
 * The AI show reinitialize any intra-round data structures.
 */
void SmarterPlayer::newRound() {
    /* DumbPlayer is too simple to do any inter-round learning. Smarter players 
     * reinitialize any round-specific data structures here.
     */
    this->lastRow = 0;
    this->lastCol = 0;
    this->phase = 0;
    this->numShipsPlaced = 0;

    this->initializeBoard();
}

/**
 * @brief Gets the AI's ship placement choice. This is then returned to the caller.
 * @param length The length of the ship to be placed.
 * @return Message The most important parts of the returned message are 
 * the direction, row, and column values. 
 *
 * The parameters returned via the message are:
 * 1. the operation: must be PLACE_SHIP 
 * 2. ship top row value
 * 3. ship top col value
 * 4. a string for the ship name
 * 5. direction Horizontal/Vertical (see defines.h)
 * 6. ship length (should match the length passed to placeShip)
 */
Message SmarterPlayer::placeShip(int length) {
    char shipName[10];
    // Create ship names each time called: Ship0, Ship1, Ship2, ...
    snprintf(shipName, sizeof shipName, "Ship%d", numShipsPlaced);
    
    while (true) { //random ship placement
	int row;
        int col;
	Direction dir = Direction(rand()%2 + 1);
	
	if (dir == Horizontal) {
	    row = rand()%boardSize;
	    col = rand()%((boardSize - length) + 1);
	} else {
            row = rand()%((boardSize - length) + 1);
            col = rand()%boardSize;
        }

	if (canPlaceShip(length, dir, row, col)) {
	    placeOnBoard(length, dir, row, col);
	    Message response(PLACE_SHIP, row, col, shipName, dir, length);
	    numShipsPlaced++;
	    return response;
	}
    }
}

/**
 * @brief Updates the AI with the results of its shots and where the opponent is shooting.
 * @param msg Message specifying what happened + row/col as appropriate.
 */
void SmarterPlayer::update(Message msg) {
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
	    // TODO: get rid of the cout, but replace in your AI with code that does something
	    // useful with the information about where the opponent is shooting.
	    //cout << gotoRowCol(20, 30) << "DumbPl: opponent shot at "<< msg.getRow() << ", " << msg.getCol() << flush;
	    break;
    }
}
