#ifndef DUMBPLAYERV2_H		// Double inclusion protection
#define DUMBPLAYERV2_H

using namespace std;

#include "PlayerV2.h"
#include "Message.h"
#include "defines.h"

// DumbPlayer inherits from/extends PlayerV2

class Skynet: public PlayerV2 {
    public:
	Skynet( int boardSize );
	~Skynet();
	void newRound();
	Message placeShip(int length);
	Message getMove();
	void update(Message msg);

    private:
	void initializeBoard();
    bool searchUp(int row, int col, int size);
    bool searchUpPlace(int row, int col, int size);
    bool searchDownPlace(int row, int col, int size);
    bool searchDown(int row, int col, int size);
    bool searchLeft(int row, int col, int size);
    bool searchLeftPlace(int row, int col, int size);
    bool searchRight(int row, int col, int size);
    bool searchRightPlace(int row, int col, int size);
    bool validShip(int shipRow, int shipCol,int shipOri, int shipSize);
        int lastRow;
        int lastCol;
        int hitRow;
        int hitCol;
        int largestShip;
	int numShipsPlaced;
        char board[MAX_BOARD_SIZE][MAX_BOARD_SIZE];
        int hitBoard[MAX_BOARD_SIZE][MAX_BOARD_SIZE];
        int OurhitBoard[MAX_BOARD_SIZE][MAX_BOARD_SIZE];
        char shipBoard[MAX_BOARD_SIZE][MAX_BOARD_SIZE];
        int Probability[MAX_BOARD_SIZE][MAX_BOARD_SIZE];
        int HitProbability[MAX_BOARD_SIZE][MAX_BOARD_SIZE];
        int shipPlaceRow[11];
        int shipPlaceCol[11];
        int shipPlaceOri[11];
        int shipPlaceSize[11];
};

#endif
