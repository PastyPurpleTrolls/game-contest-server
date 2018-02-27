#ifndef Calahart_H		// Double inclusion protection
#define Calahart_H

using namespace std;

#include "PlayerV2.h"
#include "Message.h"
#include "defines.h"

// Calahart inherits from/extends PlayerV2

class Calahart: public PlayerV2 {
    public:
	Calahart( int boardSize );
	~Calahart();
	void newRound();
	Message placeShip(int length);
	Message getMove();
	void update(Message msg);
    private:
	void initializeBoard();
        int lastRow;
	bool checkShipValid(int row, int col, int length, Direction dir);
	void borderPlacement(int length, int &col, int &row, Direction &dir);
	void cornerPlacement(int length, int &col, int &row, Direction &dir);
	void probPlacement(int length, int &col, int &row, Direction &dir);
	void randomPlacement(int length, int &col, int &row, Direction &dir);
	void drawShip(int row, int col, int length, Direction dir);
	void pickHighProb( int &row, int &col, char b[MAX_BOARD_SIZE][MAX_BOARD_SIZE] );
	void pickLowProb( int &row, int &col, char b[MAX_BOARD_SIZE][MAX_BOARD_SIZE] );
	int cellProb(int row, int col, int length, char myBoard[MAX_BOARD_SIZE][MAX_BOARD_SIZE]);
        int lastCol;
	int numShipsPlaced;
	int sizeOfBoard;
        char board[MAX_BOARD_SIZE][MAX_BOARD_SIZE];
	char oppoBoard[MAX_BOARD_SIZE][MAX_BOARD_SIZE];
	char probBoard[MAX_BOARD_SIZE][MAX_BOARD_SIZE];
	char myProb[MAX_BOARD_SIZE][MAX_BOARD_SIZE];
	bool trackingMode;
};

#endif
