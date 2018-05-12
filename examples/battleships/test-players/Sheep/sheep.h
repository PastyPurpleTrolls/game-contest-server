#ifndef SHEEP_H		// Double inclusion protection
#define SHEEP_H

using namespace std;

#include "PlayerV2.h"
#include "Message.h"
#include "defines.h"

// DumbPlayer inherits from/extends PlayerV2

class sheep: public PlayerV2 {
    public:
	sheep( int boardSize );
	~sheep();
	void newRound();
	bool canPlaceShip(int shipSize, int direction, int row, int col);
	bool lastShip(int shipSize, int& row, int& col);
	Message placeShip(int length);
	Message getMove();
	void update(Message msg);
	void incrementShot(int& row, int& col);
	bool detectHit();
	void recheck();
	bool canShoot(int row, int col);

    private:
	bool turn1;
	int tempDirection;
	int targetDirection;
	bool hit;
	int hitRow;
	int hitCol;
	void initializeBoard();
        int lastRow;
        int lastCol;
	int numShipsPlaced;
        char board[MAX_BOARD_SIZE][MAX_BOARD_SIZE];
        char shipsOnBoard[MAX_BOARD_SIZE][MAX_BOARD_SIZE];
};

#endif
