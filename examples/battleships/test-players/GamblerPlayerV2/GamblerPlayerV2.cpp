/**
 * @authors Stefan Brandle & Jonathan Geisler
 * @date May, 2004
 *
 */

#include <iostream>
#include <cstdio>
#include <cstdlib>

#include "GamblerPlayerV2.h"

using namespace std;

GamblerPlayerV2::GamblerPlayerV2( int boardSize ):
    PlayerV2(boardSize)
{
    lastRow = 0;
    lastCol = 0;
    numShipsPlaced = 0;

    for(int row=0; row<boardSize; row++) {
	for(int col=0; col<boardSize; col++) {
	    this->opponentShots[row][col] = 0;
	}
    }

    reWeighBoard( cellWeights );
}

/*
 * Private internal function that initializes a MAX_BOARD_SIZE 2D array of char to water.
 */
void GamblerPlayerV2::initializeBoard(char board[MAX_BOARD_SIZE][MAX_BOARD_SIZE]) {
    for(int row=0; row<boardSize; row++) {
	for(int col=0; col<boardSize; col++) {
	    board[row][col] = WATER;
	}
    }
}

/**
 * @brief Tells the AI that a new round is beginning.
 * The AI show reinitialize any intra-round data structures.
 */
void GamblerPlayerV2::newRound() {
    // Reinitialize any round-specific data structures here.

    this->numShipsPlaced = 0;
    this->shipMark = 'a';

    this->initializeBoard(this->board);
    this->initializeBoard(this->shipBoard);
}


/**
 * Gets the computer's shot choice. This is then returned to the caller.
 * @return int[] shot
 *  Position 0 of the int array should hold the row, position 1 the column.
 */
Message GamblerPlayerV2::getMove() {
    getShot(shot);
    Message msg(SHOT, shot[0], shot[1], "Gamble shot", None, 1);
    return msg;
}

/**
 * @brief Updates the AI with the results of its shots and where the opponent is shooting.
 * @param msg Message specifying what happened + row/col as appropriate.
 */
void GamblerPlayerV2::update(Message msg) {
    switch(msg.getMessageType()) {
	case HIT:
	case KILL:
	case MISS:
	    board[msg.getRow()][msg.getCol()] = msg.getMessageType();
	    break;
	case OPPONENT_SHOT:
	    opponentShots[msg.getRow()][msg.getCol()]++;
	    //cout << gotoRowCol(3, 30) << "CleanPl: opponent shot at "<< msg.getRow() << ", " << msg.getCol() << flush;
	    break;
    }
}
/**
 * @brief Asks the AI where it wishes to place one of its ships.
 * @param length The length of the ship to be placed.
 * @return Message A message with the row,col and direction of the ship.
 */
Message GamblerPlayerV2::placeShip(int length) {
    char shipName[10];
    // Create ship names each time called: Ship0, Ship1, Ship2, ...
    snprintf(shipName, sizeof shipName, "Ship%d", numShipsPlaced);

    int row, col;
    Direction dir;

    if( length > boardSize ) return false;	// Ship too big for board

    while(true) {
	chooseValues(row, col, length, dir);
	if( positionOk(row, col, length, dir) ) {
	    numShipsPlaced++;
	    markShip(row, col, length, dir);
	    Message response( PLACE_SHIP, row, col, string(shipName), dir, length );

	    return response;
	}
    }

    // To keep the compiler happy
    Message response(char(0));
    return response;
}

/*
 * Private internal function that marks a ship that is being placed.
 */
void GamblerPlayerV2::markShip( int row, int col, int length, Direction dir ) {
    if( dir==Horizontal ) {
	for(int c=col; c<col+length; c++) {
	    shipBoard[row][c] = SHIP;
	}
    } else {
	for(int r=row; r<row+length; r++) {
	    shipBoard[r][col] = SHIP;
	}
    }
}

/*
 * Private internal function that determines whether a particular ship location is collision-free.
 */
bool GamblerPlayerV2::positionOk( int row, int col, int length, Direction dir ) {
    if( dir==Horizontal ) {
	for(int c=col; c<col+length; c++) {
	    if(shipBoard[row][c] != WATER) return false;
	}
    } else {
	for(int r=row; r<row+length; r++) {
	    if(shipBoard[r][col] != WATER) return false;
	}
    }
    return true;
}

