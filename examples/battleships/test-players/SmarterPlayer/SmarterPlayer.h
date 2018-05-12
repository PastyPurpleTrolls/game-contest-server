#ifndef SmarterPlayer_H		// Double inclusion protection
#define SmarterPlayer_H

using namespace std;

#include "PlayerV2.h"
#include "Message.h"
#include "defines.h"

// DumbPlayer inherits from/extends PlayerV2

class SmarterPlayer: public PlayerV2 {
    public:
	SmarterPlayer( int boardSize );
	~SmarterPlayer();
	void newRound();
        int getNeighbors(int row, int col);
        bool checkShot(int row, int col);
        bool validShot(int row, int col);
	Message placeShip(int length);
	Message getMove();
        int* searchAndDestroy(int lastRow, int lastCol);
	void update(Message msg);
	
    private:
	void initializeBoard();
        int lastRow;
        int lastCol;
	int phase;
	int numShipsPlaced;
        char board[MAX_BOARD_SIZE][MAX_BOARD_SIZE];
	char shipBoard[MAX_BOARD_SIZE][MAX_BOARD_SIZE];
	int shotMatrix[MAX_BOARD_SIZE][MAX_BOARD_SIZE];
	bool canPlaceShip(int length, Direction dir, int row, int col);
	void placeOnBoard(int length, Direction dir, int row, int col);
};

#endif
