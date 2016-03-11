/**
 * @author Stefan Brandle and Jonathan Geisler
 * @date August, 2004
 * Shell for BoardV3.cpp implementations.
 * Please type in your name[s] below:
 *
 *
 */

#include <iostream>
#include <stdlib.h>

#include "BoardV3.h"
#include "defines.h"

using namespace std;

BoardV3::BoardV3(int width) {
    shipMark = 'a';
    boardSize = width;

    // Initialize the boards
    initialize(shotBoard);
    initialize(shipBoard);
}

BoardV3::BoardV3(const BoardV3& other) {
    operator=(other);	// Ask operator= to do the work.
}

void BoardV3::operator=(const BoardV3& other) {
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

bool BoardV3::placeShip(int row, int col, int length, Direction dir) {

    if( positionOk(row, col, length, dir==Horizontal) ) {
	markShip(row, col, length, dir==Horizontal);
	return true;		// Successfully placed ship.
    } else {
	return false;		// Didn't succeed in placing ship.
    }
}

bool BoardV3::positionOk( int row, int col, int length, bool horiz  ) {
    if( horiz ) {
	// If starting point off board, of would go off board, instant false.
	if( row<0 || row>=boardSize || col<0 || col+length-1>=boardSize ) {
	    cerr << "positionOk: horizontal position invalid" << endl;
	    return false;
	}

	for(int c=col; c<col+length; c++) {
	    if(shotBoard[row][c] == SHIP) {
		cerr << "positionOk: horizontal collision at row=" << row << ", col="  << c << endl;
		return false;
	    }
	}
    } else {
	// If starting point off board, of would go off board, instant false.
	if( col<0 || col>=boardSize || row<0 || row+length-1>=boardSize ) {
	    cerr << "positionOk: vertical position invalid" << endl;
	    return false;
	}

	for(int r=row; r<row+length; r++) {
	    if(shotBoard[r][col] == SHIP) {
		cerr << "positionOk: horizontal collision at row=" << r << ", col="  << col << endl;
		return false;
	    }
	}
    }
    return true;
}

void BoardV3::markShip( int row, int col, int length, bool horiz ) {
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

char BoardV3::getOpponentView(int row, int col) {
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

char BoardV3::getOwnerView(int row, int col) {
    if( shotBoard[row][col] == SHIP )
        return shipBoard[row][col];
    else
        return shotBoard[row][col];
}

char BoardV3::getShipMark(int row, int col) {
    return shipBoard[row][col];
}

char BoardV3::processShot(int row, int col) {
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
    return MISS;
}

bool BoardV3::isSunk(int row, int col) {
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

void BoardV3::markSunk(int row, int col) {
    char mark = shipBoard[row][col];
    for(int row=0; row<boardSize; row++) {
	for(int col=0; col<boardSize; col++) {
	    if(shipBoard[row][col]==mark) {
	        shotBoard[row][col]=KILL;
	    }
	}
    }
}


bool BoardV3::hasWon() {
    for(int row=0; row<boardSize; row++) {
	for(int col=0; col<boardSize; col++) {
	    if(shotBoard[row][col]==SHIP) {
	    	return false;	// Found an unsunk bit of SHIP, haven't won.
	    }
	}
    }
    return true;	// In absence of evidence to contrary, have won.
}

void BoardV3::initialize(char board[MaxBoardSize][MaxBoardSize]) {
    for(int row=0; row<MaxBoardSize; row++)
        for(int col=0; col<MaxBoardSize; col++)
            board[row][col] = WATER;
}

