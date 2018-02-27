#ifndef Bassplayer_H		// Double inclusion protection
#define Bassplayer_H

using namespace std;

#include "PlayerV2.h"
#include "Message.h"
#include "defines.h"

// DumbPlayer inherits from/extends PlayerV2

class Bassplayer: public PlayerV2 {
    public:
	Bassplayer( int boardSize );
	~Bassplayer();
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
    char boardMatrix[MAX_BOARD_SIZE][MAX_BOARD_SIZE];
    char attackMatrix[MAX_BOARD_SIZE][MAX_BOARD_SIZE];
    int shipPlaceCount;
    int attackCount;
    int twoShotsAgoRow;
    int twoShotsAgoCol;
};

#endif
