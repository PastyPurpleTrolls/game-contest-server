#ifndef OurDumbPlayerV2_H		// Double inclusion protection
#define OurDumbPlayerV2_H

using namespace std;

#include "PlayerV2.h"
#include "Message.h"
#include "defines.h"

// DumbPlayer inherits from/extends PlayerV2

class OurDumbPlayerV2: public PlayerV2 {
    public:
	OurDumbPlayerV2( int boardSize );
	~OurDumbPlayerV2();
	void newRound();
	Message placeShip(int length);
	Message getMove();
	void update(Message msg);

    private:
	int placeRow;
	int placeCol;
	
	Direction dir;
	void initializeBoard();
        int lastRow;
        int lastCol;
	int hitRow;
	int hitCol;
	bool hasHitH;
	bool hasHitV;
	int numShipsPlaced;
        char board[MAX_BOARD_SIZE][MAX_BOARD_SIZE];
};

#endif