void GamblerPlayerV2::getShot(int shot[]) {
    if( getCellStatus(lastRow, lastCol) == HIT ) {
	getFollowUpShot( lastRow, lastCol, shot );
    } else if( haveUnfinishedBusiness(shot) ){
	getFollowUpShot( shot[0], shot[1], shot );
    } else {
	getNextProbe( shot );
	lastRow = shot[0];
	lastCol = shot[1];
    }
}

/*
 * Private internal function that chooses values for where to try placing a ship.
 */
void GamblerPlayerV2::chooseValues( int& row, int& col, int& length, Direction& dir ) {
    dir = Direction( rand()%2 + 1 );
    if( dir==Horizontal ) {
        row = rand() % boardSize;
	col = rand() % (boardSize+1 - length);
    } else {	// vertical
	row = rand() % (boardSize+1 - length);
        col = rand() % boardSize;
    }
}

//***********************************************
// MAIN SHOT ROUTINES ***************************
//***********************************************

// Gets a probing shot. Grabs a cell matching the current max board cell weight.
void GamblerPlayerV2::getNextProbe( int shot[] ) {
    reWeighBoard( cellWeights );
    getMaxWeightCell( cellWeights, shot );
}

// Used to follow up on a wounded ship.
// The code needs to be improved to use weights to determine best
// followup locations.
void GamblerPlayerV2::getFollowUpShot( int row, int col, int shot[] ) {

    // Starting to play around with weights. Code place-holder.
    //int nextRow = 0, nextCol = 0;
    //int weightUp = calcCellWeight( row-1, col );
    // Done playing around with weights.  :-)

    // Check for viable shot UP
    if( search(row, col, -1, 0, shot, SHIP_MAX_LENGTH) == true ) {
	return;
    }
    // Ok, nothing [left] to shot at UP. But was there at least something UP?
    // If so, it may be worth checking in the opposite direction might be faster.
    else if( onBoard(row-1, col) && getCellStatus(row-1, col) == HIT ) {
	if( search( row, col, 1, 0, shot, SHIP_MAX_LENGTH-1) == true ) {
	    return;
	}
    }
    // Check for viable shot to RIGHT
    if ( search( row, col, 0, 1, shot, SHIP_MAX_LENGTH ) == true ) {
	return;
    } 
    // Ok, nothing [left] to shot at to RIGHT. But was there at least something to RIGHT?
    // If so, it may be worth checking in the opposite direction might be faster.
    else if( onBoard(row, col+1) && getCellStatus(row, col+1) == HIT ) {
	if( search( row, col, 0, -1, shot, SHIP_MAX_LENGTH-1) == true ) {
	    return;
	}
    }
    // At this point, check DOWN and to LEFT, but don't do reverse checks because 
    // anything there will have been covered above.
    if ( search( row, col, 1, 0, shot, SHIP_MAX_LENGTH ) == true ) {
	return;
    } 
    if ( search( row, col, 0, -1, shot, SHIP_MAX_LENGTH ) == true ) {
	return;
    } else {
	getNextProbe( shot );
	return;
    }
}

// Partner to getFollowUpShot. Assists with recursive hunting for parts of the ship.
bool GamblerPlayerV2::search( int row, int col, int rowDelta, int colDelta, int shot[], int rangeLeft ) {
    if( rangeLeft <= 0 ) return false;			// Out of jumps
    if( !onBoard(row, col) ) return false;		// Off board
    char result = getCellStatus( row, col );
    if( result == MISS || result == KILL ) {		// Nobody out here -- stop
	return false;
    }
    else if( getCellStatus( row, col ) == WATER ) {	// Not shot at yet
	shot[0] = row; shot[1] = col;
	return true;
    } else if( search(row+rowDelta, col+colDelta, rowDelta, colDelta, shot, rangeLeft-1) ) {
	return true;
    }
    return false;
}

