#include <iostream>
#include <iomanip>
#include <cstdio>
#include <cstdlib>
#include <ctime>

#include "OurPlayer.h"

/**
 * @brief Constructor that initializes any inter-round data structures.
 * @param boardSize Indication of the size of the board that is in use.
 *
 * The constructor runs when the AI is instantiated (the object gets created)
 * and is responsible for initializing everything that needs to be initialized
 * before any of the rounds happen. The constructor does not get called 
 * before rounds; newRound() gets called before every round.
 */
OurPlayer::OurPlayer( int boardSize )
    :PlayerV2(boardSize)

{
	for(int w =0; w<=boardSize; w++){
		for( int z =0; z < boardSize; z++){
			OB[w][z] = 0;
		}
	}

    for(int row=0; row<boardSize; row++) {
		for(int col=0; col<boardSize; col++) {
			this->board[row][col] = WATER;
			this->ProbabilityBoard[row][col] = 0;
			this->ShipBoard[row][col] = WATER;
		}
    }
	
    // Could do any initialization of inter-round data structures here.
}

/**
 * @brief Destructor placeholder.
 * If your code does anything that requires cleanup when the object is
 * destroyed, do it here in the destructor.
 */
OurPlayer::~OurPlayer( ) {}

/*
 * Private internal function that initializes a MAX_BOARD_SIZE 2D array of char to water.
 */
