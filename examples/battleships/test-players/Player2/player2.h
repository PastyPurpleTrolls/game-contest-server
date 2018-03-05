// BATTLESHIP AI

#ifndef FergusonHursey_H
#define FergusonHursey_H

using namespace std;

#include "PlayerV2.h"
#include "Message.h"
#include "defines.h"

class FergusonHursey: public PlayerV2 {
    public:
	FergusonHursey( int boardSize );
	~FergusonHursey();
	void newRound();
	Message placeShip(int length);
	Message getMove();
	void update(Message msg);

    private:
	void initializeBoard();
    int maxRow;
    int maxCol;
	int numShipsPlaced;
    char board[MAX_BOARD_SIZE][MAX_BOARD_SIZE];
    char shipMatrix[MAX_BOARD_SIZE][MAX_BOARD_SIZE];
    int shotMatrix[MAX_BOARD_SIZE][MAX_BOARD_SIZE];

    /* RANDOM SHOT PLACEMENT FUNCTIONS
    bool canPlaceShip(int length, Direction dir, int xcoord, int ycoord);
    void placeOnBoard(int length, Direction dir, int xcoord, int ycoord);
    */
    
    int horizontalProbCalc(int row, int col);
    int verticalProbCalc(int row, int col);
    int totalCalculator(int row, int col);
    void updateMatrix();
};

#endif
