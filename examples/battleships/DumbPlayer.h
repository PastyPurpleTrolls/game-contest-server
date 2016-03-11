/**
 * @author Stefan Brandle, Jonathan Geisler
 * @date September, 2004
 *
 * Please type in your name[s] here:
 *
 */

#ifndef DUMBPLAYER_H		// Double inclusion protection
#define DUMBPLAYER_H

using namespace std;

#include "PlayerV1.h"
#include "BoardV2.h"
#include "Message.h"
#include "defines.h"

// DumbPlayer inherits from/extends PlayerV1

class DumbPlayer: public PlayerV1 {
    public:
	DumbPlayer( int boardSize );
	~DumbPlayer();
	Message getMove();
	void hunter( int startRow, int startCol, int &shotRow, int &shotCol);
	bool goNorth( int startRow, int startCol, int &shotRow, int &shotCol);
	bool goEast( int startRow, int startCol, int &shotRow, int &shotCol);
	bool goSouth( int startRow, int startCol, int &shotRow, int &shotCol);
	bool goWest( int startRow, int startCol, int &shotRow, int &shotCol);

    private:
        int lastRow;
        int lastCol;
		int huntRow;
		int huntCol;
};

#endif
