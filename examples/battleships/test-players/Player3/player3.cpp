#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <ctime>

#include "conio.h"
#include "OttoWhitePlayer.h"

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
OttoWhitePlayer::OttoWhitePlayer( int boardSize )
    :PlayerV2(boardSize)
{
    // Could do any initialization of inter-round data structures here.
}

/**
 * @brief Destructor placeholder.
 * If your code does anything that requires cleanup when the object is
 * destroyed, do it here in the destructor.
 */
OttoWhitePlayer::~OttoWhitePlayer( ) {}

/*
 * Private internal function that initializes a MAX_BOARD_SIZE 2D array of char to water.
 */
void OttoWhitePlayer::initializeBoard() {
    for(int row=0; row<boardSize; row++) {
	for(int col=0; col<boardSize; col++) {
	    this->board[row][col] = WATER;
        this->whereAreShips[row][col]=WATER;
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
Message OttoWhitePlayer::getMove() {
    bool even=true;

    lastCol+=2;
    if(lastCol>=boardSize){
        lastCol=0;
        lastRow++;
    }
    if(lastRow>=boardSize){
        lastCol=0;
        lastRow=0;
    }

    if (lastRow%2==0){
        even=true;
    }else{
        even=false;
    }
    if(even==true&&lastCol==0){
        lastCol=0;
    }
    else if(even==false && lastCol==0 && lastRow!=0){
        lastCol+=1;
    }
       

        
    
    
   /* lastCol++;
    if( lastCol >= boardSize ) {
    	lastCol = 0;
	    lastRow++;
    }
    if( lastRow >= boardSize ) {
	    lastCol = 0;
	    lastRow = 0;
    }
*/
    Message result( SHOT, lastRow, lastCol, "Bang", None, 1 );
    return result;
}

/**
 * @brief Tells the AI that a new round is beginning.
 * The AI show reinitialize any intra-round data structures.
 */
void OttoWhitePlayer::newRound() {
    /* DumbPlayer is too simple to do any inter-round learning. Smarter players 
     * reinitialize any round-specific data structures here.
     */
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
Message OttoWhitePlayer::placeShip(int length) {
    char shipName[10];
    // Create ship names each time called: Ship0, Ship1, Ship2, ...
    snprintf(shipName, sizeof shipName, "Ship%d", numShipsPlaced);
    
    while(true){
        //srand(time(NULL));
        int row = -1, col = -1;
        Direction dir = Direction(rand()%2+1);
        if (dir==Horizontal){
            row = rand()%boardSize;
            col = rand()%(boardSize-length);
        }else{
            row = rand()%(boardSize-length);
            col = rand()%boardSize;
        }
        if(canPlaceShip(length,dir,row,col)){
            placeOnBoard(length, dir, row, col);
            Message response( PLACE_SHIP, row, col, shipName, dir, length);
            numShipsPlaced++;
            return  response;
        }
    }


    // parameters = mesg type (PLACE_SHIP), row, col, a string, direction (Horizontal/Vertical)
    //                                 row       col  someString Horizontal/Vertical
    //Message response( PLACE_SHIP, numShipsPlaced, 0, shipName, Horizontal, length );
   // numShipsPlaced++;

   // return response;
}

bool OttoWhitePlayer::canPlaceShip(int shipSize, Direction dir, int row, int col){
//make a board of where im placing things to make sure dont have collisions do this in .h
//this is where i check the board to see if adding something is allowed
//    int placeHolder=0;
    if(dir==Horizontal){
        for (int i=0; i<shipSize;i++){
            if(whereAreShips[row][col+i]!=WATER){//*is water
                return false;
                //placeHolder+=1;
            }
        }
        return true;
        /*
        if (placeHolder==shipSize){
            return true;
        }
        */
    }else{
        for(int i =0; i<shipSize;i++){
            if(whereAreShips[row+i][col]!=WATER){
                return false;
               // placeHolder+=1;
            }
        }
        return true;
       // if (placeHolder==shipSize){
         //   return true;
        //}
    }
   // return false;

}


void OttoWhitePlayer::placeOnBoard(int shipSize, Direction dir, int row, int col){
    if(dir==Horizontal){
        for (int i=0; i<shipSize;i++){
            whereAreShips[row][col+i]=SHIP;//#is ship
        }
    }else{
        for(int i =0; i<shipSize;i++){
             whereAreShips[row+i][col]=SHIP;
        }
    }

   
    
    //this is where i literally add somethign to the board
}

/**
 * @brief Updates the AI with the results of its shots and where the opponent is shooting.
 * @param msg Message specifying what happened + row/col as appropriate.
 */
void OttoWhitePlayer::update(Message msg) {
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

