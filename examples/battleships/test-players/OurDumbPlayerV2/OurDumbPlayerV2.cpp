#include <iostream>
#include <cstdio>
//I added
#include <stdlib.h>

#include "OurDumbPlayerV2.h"

/**
 * @brief Constructor that initializes any inter-round data structures.
 * @param boardSize Indication of the size of the board that is in use.
 *
 * The constructor runs when the AI is instantiated (the object gets created)
 * and is responsible for initializing everything that needs to be initialized
 * before any of the rounds happen. The constructor does not get called 
 * before rounds; newRound() gets called before every round.
 */
OurDumbPlayerV2::OurDumbPlayerV2( int boardSize )
    :PlayerV2(boardSize)
{
    // Could do any initialization of inter-round data structures here.
}

/**
 * @brief Destructor placeholder.
 * If your code does anything that requires cleanup when the object is
 * destroyed, do it here in the destructor.
 */
OurDumbPlayerV2::~OurDumbPlayerV2( ) {}

/*
 * Private internal function that initializes a MAX_BOARD_SIZE 2D array of char to water.
 */
void OurDumbPlayerV2::initializeBoard() {
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
Message OurDumbPlayerV2::getMove() {  
  	lastCol = lastCol + 2;
    if( lastCol >= boardSize ) {
	lastCol = 0;
	lastRow++;
    }
    if( lastRow >= boardSize ) {
	lastCol = 0;
	lastRow = 0;
    }

    Message result( SHOT, lastRow, lastCol, "Bang", None, 1 );
    return result;
}

/**
 * @brief Tells the AI that a new round is beginning.
 * The AI show reinitialize any intra-round data structures.
 */
void OurDumbPlayerV2::newRound() {
    /* DumbPlayer is too simple to do any inter-round learning. Smarter players 
     * reinitialize any round-specific data structures here.
     */
	
	
	
	this->placeRow=0;
	this->placeCol=0;
    this->lastRow = 0;
    this->lastCol = -1;
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
Message OurDumbPlayerV2::placeShip(int length) {
    char shipName[10];
    // Create ship names each time called: Ship0, Ship1, Ship2, ...
    snprintf(shipName, sizeof shipName, "Ship%d", numShipsPlaced);

	//puts ship0 etc into shipName


    // parameters = mesg type (PLACE_SHIP), row, col, a string, direction (Horizontal/Vertical)
	int randomNum = 0;
	randomNum = rand() % 1;
	
	//int vertOrHor = 0;
	//randomAngle = rand() % 2;
	//char vertOrHoriz = " ";
	
	if(randomNum == 0){
		switch(numShipsPlaced){
			case 0:
				placeRow = boardSize-1;
				placeCol = 0;
				dir = Horizontal;
				break;
			case 1:
				placeRow = (boardSize-1)-length;
				placeCol = boardSize-1;
				dir = Vertical;
				break;
			case 2:
				placeRow = (boardSize-2)-length;
				placeCol = 0;
				dir = Vertical;
				break;
			case 3:
				placeRow = (boardSize-1)-length;
				placeCol = (boardSize-(boardSize/2));
				dir = Vertical;
				break;
			case 4:
				placeRow = 0;
				placeCol = (boardSize-1)-length;
				dir = Horizontal;
				break;
			case 5:
				placeRow = (boardSize-2)-length;
				placeCol = (boardSize/2)-length;
				dir = Horizontal;
				break;
		}
	}
	
	/* //Code to beat Dumb Player
	if(randomNum == 0){
		switch(numShipsPlaced){
			case 0:
				placeRow = boardSize-1;
				placeCol = (boardSize-1) - length;
				dir = Horizontal;
				break;
			case 1:
				placeRow = boardSize-2;
				placeCol = (boardSize-1)-length;
				dir = Horizontal;
				break;
			case 2:
				placeRow = boardSize-3;
				placeCol = (boardSize-1)-length;
				dir = Horizontal;
				break;
			case 3:
				placeRow = boardSize-4;
				placeCol = (boardSize-1)-length;
				dir = Horizontal;
				break;
			case 4:
				placeRow = boardSize-5;
				placeCol = (boardSize-1)-length;
				dir = Horizontal;
				break;
			case 5:
				placeRow = boardSize-6;
				placeCol = (boardSize-1)-length;
				dir = Horizontal;
				break;
		}
	}
	*/
	Message response( PLACE_SHIP,placeRow,placeCol,shipName,dir,length);
	
		
		
	
	
		
	//response.setCol(0);
	
	
			
		
    numShipsPlaced++;

    return response;
}

/**
 * @brief Updates the AI with the results of its shots and where the opponent is shooting.
 * @param msg Message specifying what happened + row/col as appropriate.
 */
void OurDumbPlayerV2::update(Message msg) {
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

