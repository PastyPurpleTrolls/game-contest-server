#include <iostream>
#include <cstdio>

#include "conio.h"
#include "Calahart.h"
#include <cstdlib>
#include <ctime>
#include <vector>
#include <unistd.h>
using namespace conio;

/**
 * @brief Constructor that initializes any inter-round data structures.
 * @param sizeOfBoard Indication of the size of the board that is in use.
 *
 * The constructor runs when the AI is instantiated (the object gets created)
 * and is responsible for initializing everything that needs to be initialized
 * before any of the rounds happen. The constructor does not get called 
 * before rounds; newRound() gets called before every round.
 */
Calahart::Calahart( int boardSize )
    :PlayerV2(boardSize)
{
	trackingMode = false;
	sizeOfBoard = boardSize;
	// Could do any initialization of inter-round data structures here.
}

/**
 * @brief Destructor placeholder.
 * If your code does anything that requires cleanup when the object is
 * destroyed, do it here in the destructor.
 */
Calahart::~Calahart( ) {}

/*
 * Private internal function that initializes a sizeOfBoard 2D array of char to water.
 */
void Calahart::initializeBoard() {
    for(int row=0; row<sizeOfBoard; row++) {
		for(int col=0; col<sizeOfBoard; col++) {
			this->board[row][col] = WATER;
			this->probBoard[row][col] = WATER;
			this->oppoBoard[row][col] = WATER;
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
Message Calahart::getMove() {
	for(int r = 0; r < sizeOfBoard; r++){
		for(int c = 0; c < sizeOfBoard; c++){
			probBoard[r][c] = cellProb(r,c,rand()%3+3,this->oppoBoard);
		}
    }

	pickHighProb( lastRow, lastCol, probBoard);	
    

    Message result( SHOT, lastRow, lastCol, "Bang", None, 1 );
    return result;
}

/**
 * @brief Tells the AI that a new round is beginning.
 * The AI show reinitialize any intra-round data structures.
 */
void Calahart::newRound() {
    /* DumbPlayer is too simple to do any inter-round learning. Smarter players 
     * reinitialize any round-specific data structures here.
     */
    this->lastRow = 0;
    this->lastCol = -1;
    this->numShipsPlaced = 0;

    this->initializeBoard();


    for(int r = 0; r < sizeOfBoard; r++){
		for(int c = 0; c < sizeOfBoard; c++){
			probBoard[r][c] = cellProb(r,c,rand()%3+3,this->oppoBoard);
		}
    }


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
Message Calahart::placeShip(int length) {
    char shipName[10];
    // Create ship names each time called: Ship0, Ship1, Ship2, ...
    snprintf(shipName, sizeof shipName, "Ship%d", numShipsPlaced);

	numShipsPlaced++;

	int row, col;
	Direction dir;

	row = -1;
	col = -1;
	dir = Direction(0);
	while(row == -1 || col == -1 || dir == 0){
		int placementChoice = rand()%17+1;

		switch(placementChoice){
			case 1:
			case 2:
				probPlacement( length, row, col, dir );
				break;
			case 3:
				randomPlacement( length, row, col, dir );
				break;
			case 4:
			case 5:
			case 6:
			case 7:
			case 8:
			case 9:
			case 10:
			case 11:
			case 12:
			case 13:
				cornerPlacement( length, row, col, dir );
				break;
			case 14:
			case 15:
			case 16:
			case 17:
				borderPlacement( length, row, col, dir );
				break;
		}
	}

	drawShip(row, col, length, dir);
	Message response( PLACE_SHIP, row, col, shipName, dir, length ); // parameters = mesg type (PLACE_SHIP), row, col, a string, direction (Horizontal/Vertical)

	return response;
}

void Calahart::probPlacement( int length, int &row, int &col, Direction &dir ) {
	
    for(int r = 0; r < sizeOfBoard; r++){
		for(int c = 0; c < sizeOfBoard; c++){
			myProb[r][c] = cellProb(r,c,length,this->board);
		}
    }
	
	pickLowProb( row, col, myProb );

	dir = Direction(rand()%2+1);

	if(!(checkShipValid(row, col, length, dir))){
		row = -1;
		col = -1;
		dir = Direction(0);
	}

}

void Calahart::randomPlacement( int length, int &row, int &col, Direction &dir ) {

	row = rand()%sizeOfBoard;
	col = rand()%sizeOfBoard;
	dir = Direction(rand()%2+1);

	if(!(checkShipValid(row, col, length, dir))){
		row = -1;
		col = -1;
		dir = Direction(0);
	}

}

void Calahart::cornerPlacement( int length, int &row, int &col, Direction &dir ) {

	row = rand()%3+1;
	switch (row){
		case 1:
		case 2:
			row = 0;
			dir = Direction(rand()%2+1);
		case 3:
			row = sizeOfBoard-1;
			dir = Direction(2);
	}

	if(row == 0 || row == sizeOfBoard-1){
		dir = Direction(1);
		col = rand()%sizeOfBoard;
	}else{
		col = rand()%2;
		if(col == 1){
			col = sizeOfBoard-1;
			dir = Direction(2);
		}else{
			dir = Direction(rand()%2+1);
		}
	}
		
	if(!(checkShipValid(row, col, length, dir))){
		row = -1;
		col = -1;
		dir = Direction(0);
	}

}

void Calahart::borderPlacement( int length, int &row, int &col, Direction &dir ) {

	row = rand()%sizeOfBoard;

	if(row == 0 || row == sizeOfBoard-1){
		dir = Direction(1);
		col = rand()%sizeOfBoard;
	}else{
		col = rand()%2;
		if(col == 1){
			col = sizeOfBoard-1;
			dir = Direction(2);
		}else{
			dir = Direction(rand()%2+1);
		}
	}
		
	if(!(checkShipValid(row, col, length, dir))){
		row = -1;
		col = -1;
		dir = Direction(0);
	}

}

void Calahart::pickLowProb( int &row, int &col, char b[MAX_BOARD_SIZE][MAX_BOARD_SIZE] ){
	int lowestNum= 100;

	for(int r = 0; r < sizeOfBoard; ++r){
		for(int c = 0; c < sizeOfBoard; ++c){
			if(b[r][c] < lowestNum){
				lowestNum = b[r][c];
			}
		}
	}

	vector< vector<int> > probVector;
	int count = 0;

	for(int r = 0; r < sizeOfBoard; ++r){
		for(int c = 0; c < sizeOfBoard; ++c){
			if(b[r][c] == lowestNum){
				vector<int> cell;
				cell.push_back(r);
				cell.push_back(c);
				probVector.push_back(cell);
				count++;
			}
		}
	}

	int tmpNum = rand()%count;
	row = probVector[tmpNum][0];
	col = probVector[tmpNum][1];


}

void Calahart::pickHighProb( int &row, int &col, char b[MAX_BOARD_SIZE][MAX_BOARD_SIZE] ){
	int highestNum = -100;

	for(int r = 0; r < sizeOfBoard; ++r){
		for(int c = 0; c < sizeOfBoard; ++c){
			if(b[r][c] > highestNum){
				highestNum = b[r][c];
			}
		}
	}

	vector< vector<int> > probVector;
	int count = 0;

	for(int r = 0; r < sizeOfBoard; ++r){
		for(int c = 0; c < sizeOfBoard; ++c){
			if(b[r][c] == highestNum){
				vector<int> cell;
				cell.push_back(r);
				cell.push_back(c);
				probVector.push_back(cell);
				count++;
			}
		}
	}

	int tmpNum = rand()%count;
	row = probVector[tmpNum][0];
	col = probVector[tmpNum][1];


}

void Calahart::drawShip(int row, int col, int length, Direction dir){
	for(int i = 0; i <= length; ++i){
		if(dir == 1){
			this->board[row][col+i] = SHIP;
		}else{
			this->board[row+i][col] = SHIP;
		}
	}
}

bool Calahart::checkShipValid(int row, int col, int length, Direction dir){

	for(int inc = 0; inc < length; ++inc){
		if(dir == 1){
			if(col + inc < sizeOfBoard && col + inc >= 0){
				if(this->board[row][col+inc] == WATER){
					continue;
				}else{
					return false;
				}
			}else{
				return false;
			}
		}else{
			if(row + inc < sizeOfBoard && row + inc >= 0){
				if(this->board[row+inc][col] == WATER){
					continue;
				}else{
					return false;
				}
			}else{
				return false;
			}
		}
	}

	return true;

}


/**
 * @brief Updates the AI with the results of its shots and where the opponent is shooting.
 * @param msg Message specifying what happened + row/col as appropriate.
 */

void Calahart::update(Message msg) {
    switch(msg.getMessageType()) {
	case HIT:
		trackingMode = true;
	    oppoBoard[msg.getRow()][msg.getCol()] = msg.getMessageType();
	    break;
	case KILL:
		trackingMode = false;
	    oppoBoard[msg.getRow()][msg.getCol()] = msg.getMessageType();
	    break;
	case MISS:
	    oppoBoard[msg.getRow()][msg.getCol()] = msg.getMessageType();
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

int Calahart::cellProb(int row, int col, int length, char myBoard[MAX_BOARD_SIZE][MAX_BOARD_SIZE]){
	int count = 0;
	
	int startRow, startCol;
	//Checks Vertical
	//FIX ME: HAVE NOT CHECKED FOR HITS WELL...
	if(myBoard[row][col] != WATER){
		return 0;
	}
	if(trackingMode == true) {
		if(row == 9){
			if(col == 9){
				if( myBoard[row-1][col] != HIT && myBoard[row][col-1] != HIT){
					return 0;
				}
				else if((row-1 == lastRow && col == lastCol) || (row == lastRow && col-1 == lastCol)){
					count += 2;
				}
				else{
					count++;
				}
			}else if(col == 0){
				if( myBoard[row-1][col] != HIT && myBoard[row][col+1] != HIT){
					return 0;
				}
				else if((row-1 == lastRow && col == lastCol) || (row == lastRow && col+1 == lastCol)){
					count += 2;
				}
				else{
					count++;
				}
			}else{
				if( myBoard[row-1][col] != HIT && myBoard[row][col+1] != HIT && myBoard[row][col-1] != HIT){
					return 0;
				}
				else if((row-1 == lastRow && col == lastCol) || (row == lastRow && col-1 == lastCol) || (row == lastRow && col+1 == lastCol)){
					count += 2;
				}
				else{
					count++;
				}
			}
		}else if( row == 0 ){
			if(col == 9){
				if( myBoard[row+1][col] != HIT && myBoard[row][col-1] != HIT){
					return 0;
				}
				else if((row+1 == lastRow && col == lastCol) || (row == lastRow && col-1 == lastCol)){
					count += 2;
				}
				else{
					count++;
				}
			}else if(col == 0){
				if( myBoard[row+1][col] != HIT && myBoard[row][col+1] != HIT){
					return 0;
				}
				else if((row+1 == lastRow && col == lastCol) || (row == lastRow && col+1 == lastCol)){
					count += 2;
				}
				else{
					count++;
				}
			}else{
				if( myBoard[row+1][col] != HIT && myBoard[row][col+1] != HIT && myBoard[row][col-1] != HIT){
					return 0;
				}
				else if((row+1 == lastRow && col == lastCol) || (row == lastRow && col-1 == lastCol) || (row == lastRow && col+1 == lastCol)){
					count += 2;
				}
				else{
					count++;
				}
			}
		}else{
			if(col == 9){
				if(myBoard[row+1][col] != HIT && myBoard[row-1][col] != HIT && myBoard[row][col-1] != HIT){
					return 0;
				}
				else if((row+1 == lastRow && col == lastCol) || (row-1 == lastRow && col == lastCol) || (row == lastRow && col-1 == lastCol)){
					count += 2;
				}
				else{
					count++;
				}
			}else if(col == 0){
				if(myBoard[row+1][col] != HIT && myBoard[row-1][col] != HIT && myBoard[row][col+1] != HIT){
					return 0;
				}
				else if((row+1 == lastRow && col == lastCol) || (row-1 == lastRow && col == lastCol) || (row == lastRow && col+1 == lastCol)){
					count += 2;
				}
				else{
					count++;
				}
			}else{
				if(myBoard[row+1][col] != HIT && myBoard[row-1][col] != HIT && myBoard[row][col+1] != HIT && myBoard[row][col-1] != HIT){
					return 0;
				}
				else if((row+1 == lastRow && col == lastCol) || (row-1 == lastRow && col == lastCol) || (row == lastRow && col-1 == lastCol) || (row == lastRow && col+1 == lastCol)){
					count += 2;
				}
				else{
					count++;
				}
			}
		}
	}
	if(row <= (sizeOfBoard-length)){
		startRow = row+(length-1);
		for(int startCell = startRow; startCell >= row; --startCell){ 
			for(int shipPeice = 0; shipPeice < length; shipPeice++){
				if( startCell-shipPeice >= 0 ){
					if( myBoard[startCell-shipPeice][col] == WATER ){
						if(shipPeice == length - 1){
							count++;
						}
					}else if( myBoard[startCell-shipPeice][col] == HIT ){
						count++;
					}else{
						break;
					}
				}else{
					break;
				}
			}
		}
	}else{
		startRow = row-(length-1);
		for(int startCell = startRow; startCell <= row; ++startCell){ 
			for(int shipPeice = 0; shipPeice < length; shipPeice++){
				if( startCell+shipPeice < sizeOfBoard ){
					if( myBoard[startCell+shipPeice][col] == WATER ){
						if(shipPeice == length - 1){
							count++;
						}
					}else if( myBoard[startCell+shipPeice][col] == HIT ){
						count++;
					}else{
						break;
					}
				}else{
					break;
				}
			}
		}
	}


	//Checks Horizontal
	if(col <= (sizeOfBoard-length)){
		startCol = col+(length-1);
		for(int startCell = startCol; startCell >= col; --startCell){ 
			for(int shipPeice = 0; shipPeice < length; shipPeice++){
				if( startCell-shipPeice >= 0 ){
					if( myBoard[row][startCell-shipPeice] == WATER ){
						if(shipPeice == length - 1){
							count++;
						}
					}else if( myBoard[row][startCell-shipPeice] == HIT ){
						count++;
					}else{
						break;
					}
				}else{
					break;
				}
			}
		}
	}else{
		startCol = col-(length-1);
		for(int startCell = startCol; startCell <= col; ++startCell){ 
			for(int shipPeice = 0; shipPeice < length; shipPeice++){
				if( startCell+shipPeice < sizeOfBoard ){
				    if( myBoard[row][startCell+shipPeice] == WATER ){
						if(shipPeice == length - 1){
							count++;
						}
					}else if( myBoard[row][startCell+shipPeice] == HIT ){
						count++;
					}else{
						break;
					}
				}else{
					break;
				}
			}
		}
	}
	return count;
}