// Used to determine whether there is a known injured ship (hit while chasing a different
// ship) that needs to be killed off.
bool GamblerPlayerV2::haveUnfinishedBusiness( int position[2] ) {
    for( int row=0; row<boardSize; row++ ) {
	for( int col=0; col<boardSize; col++ ) {
	    if( getCellStatus( row, col ) == HIT ) {
		position[0] = row;
		position[1] = col;
		return true;
	    }
	}
    }
    return false;
}

//***********************************************
// BOARD WEIGHING ROUTINES **********************
//***********************************************

// Recomputes board weights
void GamblerPlayerV2::reWeighBoard( int board[][MAX_BOARD_SIZE] ) {
    for( int row=0; row<boardSize; row++ ) {
	for( int col=0; col<boardSize; col++ ) {
	    board[row][col] = calcCellWeight( row, col );
	}
    }
}

// Prints board weights in grid format
void GamblerPlayerV2::printWeightedBoard( int board[][MAX_BOARD_SIZE] ) {
    int value;
    for( int row=0; row<boardSize; row++ ) {
	for( int col=0; col<boardSize; col++ ) {
	    value = board[row][col];
	    if( value < 10 )
		cout << "  ";
	    else
		cout << " ";
	    cout << value;
	}
	cout << endl;
    }
}

// Finds a cell with the max highest weighting on the board.
// Given the current code, that will be the one with the
// lowest row/col pair of all cells set at the max weight.
void GamblerPlayerV2::getMaxWeightCell( int board[][MAX_BOARD_SIZE], int shot[2] ) {
    //int maxRow=0, maxCol=0, 
    int maxWeight=-1;
    for( int row=0; row<boardSize; row++ ) {
	for( int col=0; col<boardSize; col++ ) {
	    if( board[row][col] > maxWeight ) {
		shot[0] = row;
		shot[1] = col;
		maxWeight = board[row][col];
	    }
	}
    }
}

// Used to calculate what a cell's weight should be.
int GamblerPlayerV2::calcCellWeight( int row, int col ) {
    // Do a bit of seatbelt checking -- off-board => -1
    if( ! onBoard(row, col) ) return -1;

    int weight = 0;
    for( int length=SHIP_MIN_LENGTH; length<=SHIP_MAX_LENGTH; length++ ) {
	weight += calcCellWeightVert( row, col, length );
	weight += calcCellWeightHoriz( row, col, length );
    }

    return weight;
}

// Used to calculate a cell's vertical weight for various possible ship lengths.
// Assistant to calcCellWeight( int, int ) above.
int GamblerPlayerV2::calcCellWeightVert( int row, int col, int length ) {
    int weight = 0;
    char status;

    // Do vertical calculation
    int low=row; 
    while( low>=0 && row-low<length ) {
	status = getCellStatus( low, col );
	if( status == KILL || status == MISS )
	    break;	// Blocked
	low--;
    }
    
    int high=row;
    while( high<boardSize && high-row<length ) {
	status = getCellStatus( high, col );
	if( status == KILL || status == MISS )
	    break;	// Blocked
	high++;
    }
    if( high-low >= length ) {	// A ship could fit here
	weight += high-low - length;
    }

    return weight;
}

// Used to calculate a cell's horizontal weight for various possible ship lengths.
// Assistant to calcCellWeight( int, int ) above.
int GamblerPlayerV2::calcCellWeightHoriz( int row, int col, int length ) {
    int weight = 0;
    char status;

    // Do horizontal calculation
    int low=col, high=col;
    while( low>=0 && col-low<length ) {
	status = getCellStatus( row, low );
	if( status == KILL || status == MISS ) 
	    break;	// Blocked
	low--;
    }
    while( high<boardSize && high-col<length ) {
	status = getCellStatus( row, high );
	if( status == KILL || status == MISS )
	    break;	// Blocked
	high++;
    }
    if( high-low >= length ) {	// A ship could fit here
	weight += high-low - length;
    }

    return weight;
}

//***********************************************
// MISCELLANEOUS OTHER ROUTINES *****************
//***********************************************

bool GamblerPlayerV2::onBoard( int row, int col ) {
    return row>=0 && col>=0 && row<boardSize && col<boardSize; 
}

// Think C/C++ macro. Just to avoid typing the whole mess in
// every time!
char GamblerPlayerV2::getCellStatus( int row, int col ) {
    return board[row][col];
}

