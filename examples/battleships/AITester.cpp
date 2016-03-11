/**
 * @author Stefan Brandle and Jonathan Geisler
 * @date August, 2004
 * Main driver for BattleShipsV1 implementations.
 * Please type in your name[s] below:
 *
 *
 */

#include <iostream>
#include <string>
#include <unistd.h>

// BattleShips project specific includes.
#include "defines.h"
#include "Message.h"
#include "BoardV2.h"
#include "AITester.h"

using namespace std;

AITester::AITester( PlayerV1* player, BoardV2* playerBoard, string playerName,
		      int boardSize, bool silent )
{
    // Set up player 1
    this->player = player;
    this->playerBoard = playerBoard;
    this->playerName = playerName;

    // General
    this->boardSize = boardSize;
    this->silent = silent;
    this->playerWon = false;
}

/**
 * Places a ship. rowVector and colVector are used to determine direction of ship from
 * starting row/col.
 */
void AITester::placeShips( BoardV2* board ) {
    const int NumShips = 6;
    string shipNames[NumShips]  = { "Submarine", "Destroyer", "Aircraft Carrier", 
			    "Destroyer 2", "Submarine 2", "Aircraft Carrier 2" };
    int shipLengths[NumShips] = { 3,3,4,3,3,4 };

    int maxShips = boardSize-2;
    if( maxShips > NumShips ) {
    	maxShips = NumShips;
    }

    for( int i=0; i<maxShips; i++ ) {
	//if( board->placeShip(shipLengths[i], shipNames[i]) == false ) {
	if( board->placeShip(shipLengths[i]) == false ) {
	    cerr << "Couldn't place "<<shipNames[i]<<" (length "<<shipLengths[i]<<")"<<endl;
	}
    }
}

void AITester::showBoard(BoardV2* board, bool ownerView, string playerName) {
    if( silent ) return;

    cout << playerName << endl;
    cout << " |";
    for(int count=0; count<boardSize; count++) {
	cout << count;
    }
    cout << endl;

    // Put out horizontal header line
    for(int row=0; row<boardSize+2; row++) {
	cout << '-';
    }
    cout << endl;

    for(int row=0; row<boardSize; row++) {
	cout << (char)(row+'A') << "|";
	for(int col=0; col<boardSize; col++) {
	    if( ownerView == true ) {
		cout << board->getOwnerView(row,col);
	    } else {
		cout << board->getOpponentView(row,col);
	    }
	}
	cout << endl;
    }
}

// Clears the screen.
void AITester::clearScreen() {
    if( silent ) return;
#ifdef _POSIX_SOURCE
    cout << "\033[H\033[2J";
#else
    for(int i=0; i<25; i++) cout << endl;
#endif
}

void AITester::snooze( int milliSeconds ) {
    // usleep() takes argument in microseconds, so need to convert
    // milliseconds to microseconds.
    long sleepTime = 1000 * milliSeconds;
    usleep(sleepTime);
}

/*
void AITester::snooze( int seconds ) {
    sleep(seconds);
}
*/

void AITester::updateAI(PlayerV1 *player, BoardV2 *board) {
    Message killMsg( KILL, -1, -1, "");
    for(int row=0; row<boardSize; row++) {
	for(int col=0; col<boardSize; col++) {
	    if(board->getOwnerView(row,col) == KILL) {
	        killMsg.setRow(row);
	        killMsg.setCol(col);
		player->moveResult(killMsg);
	    }
	}
    }
}

bool AITester::processShot(string playerName, PlayerV1 *player, BoardV2 *board, 
                           int row, int col) 
{
    bool won = false;
    if( !silent ) cout << "Processing " << playerName 
                       << "'s shot [" <<row<< "," <<col<< "]." << endl;
    Message msg = board->processShot( row, col );
    // Hack because board doesn't set these properly.
    msg.setRow(row);
    msg.setCol(col);
    switch( msg.getMessageType() ) {
	case MISS:
	    if( !silent ) cout << "Miss" << endl;
	    player->moveResult(msg);
	    break;
	case HIT:
	    if( !silent ) cout << "Hit." << endl;
	    player->moveResult(msg);
	    break;
	case KILL:
	    if( !silent ) cout << "It's a KILL! " << msg.getString() << endl;
	    won = board->hasWon();
	    updateAI(player, board);
	    break;
	case DUPLICATE_SHOT:
	    if( !silent ) cout << "You already shot there." << endl;
	    break;
	case INVALID_SHOT:
	    cout << playerName << " shot at invalid board coordinates [row="<<row<<
	             ", col="<<col<<"]." << endl;
	    break;
	default:
	    if( !silent ) cout << "Invalid return from processShot: "
	                       << msg.getMessageType() << "(" << msg.getString() << ")" << endl;
	    break;
    }

    return won;
}

void AITester::play( int milliSecondsDelay, int& totalMoves ) {
    int maxShots = boardSize*boardSize*2;
    int shotCount = 0;
    totalMoves = 0;
    clearScreen();
    placeShips(playerBoard);

    //showBoard(playerBoard, true, "Sneak peek at player's board");

    do {
	clearScreen();

	Message shot = player->getMove();
	shotCount++;
	/*
	// This code kicks in when running in batch mode but want to see
	// what is happening with the occasional game that gets into trouble.
	if( silent && shotCount>70 ) {
	    silent = false;		// Turn on display again
	    milliSecondsDelay = 1000;	// One second per move
	}
	*/
	playerWon = processShot(playerName, player, playerBoard, shot.getRow(), shot.getCol());

	if( ! silent ) {
            if( playerWon ) {
	        showBoard(playerBoard, true, "Final status of " + playerName + "'s board");
	    } else {
		showBoard(playerBoard, false, playerName + "'s Board");
	    }
	    if( milliSecondsDelay > 0 ) {	// Slows program if call to sleep 0.
		snooze( milliSecondsDelay );
	    }
	}

	totalMoves++;
    } while ( !playerWon && shotCount < maxShots );

    if( ! silent ) {
	cout << endl;
	cout << "Moves = " << totalMoves << ", percentage of board shot at = " <<
				(100.0*(float)totalMoves)/(boardSize*boardSize) << "%." << endl;
	cout << endl;
	snooze( milliSecondsDelay );
    }
}

