#include <iostream>
#include <cstdio>
#include <iomanip>

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
    // Could do any initialization of inter-round data structures here.
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
     this->populateCellWeightBoard(); // TESTING!!!
     int maxWeight = 0;
     for(int row=0; row<boardSize; row++) {
 	      for(int col=0; col<boardSize; col++) {
 	         if (this->cellWeightBoard[row][col] > maxWeight) {
              maxWeight = this->cellWeightBoard[row][col];
           }
 	      }
     }

     for(int row=0; row<boardSize; row++) {
 	      for(int col=0; col<boardSize; col++) {
             //cerr << setw(4)<<cellWeightBoard[row][col];
 	         if (this->cellWeightBoard[row][col] == maxWeight) {
                lastRow = row;
                lastCol = col;
             }
 	      }
          //cerr << endl;
     }
     //cerr << endl;

     /*lastCol++;
     if( lastCol >= boardSize ) {
 	lastCol = 0;
 	lastRow++;
     }
     if( lastRow >= boardSize ) {
 	lastCol = 0;
 	lastRow = 0;
 } */

     Message result( SHOT, lastRow, lastCol, "Bang", None, 1 );
     return result;
 }

 /**
  * @brief Tells the AI that a new round is beginning.
  * The AI show reinitialize any intra-round data structures.
  */
 void Bassplayer::newRound() {
     /* Bassplayer is too simple to do any inter-round learning. Smarter players
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
 Message Bassplayer::placeShip(int length) {
     char shipName[10];
     // Create ship names each time called: Ship0, Ship1, Ship2, ...
     snprintf(shipName, sizeof shipName, "Ship%d", numShipsPlaced);

     int row = 0;
     int col = 0;
     // 0 = horizontal, 1 = vertical
     Direction direction = Horizontal;

     switch(numShipsPlaced){
       case 0:
         break;
       case 1:
         col = boardSize-1;
         direction = Vertical;
         break;
       case 2:
         row = boardSize-1;
         col = boardSize - length;
         break;
       case 3:
         row = boardSize-length;
         direction = Vertical;
         break;
       case 4:
         row = 1;
         col = 1;
         direction = Vertical;
         break;
       default:
         row =1;
         col = boardSize-2;
         direction = Vertical;
         break;
     }

     Message response( PLACE_SHIP, row, col, shipName, direction, length );

     // parameters = mesg type (PLACE_SHIP), row, col, a string, direction (Horizontal/Vertical)
     /*if(orientation == 0) {
       Message response( PLACE_SHIP, row, col, shipName, Horizontal, length );
     }
     else {
       Message response( PLACE_SHIP, row, col, shipName, Vertical, length );
     } */
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

// Other Functions in code




// calcCellWeightHoriz:  This function finds the column cell weight for a ship size 3
int Bassplayer::calcCellWeightHoriz( int row, int col ) {
    if ( board[row][col] != WATER ) {
        return -1;
    }
    int totalCount = 0;
    int count = 0;
    for( int c = col; c < col + 3; c++ ) {
        if(c - 2 >= 0 && c < boardSize){
            for( int i = 0; i < 3; ++i) {
                char ch = board[row][c - i];
                if( ch == KILL || ch == MISS ) {
                    count = 0;
                    break;
                }
                else if( ch == HIT ) {
                    count += 10;
                }
                else {
                    count ++;
                }
            }
        }
        totalCount += count;
        count = 0;
    }
    return totalCount;
}


// calcCellWeightVert:  This function finds the row cell weight for a ship size 3 *** NEEDS TO BE LOGIC CHECKED
int Bassplayer::calcCellWeightVert( int row, int col ) {
    if ( board[row][col] != WATER ) {
        return -1;
    }
  int totalCount = 0;
  int count = 0;
  for( int r = row; r < row + 3; r++ ) {
      if(r - 2 >= 0 && r < boardSize){
          for( int i = 0; i < 3; ++i) {
              char ch = board[r - i][col];
              if( ch == KILL || ch == MISS ) {
                  count = 0;
                  break;
              }
              else if( ch == HIT ) {
                  count += 10;
              }
              else {
                  count ++;
              }
          }
      }
      totalCount += count;
      count = 0;
  }
return totalCount;
}


// getCellWeight is a function that returns the total cell weight for a location (horz + vertical)
int Bassplayer::getCellWeight(int row, int col){
    return calcCellWeightHoriz(row, col) + calcCellWeightVert(row, col);
}


// populateCellWeights creates our matrix of intigers with the differnt cell weights for every location on the board.
void Bassplayer::populateCellWeightBoard() {
  for(int row=0; row<boardSize; row++) {
    for(int col=0; col<boardSize; col++) {
      this->cellWeightBoard[row][col] = getCellWeight(row, col);
    }
  }
}
