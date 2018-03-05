#include <iostream>
#include <cstdio>
#include <stdlib.h>
#include <time.h>
#include <vector>

#include "conio.h"
#include "Bassplayer.h"

using namespace conio;

/**
 * @brief Constructor that initializes any inter-round data structures.
 * @param boardSize Indication of the size of the board that is in use.
 *
 * The constructor runs when the AI is instantiated (the object gets created)
 * and is responsible for initializing everything that needs to be initialized
 * before any of the rounds happen. The constructor does not get called 
 * before rounds; newRound() gets called before every round.
 */
Bassplayer::Bassplayer( int boardSize )
    :PlayerV2(boardSize)
{
	// Fills board matrix with '0's representing an empty board
    for ( int row = 0; row < boardSize; ++row ) {
    	for ( int col = 0; col < boardSize; ++col ) {
    		boardMatrix[row][col] = 0;
    	}
    }

    // Fills attack option board with '0's
    for ( int row = 0; row < boardSize; ++row ) {
        for ( int col = 0; col < boardSize; ++col ) {
            board[row][col] = 0;
        }
    }

    shipPlaceCount = 0;
    attackCount = 0;
    twoShotsAgoRow = 0;
    twoShotsAgoCol = 0;
}

/**
 * @brief Destructor placeholder.
 * If your code does anything that requires cleanup when the object is
 * destroyed, do it here in the destructor.
 */
Bassplayer::~Bassplayer( ) {}

/*
 * Private internal function that initializes a MAX_BOARD_SIZE 2D array of char to water.
 */
void Bassplayer::initializeBoard() {
    for(int row=0; row<boardSize; row++) {
	    for(int col=0; col<boardSize; col++) {
	        this->board[row][col] = WATER;
	    }
    }
}


/**
 * @brief Specifies the AI's shot choice and returns the information to the caller.
 * @return Message The most important parts of the returned message are 
 * the row and column values. 
 *
 * See the Message class documentation for more information on the 
 * Message constructor.
 */
