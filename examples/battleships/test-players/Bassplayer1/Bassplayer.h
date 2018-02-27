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
  // Methods
  int getCellWeight( int row, int col ); // added by Jason
  int calcCellWeightVert( int row, int col ); // added by Jason
  int calcCellWeightHoriz( int row, int col ); // added by Jason
	void initializeBoard();
  void populateCellWeightBoard(); // added by Jason


  // Values
  int lastRow;
  int lastCol;
	int numShipsPlaced;
  int cellWeightBoard[MAX_BOARD_SIZE][MAX_BOARD_SIZE]; // added by Jason
  char board[MAX_BOARD_SIZE][MAX_BOARD_SIZE];

};

#endif
