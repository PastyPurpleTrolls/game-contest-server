/**
 * @file Gilly.cpp
 * @author Stefan Brandle, Jonathan Geisler
 * @date September, 2004 Updated 2015 for multi-round play.
 *
 * This Battleships AI is very simple and does nothing beyond playing
 * a legal game. However, that makes it a good starting point for writing
 * a more sophisticated AI.
 *
 * The constructor
 */

#include <iostream>
#include <cstdio>
#include <stdlib.h>
#include "conio.h"
#include "Gilly.h"

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
Gilly::Gilly( int boardSize )
    :PlayerV2(boardSize)
{
    // Could do any initialization of inter-round data structures here.
}

/**
 * @brief Destructor placeholder.
 * If your code does anything that requires cleanup when the object is
 * destroyed, do it here in the destructor.
 */
Gilly::~Gilly( ) {}

/*
 * Private internal function that initializes a MAX_BOARD_SIZE 2D array of char to water.
 */
void Gilly::initializeBoard() {
    for(int row=0; row<boardSize; row++) {
        for(int col=0; col<boardSize; col++) {
            this->board[row][col] = WATER;
            this->shipPlace[row][col] = WATER;
        }
    }
    for(int i=0; i<boardSize; i++){
        for(int j = 0; j<boardSize; j+=3){
            if(i+j+1 < boardSize ){
             copyBoard[i][j+i+1] = SHOT;
            }
        }
    }
    for (int m = 0; m<boardSize;m++){
        for (int n=0;n<boardSize;n+=3){
            if ((boardSize-3-(n+m))>=0){
                copyBoard[boardSize-1-m][boardSize-3-(n+m)]=SHOT;
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

int index = 1;
Message Gilly::getMove() {
/*    bool shotsA = false;
    for (int i=0; i<boardSize; i++){
    cerr<<"O"<<flush;
        for (int j=0; j<boardSize; j++){
        cerr<<"I"<<flush;
            if (copyBoard[i][j]==SHOT){
            cerr<<"A"<<flush;
                shotsA = true;
            }
        }
    }*/
    while (true){
            for (int row =0; row<boardSize; row++){
     //       cerr<<row<<flush;
            for (int col =0; col<boardSize; col++){
       //     cerr<<col<<flush;
            int searchingRow = row;
            int searchingCol = col;
            //bool colR = false;
            //bool colL = false;
            //bool rowUP = false;
            //bool rowDown = false;
            while(board[searchingRow][searchingCol] == HIT){
         //   cerr<<"7"<<flush;
            if(index == 1) {
            //cerr << "1" <<flush;
                if(board[searchingRow+1][searchingCol] == HIT && searchingRow+1 <boardSize){
                    searchingRow++;
                    index = 1;
                }
                else if(board[searchingRow+1][searchingCol] == MISS && searchingRow+1 <boardSize){
                    searchingRow = row;
                    index = -1;
                }
                else if(board[searchingRow+1][searchingCol] == KILL && searchingRow+1 <boardSize){
                    searchingRow = row;
                    index = -1;
                }
/*                else if(board[searchingRow+1][searchingCol] == WATER && searchingRow+1 <boardSize && searchingRow+2 < boardSize && board[searchingRow +2][searchingCol]!=WATER && rowDown ==false){
                    index = -1;
                    rowDown = true;
                }*/
                else if(board[searchingRow+1][searchingCol] == WATER && searchingRow+1 <boardSize){
                    Message result( SHOT, searchingRow+1, searchingCol, "Bang", None, 1 );
                    return result;
                }
                else{
                    index = -1;
                }
            }

            else if(index == -1) {    
            //cerr << "-1"<<flush;
                if(board[searchingRow-1][searchingCol] == HIT && searchingRow !=0){
                    searchingRow--;
                    index = -1;
                }
                else if(board[searchingRow-1][searchingCol] == MISS && searchingRow !=0){
                    searchingRow = row;
                    index = 2;
                }
                else if(board[searchingRow-1][searchingCol] == KILL && searchingRow !=0){
                    searchingRow = row;
                    index = 2;
                }
/*                else if(board[searchingRow-1][searchingCol] == WATER && searchingRow !=0 && searchingRow-1 >= 0 && board[searchingRow -2][searchingCol] !=WATER && rowUP == false){
                    index = 2;
                    rowUP = true;
                }*/
                else if(board[searchingRow-1][searchingCol] == WATER && searchingRow !=0){
                    Message result( SHOT, searchingRow-1, searchingCol, "Bang", None, 1 );
                    return result;
                }
                else {
                    index = 2;
                }
            }
            else if(index == 2){
            //cerr << "2" <<flush;

                if(board[searchingRow][searchingCol-1] == HIT && searchingCol !=0){
                    searchingCol--;
                    index =2;
                }
                else if(board[searchingRow][searchingCol-1] == MISS && searchingCol !=0){
                    searchingCol = col;
                    index = -2;
                }
                else if(board[searchingRow][searchingCol-1] == KILL && searchingCol !=0){
                    searchingCol = col;
                    index = -2;
                }
/*                else if(board[searchingRow][searchingCol-1] == WATER && searchingCol !=0 && searchingCol-1 >=0 && board[searchingRow][searchingCol -2] != WATER && colL == false ){
                    index = -2;
                    colL = true;
                }*/
                else if(board[searchingRow][searchingCol-1] == WATER && searchingCol !=0){
                    Message result( SHOT, searchingRow, searchingCol-1, "Bang", None, 1 );
                    return result;
                }
                else{
                    index = -2;
                }
            }
            else if (index -2){
            //cerr << "-2" <<flush;
                if(board[searchingRow][searchingCol+1] == HIT && searchingCol+1 <boardSize){
                    searchingCol++;
                    index = -2;
                }
                else if(board[searchingRow][searchingCol+1] == MISS && searchingCol+1 <boardSize){
                    searchingCol = col;
                    index =1;
                }
                else if(board[searchingRow][searchingCol+1] == KILL && searchingCol+1 <boardSize){
                    searchingCol = col;
                    index = 1;
                }
/*                else if(board[searchingRow][searchingCol+1] == WATER && searchingCol+1 <boardSize && searchingCol+2 < boardSize && board[searchingRow][searchingCol+2]!=WATER && colR == false){
                        index = 1;
                        colR = true;
                }*/
                else if(board[searchingRow][searchingCol+1] == WATER && searchingCol+1 <boardSize){
                    Message result( SHOT, searchingRow, searchingCol+1, "Bang", None, 1 );
                    return result;
                }
                else{
                    index = 1;
                }
            }    
            } 
            }
            }//closes searching for hit stuff
         
            int startingRow = rand() % boardSize; //randomly select row
            int startingCol = rand() % boardSize; //randomly select col
            if (board[startingRow][startingCol]==WATER && copyBoard[startingRow][startingCol] == SHOT){
            ////cerr<<"S"<<flush;
                Message result( SHOT, startingRow, startingCol, "Bang", None, 1 );
                copyBoard[startingRow][startingCol]=MISS;
                return result;
               }
     /*  else if (board[startingRow][startingCol]==WATER && shotsA==false){
        cerr<<"R"<<flush;
            Message result( SHOT, startingRow, startingCol, "Bang", None, 1 );
            return result; 
        }*/
    }
}

/**
 * @brief Tells the AI that a new round is beginning.
 * The AI show reinitialize any intra-round data structures.
 */
void Gilly::newRound() {
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
Message Gilly::placeShip(int length) {
    char shipName[10];
    // Create ship names each time called: Ship0, Ship1, Ship2, ...
    snprintf(shipName, sizeof shipName, "Ship%d", numShipsPlaced);
    
    int halfBoardSize;
    halfBoardSize = boardSize/2;
    /*if (numShipsPlaced%2==0){
        Direction dir = Direction (rand()%1+1);
        }
    else{Direction dir = Direction(rand()%1+2);}*/
    
    while(true){
        bool isSafe = true;
        int row,col;

        if (numShipsPlaced%2==0){
            Direction dir = Direction (1);
            cerr << dir<< flush;
            if (numShipsPlaced < 1){
            Direction dir = Direction (1);
                while(true){
                cerr <<"H#" << flush;
                Direction dir = Direction (1);
                    isSafe = true;
                    int corner = rand()%4;
                    switch(corner){
                        case 0:
                            row = 0;
                            col = 0;
                            break;
                        case 1:   
                            row = 0;
                            col = boardSize-length;
                            break;
                        case 2:
                            row = boardSize-1;
                            col = 0;
                            break;
                        case 3:
                            row = boardSize-1;
                            col = boardSize-length;
                            break;
                        default:
                            row = boardSize-1;
                            col = 0;
                    }//closes switch
                    
                    for (int i = 0; i < length;i++){
                        if (shipPlace[row][col+i]==SHIP){
                            isSafe = false;
                            cerr << "F" << flush;
                        }
                    }
                    if (isSafe == true){
                        for (int i = 0; i<length;i++){
                            shipPlace[row][col+i]=SHIP;
                            cerr << "I" << flush;
                        }
                    
                        Message response (PLACE_SHIP, row, col, shipName, dir, length);
                        numShipsPlaced++;
                        return response;
                    }
            /*        else{
                        Message response (PLACE_SHIP, row, col, shipName, dir, length);
                        numShipsPlaced++;
                        return response;
                    }*/
                }//closes while
            }//closes inner if
            else {
                cerr <<"H$" << flush;
                row = rand()%boardSize;
                col = rand()%(boardSize-length+1);
                //row = (rand()%(halfBoardSize))+halfBoardSize;
                //col = (rand()%(boardSize-length));
                for (int i = 0; i < length;i++){
                    if (col+i>=boardSize || shipPlace[row][col+i]==SHIP){
                        cerr<<"&" << flush;
                        isSafe = false;
                    }
                }
                if (isSafe == true){
                    for (int i = 0; i<length;i++){
                        shipPlace[row][col+i]=SHIP;
                    }

                    Message response (PLACE_SHIP, row, col, shipName, dir, length);
                    numShipsPlaced++;
                    return response;
                }
            }
        }//closes if statement

        else{
        Direction dir = Direction (2);
        if (numShipsPlaced < 1){
        while(true){
            isSafe = true;
            cerr <<"V" << flush;
            int corner = rand()%4;
            switch(corner){
            case 0:
                row = 0;
                col = 0;
                break;
            case 1:   
                row = 0;
                col = boardSize-1;
                break;
            case 2:
                row = boardSize-length;
                col = 0;
                break;
            case 3:
                row = boardSize-length;
                col = boardSize-1;
                break;
            default:
                row = boardSize-length;
                col = 0;
            }
            for (int i = 0; i < length;i++){
                if (shipPlace[row+i][col]==SHIP){
                    isSafe = false;
                }
            }
            if (isSafe == true){
                for (int i = 0; i<length;i++){
                    shipPlace[row+i][col]=SHIP;
                }
            
                Message response (PLACE_SHIP, row, col, shipName, dir, length);
                numShipsPlaced++;
                return response;
            }
            else{
                Message response (PLACE_SHIP, row, col, shipName, dir, length);
                numShipsPlaced++;
                return response;
            
            }
        }
        }
            else{
            //row = (rand()%(boardSize-length));
            //col = (rand()%(halfBoardSize))+halfBoardSize;
            col = rand()%boardSize;
            row = rand()%(boardSize-length+1);

            for (int i = 0; i < length;i++){
                if (shipPlace[row+i][col]==SHIP){
                    isSafe = false;
                }
            }
            if (isSafe == true){
                for (int i = 0; i<length;i++){
                    shipPlace[row+i][col]=SHIP;
                }
                Message response (PLACE_SHIP, row, col, shipName, dir, length);
                numShipsPlaced++;
                return response;
            }
        //closes Else statement
        
        // parameters = mesg type (PLACE_SHIP), row, col, a string, direction (Horizontal/Vertical)
        /*if (isSafe == true){
            Message response( PLACE_SHIP, row, col, shipName, dir, length );
            numShipsPlaced++;
            return response;
            }*/
        }
    }
    }
}


/**
 * @brief Updates the AI with the results of its shots and where the opponent is shooting.
 * @param msg Message specifying what happened + row/col as appropriate.
 */
void  Gilly::update(Message msg) {
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

