/**
 * @author 
 * @date April, 2017
 *
 * 
 *
 */

#ifndef GILLY_H		// Double inclusion protection
#define GILLY_H

using namespace std;

#include "PlayerV2.h"
#include "Message.h"
#include "defines.h"

// DumbPlayer inherits from/extends PlayerV2

class Gilly: public PlayerV2 {
    public:
	Gilly( int boardSize );
	~Gilly();
	void newRound();
	Message placeShip(int length);
	Message getMove();
	void update(Message msg);

    private:
	void initializeBoard();
        int lastRow;
        int lastCol;
	int numShipsPlaced;
        char board[MAX_BOARD_SIZE][MAX_BOARD_SIZE];
        char shipPlace[MAX_BOARD_SIZE][MAX_BOARD_SIZE];
        char copyBoard[MAX_BOARD_SIZE][MAX_BOARD_SIZE];
};

#endif