Message Bassplayer::getMove() {
    /*lastCol++;
    if( lastCol >= boardSize ) {
	lastCol = 0;
	lastRow++;
    }
    if( lastRow >= boardSize ) {
	lastCol = 0;
	lastRow = 0;
    }*/
    int rowToHit = 1;
    int colToHit = 1;
    bool foundHit = false;

    if ( attackCount == 0 ) {
        rowToHit = rand() % boardSize;
        colToHit = rand() % boardSize;
    }

    else {
        if ( board[lastRow][lastCol] == HIT ) {

            // Right
            if ( board[lastRow][lastCol + 1] == WATER && lastCol + 1 < boardSize ) {
                rowToHit = lastRow;
                colToHit = lastCol + 1;
            }
            // Up
            else if ( board[lastRow - 1][lastCol] == WATER && lastRow - 1 >= 0 ) {
                rowToHit = lastRow - 1;
                colToHit = lastCol;
            }
            // Down
            else if ( board[lastRow + 1][lastCol] == WATER && lastRow + 1 < boardSize ) {
                rowToHit = lastRow + 1;
                colToHit = lastCol;
            }
            // Left
            else if ( board[lastRow][lastCol - 1] == WATER && lastCol - 1 >= 0 ) {
                rowToHit = lastRow;
                colToHit = lastCol - 1;
            }
        }    

        else {
            for ( int row = 0; row < boardSize; ++row ) {
                for ( int col = 0; col < boardSize; ++col ) {
                    // Tries to find spots that have been hits
                    if ( board[row][col] == HIT ) {
                        foundHit = true;
                        // Right
                        if ( board[row][col + 1] == WATER && lastCol + 1 < boardSize ) {
                            rowToHit = row;
                            colToHit = col + 1;
                        }
                        // Up
                        else if ( board[row - 1][col] == WATER && lastRow - 1 >= 0 ) {
                            rowToHit = row - 1;
                            colToHit = col;
                        }
                        // Down
                        else if ( board[row + 1][col] == WATER && lastRow + 1 < boardSize ) {
                            rowToHit = row + 1;
                            colToHit = col;
                        }
                        // Left
                        else if ( board[row][col - 1] == WATER && lastCol - 1 >= 0 ) {
                            rowToHit = row;
                            colToHit = col - 1;
                        }
                    }
                }
            }
            if ( ! foundHit ) {
                rowToHit = rand() % boardSize;
                colToHit = rand() % boardSize;

                while ( board[rowToHit][colToHit] != WATER ) {
                    rowToHit = rand() % boardSize;
                    colToHit = rand() % boardSize;
                }
            } 
        }
    }
    ++attackCount;
    lastRow = rowToHit;
    lastCol = colToHit;
/*

            // Randomly choose either right, left, top, or bottom around last hit
            int randomNum = rand() % 3;

            switch ( randomNum ) {
                case 0:
                    // Try to the right
                    rowToHit = lastRow;
                    colToHit = lastCol + 1;
                    break;
                case 1:
                    // Try above
                    rowToHit = lastRow - 1;
                    colToHit = lastCol;
                    break;
                case 2:
                    // Try to the left
                    rowToHit = lastRow;
                    colToHit = lastCol - 1;
                    break;
                case 3:
                    // Try below
                    rowToHit = lastRow + 1;
                    colToHit = lastCol;
                    break;
            }
        }
    }

    //int right, left, up, down;

    // If previous shot was a hit
    if ( board[lastRow][lastCol] == 2 ) {
        attackCoords.push_back()
        while ( board[rowToHit][colToHit] != 0 ) { // While shot attempt is valid
            
            // Randomly choose either right, left, top, or bottom around last hit
            int randomNum = rand() % 3;

            switch ( randomNum ) {
                case 0:
                    // Try to the right
                    rowToHit = lastRow;
                    colToHit = lastCol + 1;
                    break;
                case 1:
                    // Try above
                    rowToHit = lastRow - 1;
                    colToHit = lastCol;
                    break;
                case 2:
                    // Try to the left
                    rowToHit = lastRow;
                    colToHit = lastCol - 1;
                    break;
                case 3:
                    // Try below
                    rowToHit = lastRow + 1;
                    colToHit = lastCol;
            }
        }   
    }

    else {
        rowToHit = rand() % boardSize;
        colToHit = rand() % boardSize;

        while ( board[rowToHit][colToHit] != 0 ) {
            rowToHit = rand() % boardSize;
            colToHit = rand() % boardSize;
        }
    }

    for ( int row = 0; row < boardSize; ++row ) {
        for ( int col = 0; col < boardSize; ++col ) {
            // Tries to find spots that have been hits (represented by 2)
            if ( board[row][col] == 2 ) {

                // Get contents of all adjacent locations
                right = board[row][col + 1];
                up = board[row - 1][col];
                left = board[row][col - 1];
                down = board[row + 1][col];

                // Check far right possibilities
                if ( right == 2 ) {
                    right = board[row][col + 2];
                    if ( right == 2 ) {
                        right = board[row][col + 3];
                        if ( right == 2 ) {
                            colToHit = col + 4;
                            rowToHit = row;
                        }

                        else if ( right == 1 ) {
                            // Check far left possibilities
                            if ( left == 2 ) {
                                left = board[row][col - 2];
                                if ( left == 2 ) {
                                    left = board[row][col - 3];
                                    if ( left == 2 ) {
                                        colToHit = col - 4;
                                        rowToHit = row;
                                    }
                                }
                            }
                        }
                    }

                    // Immediately jumps to checking leftward values
                    else if ( right == 1 ) {
                        if ( left == 2 ) {
                            left = board[row][col - 2];
                            if ( left == 2 ) {
                                left = board[row][col - 3];
                                if ( left == 2 ) {
                                    colToHit = col - 4;
                                    rowToHit = row;
                                }
                            }
                        }

                        else if ( left == 1 ) {
                            // Checks up possibilities
                            if ( up == 2 ) {
                                up = board[row - 2][col];
                                if ( up == 2 )  {
                                    up = board[row - 3][col];
                                    if ( up == 2 ) {
                                        rowToHit = row - 4;
                                        colToHit = col;
                                    }
                                }
                            }
                        }
                    }
                }

                // Checks far left possibilities
                else if ( right == 1 ) {
                    if ( left == 2 ) {
                        left = board[row][col - 2];
                        if ( left == 2 ) {
                            left = board[row][col - 3];
                            if ( left == 2 ) {
                                colToHit = col - 4;
                                rowToHit = row;
                            }
                        }
                    }

                    else if ( left == 1 ) {
                        // Check above possibilities
                        if ( up == 2 ) {
                            up = board[row - 2][col];
                            if ( up == 2 )  {
                                up = board[row - 3][col];
                                if ( up == 2 ) {
                                    rowToHit = row - 4;
                                    colToHit = col;
                                }
                            }
                        }

                        // Checks below possibilities
                        else if ( up == 1 ) {
                            if ( down == 2 ) {
                                down = board[row + 2][col];
                                if ( down == 2 ) {
                                    down = board[row + 3][col];
                                    if ( down == 2 ) {
                                        rowToHit = row + 4;
                                        colToHit = col;
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    board[rowToHit][colToHit] = 1;
    lastRow = rowToHit;
    lastCol = colToHit;

*/

    //              type,    row ,  col
    Message result( SHOT, rowToHit, colToHit, "Bang", None, 1 );
    return result;
}

