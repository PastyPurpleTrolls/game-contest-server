#include <iostream>
#include <cstdio>
#include <fstream>
#include <iomanip>
#include <cstdlib>
#include <ctime>

#include "Skynet.h"

/**
 * @brief Constructor that initializes any inter-round data structures.
 * @param boardSize Indication of the size of the board that is in use.
 *
 * The constructor runs when the AI is instantiated (the object gets created)
 * and is responsible for initializing everything that needs to be initialized
 * before any of the rounds happen. The constructor does not get called 
 * before rounds; newRound() gets called before every round.
 */
Skynet::Skynet( int boardSize )
    :PlayerV2(boardSize)
{
    // Could do any initialization of inter-round data structures here.
    
    for(int row = 0; row < boardSize; ++row) {
        for(int col = 0; col < boardSize; ++col) {
            hitBoard[row][col]=0;
            OurhitBoard[row][col]=0;
            this->board[row][col] = WATER;
            shipPlaceRow[row] = -1;
            shipPlaceCol[row] = -1;
            shipPlaceSize[row] = 0;
        }   
    }
    shipPlaceRow[10] = 0;
    shipPlaceCol[10] = 0;
    
}

/**
 * @brief Destructor placeholder.
 * If your code does anything that requires cleanup when the object is
 * destroyed, do it here in the destructor.
 */
Skynet::~Skynet( ) {}

/*
 * Private internal function that initializes a MAX_BOARD_SIZE 2D array of char to water.
 */