void OurPlayer::initializeBoard() {
    for(int row=0; row<boardSize; row++) {
	for(int col=0; col<boardSize; col++) {
	    this->board[row][col] = WATER;
		this->ProbabilityBoard[row][col] = 0;
		this->ShipBoard[row][col] = WATER;

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
Message OurPlayer::getMove() {
	srand(time(NULL));
	if(board[lastRow][lastCol] == '~');{
		lastRow = rand() % 10;
		lastCol = rand() % 10;

	}
/*
	if(board[lastRow][lastCol] == 'X'){
		lastCol++;
	}else if(board[lastRow][lastCol] == '*'){
		lastRow++;
	}


	
	if(lastCol >= boardSize){
		lastCol = 0;
		lastRow++;
	}
	if(lastRow >= boardSize){
		lastCol = 0;
		lastRow = 0;
	}

	lastCol++;
*/	
	
//	int MaxProbRow;
//	int MaxProbCol;
	MaxProb = 0;


	for(int i=0; i < boardSize; i++){
		for(int j=0; j < boardSize; j++){
			ProbabilityBoard[i][j] =0;
			if(board[i][j] == WATER){
				//this goes down
				for(int d =1; d<=5; d++){
					if( (i+d) < boardSize-1){
						if( d==1 && board[i+d][j] == HIT){
							ProbabilityBoard[i][j] +=500;
						}

						if(board[i+d][j] == WATER){
							ProbabilityBoard[i][j]+= 5;
						}else if(board[i+d][j] == MISS){
							break;
						}else if (board[i+d][j] == HIT){
							ProbabilityBoard[i][j]  += 100;
						}else
							break;
					}
					else{
						break;
					}

				}
				//this should up
				for( int d =1; d<=5; d++){
					if( (i-d) >=0){

						if( d==1 && board[i-d][j] == HIT){
							ProbabilityBoard[i][j] +=500;
						}
						if(board[i-d][j] == WATER){
							ProbabilityBoard[i][j]+= 5;
						}else if(board[i-d][j] == MISS){
							break;
						}else if (board[i-d][j] == HIT){
							ProbabilityBoard[i][j]  += 100;
						}else
							break;
					}
				}
				//this should check right
				for(int d=1; d<=5; d++){
					if( (j+d) < boardSize){

						if( d==1 && board[i][j+d] == HIT){
							ProbabilityBoard[i][j] +=500;
						}
						if(board[i][j+d] == WATER){
							ProbabilityBoard[i][j]+= 5;
						}else if(board[i][j+d] == MISS){
							break;
						}else if (board[i][j+d] == HIT){
							ProbabilityBoard[i][j]  += 100;
						}else
							break;
					}
				}
				//this should check left
				for(int d=1; d<=5; d++){
					if( (j-d) < boardSize){

						if( d==1 && board[i][j-d] == HIT){
							ProbabilityBoard[i][j] +=500;
						}
						if(board[i][j-d] == WATER){
							ProbabilityBoard[i][j]+= 5;
						}else if(board[i][j-d] == MISS){
							break;
						}else if (board[i][j-d] == HIT){
							ProbabilityBoard[i][j]  += 100;
						}else
							break;
					}
				}
				
			if(ProbabilityBoard[i][j]>MaxProb){
				MaxProb = ProbabilityBoard[i][j];
				MaxProbRow = i;
				MaxProbCol =j;
			}
			}

		//	else if(board[i][j] == HIT || board[i][j] == MISS || board[i][j] == KILL){
		//				break;}

				//changes max prob based on the probability of each spot



			}
		

	}


    Message result( SHOT, MaxProbRow, MaxProbCol, "Bang", None, 1 );
    return result;
}

/**
 * @brief Tells the AI that a new round is beginning.
 * The AI show reinitialize any intra-round data structures.
 */
void OurPlayer::newRound() {
    /* DumbPlayer is too simple to do any inter-round learning. Smarter players 
     * reinitialize any round-specific data structures here.

	 */
	for(int r =0; r < boardSize; r++){
		for ( int c =0 ;c <boardSize; c++){
			cerr << setw(8) << OB[r][c]; 
		}
		cerr << endl;
	}
	cerr << endl;

	for(int r =0; r < boardSize; r++){
		for ( int c =0 ;c <boardSize; c++){
			cerr <<  ShipBoard[r][c]; 
		}
		cerr << endl;
	}
	cerr << endl;

	
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
Message OurPlayer::placeShip(int length) {
    char shipName[10];
	MinProb =5000;
	//int RowNum;
	//int ColNum;
	//this is checking vertical
	//Direction Dir;
	
/*
	if(numShipsPlaced == 0) {
		Message response( PLACE_SHIP, boardSize-1, boardSize-length, shipName, Horizontal, length );
		numShipsPlaced++;

	for(int L =0; L<length;L++){
			ShipBoard[boardSize-1][(boardSize-length)+L] = SHIP;
		}
		return response;			
	}

	else{
*/



	for( int i=0; i < boardSize; i++){
		for( int k = 0; k< boardSize; k++){
			SumProb = 0;

			for(int s = i; s < length+i; s++){
					if(s <  boardSize){
						if(ShipBoard[s][k] == SHIP){
							SumProb +=5000;
							break;
						}
						else {
							SumProb += OB[s][k];
						}
					}
					else{
						SumProb +=5000;
						//you want it this high to keep it from shooting here
					}
			}


//add probbaility of the opponent board to the sum probability
			if( SumProb <= MinProb){
				RowNum=i;
				ColNum=k;
				MinProb = SumProb;
				Dir = Vertical;
			}
			SumProb = 0;

		
			for(int s = k; s< length+k; s++){
					if(s <  boardSize){
						if(ShipBoard[i][s] == SHIP){
							SumProb +=5000;
							break;
						}
						else {
							SumProb += OB[i][s];
						}
					}
					else{
						SumProb +=5000;
						//you want it this high to keep it from shooting here
					}
			}


//add probbaility of th eoponent baord to the sum probability
			if( SumProb <= MinProb){
				RowNum=i;
				ColNum=k;
				MinProb = SumProb;
				Dir  =  Horizontal;
			}

	}
	}

	for(int L =0; L<length;L++){
		if(Dir == Vertical){
			ShipBoard[RowNum+L][ColNum] = SHIP;
		}
		else if( Dir == Horizontal){
			ShipBoard[RowNum][ColNum+L] = SHIP;
		}
	}

    // Create ship names each time called: Ship0, Ship1, Ship2, ...
    snprintf(shipName, sizeof shipName, "Ship%d", numShipsPlaced);

    // parameters = mesg type (PLACE_SHIP), row, col, a string, direction (Horizontal/Vertical)
    Message response( PLACE_SHIP, RowNum, ColNum, shipName, Dir, length );
    numShipsPlaced++;

    return response;
		
}

/**
 * @brief Updates the AI with the results of its shots and where the opponent is shooting.
 * @param msg Message specifying what happened + row/col as appropriate.
 */
void OurPlayer::update(Message msg) {
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
		this->OB[msg.getRow()][msg.getCol()]+=1;
		cerr << "OB shot ("<<msg.getRow() << "," << msg.getCol() << ")" << endl;
		//this adds one to the opponent board that we have stored to base our ship placement on

	    // TODO: get rid of the cout, but replace in your AI with code that does something
	    // useful with the information about where the opponent is shooting.
	    //cout << gotoRowCol(20, 30) << "DumbPl: opponent shot at "<< msg.getRow() << ", " << msg.getCol() << flush;
	    break;
    }
}