/**
 * @brief Tells the AI that a new round is beginning.
 * The AI show reinitialize any intra-round data structures.
 */
void Bassplayer::newRound() {
    /* DumbPlayer is too simple to do any inter-round learning. Smarter players 
     * reinitialize any round-specific data structures here.
     */
    // Fills board matrix with '0's representing an empty board
    for ( int row = 0; row < boardSize; ++row ) {
        for ( int col = 0; col < boardSize; ++col ) {
            boardMatrix[row][col] = 0;
        }
    }

    // Fills attack option board with '0's
    for ( int row = 0; row < boardSize; ++row ) {
        for ( int col = 0; col < boardSize; ++col ) {
            board[row][col] = 0;
        }
    }

    this->lastRow = 0;
    this->lastCol = -1;
    this->numShipsPlaced = 0;
    shipPlaceCount = 0;
    attackCount = 0;

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
Message Bassplayer::placeShip(int length) {
    char shipName[10];
    // Create ship names each time called: Ship0, Ship1, Ship2, ...
    snprintf(shipName, sizeof shipName, "Ship%d", numShipsPlaced);

    // Seeds random number generator
    srand (time(NULL));

    // Creates vector to hold rows where a ship has been placed
    //int rowsUsed[6];
    //vector<int> rowsUsed(6);

    bool placeOK = true;

    int rowToBePlaced = 0;
    
    // Generate random row for ships to be placed in
    rowToBePlaced = rand() % boardSize;

    // Checks to see if any column in that row has a ship on it
    for ( int col = 0; col < boardSize; ++col ) {
        if ( boardMatrix[rowToBePlaced][col] == 1 ) {
            placeOK = false;
        }
    }

    // If previous ship placement doesn't work, then try again
    while ( ! placeOK ) {
        placeOK = true;
        rowToBePlaced = rand() % boardSize;

        for ( int col = 0; col < boardSize; ++col ) {
            if ( boardMatrix[rowToBePlaced][col] ) {
                placeOK = false;
            }
        }
    }

    // Picks random column within selected row to place ship horizontally to the right
    int colToBePlaced = rand() % boardSize - length;

    if ( colToBePlaced < 0 ) {
        colToBePlaced += length;
    }

    // Places a 1 on boardMatrix to represent a ship resides there
    for ( int col = colToBePlaced; col < colToBePlaced + length; ++col ) {
        boardMatrix[rowToBePlaced][col] = 1;
    }

    /*do {
	    // Generate random row for ships to be placed in
	    rowToBePlaced = rand() % boardSize-1;

	    // Check if row generated has already been used
		if ( boardMatrix[rowToBePlaced][0] == 1 ) {
			placeOK = false;
		}

	    if ( placeOK ) {
	    	boardMatrix[rowToBePlaced][0] = 1;
	    }
	} while ( ! placeOK );*/

    // parameters = mesg type (PLACE_SHIP), row, col, a string, direction (Horizontal/Vertical)
    Message response( PLACE_SHIP, rowToBePlaced, colToBePlaced, shipName, Horizontal, length );
    numShipsPlaced++;

    return response;
}

/**
 * @brief Updates the AI with the results of its shots and where the opponent is shooting.
 * @param msg Message specifying what happened + row/col as appropriate.
 */
void Bassplayer::update(Message msg) {
    switch(msg.getMessageType()) {
	case HIT:
        //board[lastRow][lastCol] = 2;
	case KILL:
        //board[lastRow][lastCol] = 3;
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