void Skynet::initializeBoard() {
    int half = static_cast<int>(boardSize/2);
    for(int row=0; row<boardSize; row++) {
        for(int col=0; col<boardSize; col++) {
            this->board[row][col] = WATER;
            this->shipBoard[row][col] = WATER;
            if ((row == half && col == half) || (row == half-1 && col == half-1) || (row == half-1 &&  col == half) ||
                (row == half && col == half-1)) {
//                shipBoard[row][col] = HIT;
            }
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
Message Skynet::getMove() {
   // ofstream prob;
   // prob.open("Probability.txt",std::ios_base::app);

    for (int row=0; row<boardSize; ++row) {
        for (int col = 0; col<boardSize; ++col) {
            Probability[row][col] = 0;
            HitProbability[row][col] = 0;
        }
    }

    for (int row=0; row<boardSize; ++row) {
        for (int col = 0; col<boardSize; ++col) {
            searchUp(row,col,MAX_SHIP_SIZE-largestShip);
            searchDown(row,col,MAX_SHIP_SIZE-largestShip);
            searchLeft(row,col,MAX_SHIP_SIZE-largestShip);
            searchRight(row,col,MAX_SHIP_SIZE-largestShip);
            if(Probability[row][col] != 0) {
                Probability[row][col] = Probability[row][col]; //+ OurhitBoard[row][col];
            }
        }
    }
    
    bool foundHit = false;
    for(int row=0; row<boardSize; ++row) {
        for(int col = 0; col<boardSize; ++col) {
            if(board[row][col] == HIT) {
                if(row+1 < boardSize) {
                    int newRow = row+1;
                    if(board[newRow][col] == WATER) {
                        HitProbability[newRow][col]++;
                        foundHit = true;
                    }
                    else if (board[newRow][col] == HIT) {
                        while(board[newRow][col] == HIT) {
                            if (newRow + 1 < boardSize) {
                                newRow++;
                            }
                            else {
                                break;
                            }  
                        }
                        if(board[newRow][col] == WATER) {
                            HitProbability[newRow][col]=newRow-row;
                            foundHit = true;
                        }
                    }
                }
                if(row-1 > -1) {
                    int newRow = row-1;
                    if(board[newRow][col] == WATER) {
                        HitProbability[newRow][col]++;
                        foundHit = true;
                    }
                    else if (board[newRow][col] == HIT) {
                        while(board[newRow][col] == HIT) {
                            if (newRow - 1 > -1) {
                                newRow--;
                            }
                            else {
                                break;
                            }  
                        }
                        if(board[newRow][col] == WATER) {
                            HitProbability[newRow][col]=row-newRow;
                            foundHit = true;
                        }
                    }
                }
                if(col+1 < boardSize) {
                    int newCol = col+1;
                    if(board[row][newCol] == WATER) {
                        HitProbability[row][newCol]++;
                        foundHit = true;
                    }
                    else if (board[row][newCol] == HIT) {
                        while(board[row][newCol] == HIT) {
                            if (newCol + 1 < boardSize) {
                                newCol++;
                            }
                            else {
                                break;
                            }  
                        }
                        if(board[row][newCol] == WATER) {
                            HitProbability[row][newCol]=newCol-col;
                            foundHit = true;
                        }
                    }
                }
                if(col-1 > -1) {
                    int newCol = col-1;
                    if(board[row][newCol] == WATER) {
                        HitProbability[row][newCol]++;
                        foundHit = true;
                    }
                    else if (board[row][newCol] == HIT) {
                        while(board[row][newCol] == HIT) {
                            if (newCol - 1 > -1) {
                                newCol--;
                            }
                            else {
                                break;
                            }  
                        }
                        if(board[row][newCol] == WATER) {
                            HitProbability[row][newCol]=col-newCol;
                            foundHit = true;
                        }
                    }
                }
            }
        }
    }

 /*   prob << "\nFIND PROB\n";
    for (int row=0; row<boardSize; ++row) {
        for (int col = 0; col<boardSize; ++col) {
            prob << setw(4) << Probability[row][col];
        }
        prob << "\n";
    }
    prob << "\nHIT PROB\n";
    for (int row=0; row<boardSize; ++row) {
        for (int col = 0; col<boardSize; ++col) {
            prob << setw(4) << HitProbability[row][col];
        }
        prob << "\n";
    }
    prob << "\nHIT MAP\n";
    for (int row=0; row<boardSize; ++row) {
        for (int col = 0; col<boardSize; ++col) {
            prob << setw(4) << hitBoard[row][col];
        }
        prob << "\n";
    }
    prob << "\n";
    prob.close();*/
    
    int rowShot = 0;
    int colShot = 0;
    if(foundHit) {
        for(int row = 0; row < boardSize; ++row) {
            for(int col = 0; col < boardSize; ++ col) {
                if(HitProbability[row][col] >= HitProbability[rowShot][colShot]) {
                    rowShot = row;
                    colShot = col;
                }
            }
        }
    }
    else {
        for(int row = 0; row < boardSize; ++row) {
            for(int col = 0; col < boardSize; ++ col) {
                if(Probability[row][col] >= Probability[rowShot][colShot]) {
                    rowShot = row;
                    colShot = col;
                }
            }
        }
    }

    Message result( SHOT, rowShot, colShot, "Bang", None, 1 );
    return result;
}

bool Skynet::searchUp(int row, int col, int size) {
    if (size == 0) {
        return true;
    }
    else if (row >= boardSize || row < 0) {
        return false;
    }
    else if (board[row][col] == HIT || board[row][col] == KILL || board[row][col] == MISS) {
        return false;
    }
    if (searchUp(row-1,col,size-1)) {
        Probability[row][col]++;
        return true;
    }
    else {
        return false;
    }
}

bool Skynet::searchDown(int row, int col, int size) {
    if (size == 0) {
        return true;
    }
    else if (row >= boardSize || row < 0) {
        return false;
    }
    else if (board[row][col] == HIT || board[row][col] == KILL || board[row][col] == MISS) {
        return false;
    }
    if (searchDown(row+1,col,size-1)) {
        Probability[row][col]++;
        return true;
    }
    else {
        return false;
    }
}

bool Skynet::searchLeft(int row, int col, int size) {
    if (size == 0) {
        return true;
    }
    else if (col >= boardSize || col < 0) {
        return false;
    }
    else if (board[row][col] == HIT || board[row][col] == KILL || board[row][col] == MISS) {
        return false;
    }
    if (searchLeft(row,col-1,size-1)) {
        Probability[row][col]++;
        return true;
    }
    else {
        return false;
    }
}

bool Skynet::searchRight(int row, int col, int size) {
    if (size == 0) {
        return true;
    }
    else if (col >= boardSize || col < 0) {
        return false;
    }
    else if (board[row][col] == HIT || board[row][col] == KILL || board[row][col] == MISS) {
        return false;
    }
    if (searchRight(row,col+1,size-1)) {
        Probability[row][col]++;
        return true;
    }
    else {
        return false;
    }
}
bool Skynet::searchLeftPlace(int row, int col, int size) {
    if (size == 0) {
        return true;
    }
    else if (col >= boardSize || col < 0) {
        return false;
    }
    else if (shipBoard[row][col] == HIT || shipBoard[row][col] == KILL || shipBoard[row][col] == MISS) {
        return false;
    }
    if (searchLeftPlace(row,col-1,size-1)) {
        return true;
    }
    else {
        return false;
    }
}
bool Skynet::searchRightPlace(int row, int col, int size) {
    if (size == 0) {
        return true;
    }
    else if (col >= boardSize || col < 0) {
        return false;
    }
    else if (shipBoard[row][col] == HIT || shipBoard[row][col] == KILL || shipBoard[row][col] == MISS) {
        return false;
    }
    if (searchRightPlace(row,col+1,size-1)) {
        return true;
    }
    else {
        return false;
    }
}
bool Skynet::searchDownPlace(int row, int col, int size) {
    if (size == 0) {
        return true;
    }
    else if (row >= boardSize || row < 0) {
        return false;
    }
    else if (shipBoard[row][col] == HIT || shipBoard[row][col] == KILL || shipBoard[row][col] == MISS) {
        return false;
    }
    if (searchDownPlace(row+1,col,size-1)) {
        return true;
    }
    else {
        return false;
    }
}
bool Skynet::searchUpPlace(int row, int col, int size) {
    if (size == 0) {
        return true;
    }
    else if (row >= boardSize || row < 0) {
        return false;
    }
    else if (shipBoard[row][col] == HIT || shipBoard[row][col] == KILL || shipBoard[row][col] == MISS) {
        return false;
    }
    if (searchUpPlace(row-1,col,size-1)) {
        return true;
    }
    else {
        return false;
    }
}
/**
 * @brief Tells the AI that a new round is beginning.
 * The AI show reinitialize any intra-round data structures.
 */
void Skynet::newRound() {
    /* DumbPlayer is too simple to do any inter-round learning. Smarter players 
     * reinitialize any round-specific data structures here.
     */
    this->lastRow++;
    this->lastCol = -1;
    this->numShipsPlaced = 0;
    this->hitRow = -1;
    this->hitCol = -1;
    this->largestShip = 0;

    for(int row = 0; row < boardSize; ++row) {
        for(int col = 0; col < boardSize; ++col) {
            if(board[row][col] == HIT || board[row][col] == KILL) {
                OurhitBoard[row][col]++;
            }
        }
    }
            
    this->initializeBoard();
}

bool Skynet::validShip(int shipRow,int shipCol,int shipOri,int shipSize) {
    if(shipRow >= boardSize || shipRow < 0 || shipCol >= boardSize || shipCol < 0) {
        return false;
    }
    if(shipOri == 0) {
        if(!searchRightPlace(shipRow, shipCol, shipSize)) {
            return false;
        }
       /* if(!searchLeftPlace(shipRow, shipCol,2)) {
            return false;
        }
        for(int i = 0; i < shipSize; ++i) {
            if(!searchUpPlace(shipRow, shipCol + i, 2)) {
                return false;
            }
            if(!searchDownPlace(shipRow, shipCol + i, 2)) {
                return false;
            }
        }
        if(!searchRightPlace(shipRow, shipCol + shipSize - 1, 2)) {
            return false;
        }*/
    }
    else {
        if(!searchDownPlace(shipRow, shipCol, shipSize)) {
            return false;
        }
       /* if(!searchUpPlace(shipRow, shipCol,2)) {
            return false;
        }
        for(int i = 0; i < shipSize; ++i) {
            if(!searchRightPlace(shipRow+i, shipCol, 2)) {
                return false;
            }
            if(!searchLeftPlace(shipRow+i, shipCol, 2)) {
                return false;
            }
        }
        if(!searchDownPlace(shipRow, shipCol + shipSize - 1, 2)) {
            return false;
        }*/
   }
   return true;
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
  NOTE TO MYSELF we can use search functions to check ship validity.
 */
Message Skynet::placeShip(int length) {
    char shipName[10];
    // Create ship names each time called: Ship0, Ship1, Ship2, ...
    snprintf(shipName, sizeof shipName, "Ship%d", numShipsPlaced);

    int shipRow = -1;
    int shipCol = -1;
    int shipOri = 0;
    int count = 0;
    int count2 = 0;
    int diff = 0;
    int lowestRow[boardSize*boardSize];
    int lowestCol[boardSize*boardSize];
    int index = 0;
    int sum = 0;
    int avg = 0;

    for(int row = 0; row < boardSize; ++row) {
        for(int col = 0; col < boardSize; ++col) {
            if(col + length <  boardSize){
                for(int i = 0; i < length; ++i) {
                    sum += hitBoard[row][col+i];
                }
            }
        }
    }
    avg = sum/boardSize*boardSize;
    index = 0;
    for(int row = 0; row < boardSize; ++row) {
        for(int col = 0; col < boardSize; ++col) {
            if (hitBoard[row][col] <= (avg/2)) {
                lowestRow[index] = row;
                lowestCol[index] = col;
            }
        }
        index++;
    }

    while(!validShip(shipRow, shipCol, shipOri, length)) {
        if (shipPlaceRow[10] == 1 && shipPlaceCol[10] == 1 && count < 6) {
            if(shipPlaceSize[count] == length-diff) {
                shipRow = shipPlaceRow[count];
                shipCol = shipPlaceCol[count];
                shipOri = shipPlaceOri[count];
                count++;
            }
            else {
                count++;
            }
        } 
        else if (count >= 6 && length-diff > 2 && validShip(shipRow, shipCol, shipOri, length)==false) {
            count = 0;
            diff++;
        }
        else if (count2 <= boardSize*boardSize) {
            int ranIn = (rand() % index) + 1;
            shipRow = lowestRow[ranIn];
            shipCol = lowestCol[ranIn];
            shipOri = 0;
            count2++;
        }
        else {
            shipRow = (rand() % boardSize);
            shipCol = (rand() % boardSize);
            shipOri = 0;//(rand() % 2);
        }
    }
    // parameters = mesg type (PLACE_SHIP), row, col, a string, direction (Horizontal/Vertical)
    shipPlaceRow[numShipsPlaced] = shipRow;
    shipPlaceCol[numShipsPlaced] = shipCol;
    shipPlaceOri[numShipsPlaced] = shipOri;
    shipPlaceSize[numShipsPlaced] = length;

//    ofstream prob;
//    prob.open("ShipPlace.txt",std::ios_base::app);
//    prob << "\n0 is lose, 1 is win: " << shipPlaceRow[10] << "\n";
//   prob << "Row, Col, length: " << shipRow << ", " << shipCol << ", " << length << "\n";
//    prob << "Just placed ship: " << numShipsPlaced << "\n";
//    prob.close();
    if(shipOri == 0) {
        for(int i = 0; i < length; ++i) {
            shipBoard[shipRow][shipCol + i] = HIT;
        }
        numShipsPlaced++;
     /*   prob << "\nShip Place\n";
        for (int row=0; row<boardSize; ++row) {
            for (int col = 0; col<boardSize; ++col) {
                prob << setw(4) << shipBoard[row][col];
            }
            prob << "\n";
        }*/
        Message response( PLACE_SHIP, shipRow, shipCol, shipName, Horizontal, length );
        return response;
    } else {
        for(int i = 0; i < length; ++i) {
            shipBoard[shipRow + i][shipCol] = HIT;
        }
        numShipsPlaced++;
       /* prob << "\nShip Place\n";
        for (int row=0; row<boardSize; ++row) {
            for (int col = 0; col<boardSize; ++col) {
                prob << setw(4) << shipBoard[row][col];
            }
            prob << "\n";
        }*/
        Message response( PLACE_SHIP, shipRow, shipCol, shipName, Vertical, length );
        return response;
    }
}

/**
 * @brief Updates the AI with the results of its shots and where the opponent is shooting.
 * @param msg Message specifying what happened + row/col as appropriate.
 */
void Skynet::update(Message msg) {
    switch(msg.getMessageType()) {
	case HIT:
	    board[msg.getRow()][msg.getCol()] = msg.getMessageType();
        break;
	case KILL:
        if(MAX_SHIP_SIZE - largestShip > MIN_SHIP_SIZE) {
            largestShip++;
        }
	    board[msg.getRow()][msg.getCol()] = msg.getMessageType();
        break;
	case MISS:
	    board[msg.getRow()][msg.getCol()] = msg.getMessageType();
	    break;
	case WIN:
        shipPlaceRow[10] = 1;
        shipPlaceCol[10] = 1;
	    break;
	case LOSE:
        shipPlaceRow[10] = 0;
        shipPlaceCol[10] = 0;
	    break;
	case TIE:
        shipPlaceRow[10] = 0;
        shipPlaceCol[10] = 0;
	    break;
	case OPPONENT_SHOT:
        hitBoard[msg.getRow()][msg.getCol()]++;
	    // TODO: get rid of the cout, but replace in your AI with code that does something
	    // useful with the information about where the opponent is shooting.
	    //cout << gotoRowCol(20, 30) << "DumbPl: opponent shot at "<< msg.getRow() << ", " << msg.getCol() << flush;
	    break;
    }
}

