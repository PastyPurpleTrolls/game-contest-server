#ifndef OttoWhitePlayer_H		// Double inclusion protection
#define OttoWhitePlayer_H

using namespace std;

#include "PlayerV2.h"
#include "Message.h"
#include "defines.h"

// DumbPlayer inherits from/extends PlayerV2

class OttoWhitePlayer: public PlayerV2 {
    public:
	OttoWhitePlayer( int boardSize );
	~OttoWhitePlayer();
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
        char whereAreShips[MAX_BOARD_SIZE][MAX_BOARD_SIZE];
    bool canPlaceShip(int length, Direction dir, int row, int col);
    void placeOnBoard(int length, Direction dir, int row, int col);
};

#endif
