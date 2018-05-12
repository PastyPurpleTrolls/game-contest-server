#ifndef Sylok_H		// Double inclusion protection
#define Sylok_H

using namespace std;

#include "PlayerV2.h"
#include "Message.h"
#include "defines.h"
#include <vector>
#include <stack>

// DumbPlayer inherits from/extends PlayerV2

class Sylok: public PlayerV2 {
    public:
	Sylok( int boardSize );
	~Sylok();
	void newRound();
	Message placeShip(int length);
	Message getMove();
	void update(Message msg);

    private:
	void initializeBoard();
	int numShipsPlaced;
    char board[MAX_BOARD_SIZE][MAX_BOARD_SIZE];
	int boardSize;
	
	//Shooting stuff AEB added
	vector<vector<vector<int> > > shootPairs; //stores row,col pairs that can be used to shoot 
	char shotResult; //stores the result of the last shot
	int roundCount; //counts the number of rounds in the game
	bool hasHit; //If Sylok is looking for the rest of the ship
	bool firstHit; //If this is the first hit on the ship
	vector<int> prevShot; //stores the location of the last shot 
	stack<vector<int> > hitPoss; //stores the possible next places to shoot if there was a hit
	vector<int> firstHitLoc; //Stores the location of the first hit on the ship
	
	//Placing stuff also added by me ;)
	vector<int> prevShip; // stores the location of the end of the last ship TODO probably delete
	vector<int> shipStart; // stores the row and col of the next ship to be placed(may be invalid)
	int threes; //stores the numer of ships placed of length 3

};

#endif
