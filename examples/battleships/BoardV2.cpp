/**
 * @author Stefan Brandle and Jonathan Geisler
 * @date August, 2004
 * Shell for BoardV2.cpp implementations.
 * Please type in your name[s] below:
 *
 *
 */

#include <iostream>
#include <stdlib.h>

#include "BoardV2.h"
#include "defines.h"

using namespace std;

BoardV2::BoardV2(int width) {
    shipMark = 'a';
    boardSize = width;

    // Initialize the boards
    initialize(shotBoard);
    initialize(shipBoard);
}

BoardV2::BoardV2(const BoardV2& other) {
    operator=(other);	// Ask operator= to do the work.
}

void BoardV2::operator=(const BoardV2& other) {
    // Avoid setting yourself to yourself.
    if( this == &other) return;

    shipMark = other.shipMark;    
    boardSize = other.boardSize;

    for(int row=0; row<boardSize; row++) {
	for(int col=0; col<boardSize; col++) {
	    shipBoard[row][col] = other.shipBoard[row][col];
	    shotBoard[row][col] = other.shotBoard[row][col];
	}
    }
}

bool BoardV2::placeShip(int length) {
    const int MaxTries = 25;
    int row, col;
    bool horiz;

    if( length > boardSize ) return false;	// Ship too big for board

    for(int tryCount=0; tryCount<MaxTries; tryCount++) {
	chooseValues(row, col, length, horiz);
	if( positionOk(row, col, length, horiz) ) {
	    markShip(row, col, length, horiz);
	    return true;	// Successfully placed ship.
	}
    }

    return false;		// Didn't succeed in placing ship.
}

void BoardV2::chooseValues( int& row, int& col, int& length, bool& horiz ) {
    horiz = bool( rand()%2 );
    if( horiz ) {
        row = rand() % boardSize;
	col = rand() % (boardSize+1 - length);
    } else {	// vertical
	row = rand() % (boardSize+1 - length);
        col = rand() % boardSize;
    }
}

bool BoardV2::positionOk( int row, int col, int length, bool horiz  ) {
    if( horiz ) {
	for(int c=col; c<col+length; c++) {
	    if(shotBoard[row][c] == SHIP) return false;
	}
    } else {
	for(int r=row; r<row+length; r++) {
	    if(shotBoard[r][col] == SHIP) return false;
	}
    }
    return true;
}

void BoardV2::markShip( int row, int col, int length, bool horiz ) {
    if( horiz ) {
	for(int c=col; c<col+length; c++) {
	    shipBoard[row][c] = shipMark;
	    shotBoard[row][c] = SHIP;
	}
    } else {
	for(int r=row; r<row+length; r++) {
	    shipBoard[r][col] = shipMark;
	    shotBoard[r][col] = SHIP;
	}
    }

    shipMark ++;	// Increment shipMark to next avail value
}

char BoardV2::getOpponentView(int row, int col) {
    char value = shotBoard[row][col];
    switch (value) {
        case HIT:
        case MISS:
        case KILL:
    	    return value;
        default:
    	    return WATER;
    }
}

char BoardV2::getOwnerView(int row, int col) {
    if( shotBoard[row][col] == SHIP )
        return shipBoard[row][col];
    else
        return shotBoard[row][col];
}

char BoardV2::processShot(int row, int col) {
    // Ensure that row/col coordinates are valid!
    if( row<0 || row>= boardSize || col<0 || col>=boardSize ) {
	return INVALID_SHOT;
    }

    switch(shotBoard[row][col]) {
	case WATER:
	    shotBoard[row][col] = MISS;
	    return MISS;
	case MISS:
	case HIT:
	case KILL:
	    return DUPLICATE_SHOT;
	case SHIP:
	    shotBoard[row][col] = HIT;
	    if(isSunk(row,col)) {
	        markSunk(row,col);
		return KILL;
	    } else {
	        return HIT;
	    };
	default:
	    cerr << "This didn't happen!!!!" << endl
	         << shotBoard << "[" <<row<<"]["<<col<<"] had value " 
	         << shotBoard[row][col] << endl;
	    break;
    }
}

bool BoardV2::isSunk(int row, int col) {
    char mark = shipBoard[row][col];
    for(int row=0; row<boardSize; row++) {
	for(int col=0; col<boardSize; col++) {
	    if(shipBoard[row][col]==mark && shotBoard[row][col]==SHIP) {
		return false;
	    }
	}
    }
    return true;
}

void BoardV2::markSunk(int row, int col) {
    char mark = shipBoard[row][col];
    for(int row=0; row<boardSize; row++) {
	for(int col=0; col<boardSize; col++) {
	    if(shipBoard[row][col]==mark) {
	        shotBoard[row][col]=KILL;
	    }
	}
    }
}


bool BoardV2::hasWon() {
    for(int row=0; row<boardSize; row++) {
	for(int col=0; col<boardSize; col++) {
	    if(shotBoard[row][col]==SHIP) {
	    	return false;	// Found an unsunk bit of SHIP, haven't won.
	    }
	}
    }
    return true;	// In absence of evidence to contrary, have won.
}

void BoardV2::initialize(char board[MaxBoardSize][MaxBoardSize]) {
    for(int row=0; row<MaxBoardSize; row++)
        for(int col=0; col<MaxBoardSize; col++)
            board[row][col] = WATER;
}

