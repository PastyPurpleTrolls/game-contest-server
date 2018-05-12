#ifndef OurPlayer_H		// Double inclusion protection
#define OurPlayer_H

using namespace std;

#include "PlayerV2.h"
#include "Message.h"
#include "defines.h"

// DumbPlayer inherits from/extends PlayerV2

class OurPlayer: public PlayerV2 {
    public:
	OurPlayer( int boardSize );
	~OurPlayer();
	void newRound();
	Message placeShip(int length);
	Message getMove();
	void update(Message msg);

    private:
	void initializeBoard();
        int lastRow;
        int lastCol;
		Direction Dir;
		int ColNum;
		int RowNum;
		int MinProb;
		int MaxProbRow;
		int MaxProbCol;
		int MaxProb;
		int SumProb;
	int numShipsPlaced;
        char board[MAX_BOARD_SIZE][MAX_BOARD_SIZE];
	int ProbabilityBoard[MAX_BOARD_SIZE][MAX_BOARD_SIZE];
	int OB[MAX_BOARD_SIZE][MAX_BOARD_SIZE];
	char ShipBoard[MAX_BOARD_SIZE][MAX_BOARD_SIZE];
};

#endif
