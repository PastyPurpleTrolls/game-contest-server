#include <iostream>
#include <cstdio>
#include <stdlib.h>
#include "sheep.h"
#include "defines.h"

/**
 * @brief Constructor that initializes any inter-round data structures.
 * @param boardSize Indication of the size of the board that is in use.
 *
 * The constructor runs when the AI is instantiated (the object gets created)
 * and is responsible for initializing everything that needs to be initialized
 * before any of the rounds happen. The constructor does not get called 
 * before rounds; newRound() gets called before every round.
 */
sheep::sheep( int boardSize )
    :PlayerV2(boardSize)
{
    // Could do any initialization of inter-round data structures here.
}

/**
 * @brief Destructor placeholder.
 * If your code does anything that requires cleanup when the object is
 * destroyed, do it here in the destructor.
 */
sheep::~sheep( ) {}

/*
 * Private internal function that initializes a MAX_BOARD_SIZE 2D array of char to water.
 */
void sheep::initializeBoard() {
	turn1=true;
	tempDirection=0;
	targetDirection=0;
	hitRow = 0;
	hitCol = 0;
	hit=false;
    for(int row=0; row<boardSize; row++) {
	for(int col=0; col<boardSize; col++) {
	    this->board[row][col] = WATER;
		this ->shipsOnBoard[row][col] = '~';
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
Message sheep::getMove() {
	if(!turn1){
		lastCol++;
		}
	if( lastCol >= boardSize ) {
		lastCol = 0;
		lastRow++;
	}
	if( lastRow >= boardSize ) {
		lastCol = 0;
		lastRow = 0;
	}
	turn1=false;
	Message result( SHOT, lastRow, lastCol, "Bang", None, 1 );
	return result;
										}
										
	//I tried to beat the clean player, but just kept failing, this is my sad code lol
	/*
	if(hit){ //check around the area
		if(targetDirection==0){
			if(hitRow-1 >= 0 && board[hitRow-1][hitCol]=='~'){
				tempDirection=1;
				Message result(SHOT,hitRow-1, hitCol, "Bang", None, 1);
				return result;
			}
			else if(hitCol-1 >=0 && board[hitRow][hitCol-1]=='~'){
				tempDirection=2;
				Message result(SHOT,hitRow, hitCol-1, "Bang", None, 1);
				return result;
			}
			else if((hitRow+1 <= (boardSize-1))&& board[hitRow+1][hitCol]=='~'){
				tempDirection=3;
				Message result(SHOT,hitRow+1, hitCol, "Bang", None, 1);
				return result;
			}
			else if(hitCol+1 <=0 && board[hitRow][hitCol+1]=='~'){
				tempDirection=4;
				Message result(SHOT,hitRow, hitCol+1, "Bang", None, 1);
				return result;
			}
			}
		else{
			if(targetDirection == 1){
				if(canShoot(hitRow-1, hitCol)){
					tempDirection=1;
					Message result(SHOT,hitRow-1, hitCol, "Bang", None, 1);
					return result;
				}
				else{
					tempDirection=3;
					for(int i=hitRow; i<boardSize; i++){
						if(canShoot(i,hitCol)){
							Message result(SHOT, i, hitCol, "Bang", None, 1);
							return result;
						}
					}
				}
			}
			else if(targetDirection == 2){
				if(canShoot(hitRow, hitCol-1)){
					tempDirection=2;
					Message result(SHOT,hitRow, hitCol-1, "Bang", None, 1);
					return result;
				}
				else{
					tempDirection=4;
					for(int i=hitCol; i<boardSize; i++){
						if(canShoot(hitRow,i)){
							Message result(SHOT, hitRow, i, "Bang", None, 1);
							return result;
						}
					}
				}
			}
				
			else if(targetDirection == 3){
				if(canShoot(hitRow+1, hitCol)){
					tempDirection=3;
					Message result(SHOT,hitRow+1, hitCol, "Bang", None, 1);
					return result;
				}
				else{
					tempDirection=1;
					for(int i=hitRow; i>=0; i--){
						if(canShoot(i,hitCol)){
							Message result(SHOT, i, hitCol, "Bang", None, 1);
							return result;
						}
					}
				}
			}
			else if(targetDirection==4){
				if(canShoot(hitRow, hitCol+1)){
					tempDirection=4;
					Message result(SHOT,hitRow, hitCol+1, "Bang", None, 1);
					return result;
				}
				else{
					tempDirection=2;
					for(int i=hitCol; i>=0; i--){
						if(canShoot(hitRow,i)){
							Message result(SHOT, hitRow, i, "Bang", None, 1);
							return result;
						}
					}
				}
			}	
		}
	}
	if(turn1){
		Message result(SHOT, lastRow, lastCol, "Bang", None, 1);
		turn1=false;
		return result;
	}
	else{incrementShot(lastRow, lastCol);}
	
	while(board[lastRow][lastCol] != '~'){
		incrementShot(lastRow, lastCol);
	}
	Message result(SHOT, lastRow, lastCol, "Bang",None,1);
	return result;
}

bool sheep::canShoot(int row, int col){
	if((row>=0 && row<boardSize)&&(col>=0 && col<boardSize)){
		if(board[row][col]=='~'){
			return true;
		}
	}
	return false;
}

void sheep::incrementShot(int& row, int& col){
	col+=3;
	if(col >= boardSize){
		if (col == boardSize+2){
			col = 1;
		}
		else if(col == boardSize){
			col = 2;
		}
		else if(col == boardSize+1){
			col = 0;
		}
		row++;
	}
	if(row>= boardSize){
		col = 0;
		row = 0;
	}

} 

void sheep::recheck(){
	for(int i=0; i<boardSize; i++){
		for(int j=0; j<boardSize; j++){
			if (board[i][j]=='X'){
				hitRow=i;
				hitCol=j;
				hit= true;
			}
		}
	}
}
*/
/**
 * @brief Tells the AI that a new round is beginning.
 * The AI show reinitialize any intra-round data structures.
 */
void sheep::newRound() {
    /* DumbPlayer is too simple to do any inter-round learning. Smarter players 
     * reinitialize any round-specific data structures here.
     */
    this->lastRow = 0;
    this->lastCol = 0;
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
Message sheep::placeShip(int length) {
    char shipName[10];
    // Create ship names each time called: Ship0, Ship1, Ship2, ...
    snprintf(shipName, sizeof shipName, "Ship%d", numShipsPlaced);

    // parameters = mesg type (PLACE_SHIP), row, col, a string, direction (Horizontal/Vertical)
    /*Message response( PLACE_SHIP,row,col, shipName, Horizontal, length );
    numShipsPlaced++;

    return response;*/
	bool placed = false;
	int dir = -1;
	int row =0;
	int col =0;
	while(placed == false){
		dir = rand()%2+1;  //horizonal=1, vertical=2
		if(dir == 1){        //if direction is horizontal
			row = rand()%boardSize;
			col = rand()%(boardSize-length+1);
		}
		else if(dir ==2){
			row = rand()%(boardSize-length+1);
			col = rand()%boardSize;
		}
		if(numShipsPlaced == 5){
			if(lastShip(length,row,col)){
				Message response( PLACE_SHIP, row, col, shipName, Horizontal, length);
				return response;
			}
		}
		if(canPlaceShip(length, dir, row, col)){
				numShipsPlaced++;
				placed = true;
				
		}

	}
	
	if(dir==1){
		Message response( PLACE_SHIP, row, col, shipName, Horizontal, length );
		return response;
	}
	else if (dir ==2 ){
		Message response( PLACE_SHIP, row, col, shipName, Vertical, length );
		return response;
	}
	return 0;
}
bool sheep::canPlaceShip(int shipSize, int direction, int row, int col){
    if(numShipsPlaced == 0){
	if (direction == 1){
	    for (int i = col; i < (col+shipSize); i++){
			shipsOnBoard[row][i] = '#';
	    }
	}

	else if (direction == 2){
	    for (int i = row; i < (row+shipSize); i++){
			shipsOnBoard[i][col] = '#';
	    }
			
	}
	return true;
    }
    else{ //check if random placement overlaps with current ships
		if (direction == 1){
	    	for (int i = col; i <(col+shipSize); i++){
				if(shipsOnBoard[row][i] == '#'){
		    		return false;
				}
	    	}
	    	for (int i = col; i < (col+shipSize); i++){
				shipsOnBoard[row][i] = '#';
	    	}
	    return true;
		}
		else if (direction == 2){
	    	for (int i = row; i < (row+shipSize); i++){
				if(shipsOnBoard[i][col] == '#'){
		    		return false;
				}
	    	}
	    	for (int i = row; i < (row+shipSize); i++){
				shipsOnBoard[i][col] = '#';
	    	}
	    return true;
		}
    }
    return false;
}
bool sheep::lastShip(int shipSize, int& row, int& col){
	bool spot1 = true;
	bool spot2 = true;
	int max = boardSize-1;
	for(int i=0; i<shipSize; i++){
		if(shipsOnBoard[max][i]=='#'){
			spot1=false;
		}
	}
	if(spot1 == true){
		row = max;
		col = 0;
		return true;
	}
	else{
	for(int i =(boardSize-shipSize); i<boardSize; i++){
		if(shipsOnBoard[max][i]=='#' || i==10){
			spot2=false;
		}
	}
	if(spot2==true){
		row=max;
		col=(boardSize-shipSize);
		return true;
	}
	}
	return false;
}
/**
 * @brief Updates the AI with the results of its shots and where the opponent is shooting.
 * @param msg Message specifying what happened + row/col as appropriate.
 */
void sheep::update(Message msg) {
    switch(msg.getMessageType()) {
	case HIT:
	   // board[msg.getRow()][msg.getCol()] = msg.getMessageType();
		//hitRow = msg.getRow();
		//hitCol = msg.getCol();
		//hit=true;
		//targetDirection=tempDirection;
		//break;
	case KILL:
		//hit=false;
		//recheck();
		//break;
	case MISS:
	    //board[msg.getRow()][msg.getCol()] = msg.getMessageType();
		//targetDirection=0;
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

