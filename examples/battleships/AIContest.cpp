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
#include "AIContest.h"

using namespace std;

AIContest::AIContest( PlayerV1* player1, string player1Name, 
                      PlayerV1* player2, string player2Name,
		      int boardSize, bool silent )
{
    // Set up player 1
    this->player1 = player1;
    this->player1Board = new BoardV2(boardSize);
    this->player1Name = player1Name;
    this->player1Won = false;

    // Set up player 2
    this->player2 = player2;
    //this->player2Board = new BoardV2(this->player1Board);
    this->player2Board = new BoardV2(boardSize);
    *(this->player2Board) = *player1Board;
    this->player2Name = player2Name;
    this->player2Won = false;

    // General
    this->boardSize = boardSize;
    this->silent = silent;
}

/**
 * Places a ship. rowVector and colVector are used to determine direction of ship from
 * starting row/col.
 */
void AIContest::placeShips( BoardV2* board ) {
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

void AIContest::showBoard(BoardV2* board, bool ownerView, string playerName,
			  bool hLMostRecentShot, int hLRow, int hLCol ) {
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
#ifdef _POSIX_SOURCE
		char value = board->getOwnerView(row,col);
		if( value >= 'a' && value <= 'f' ) {
		    cout << "\033[7m" <<value<< "\033[0m";	// add ship highlighting
		} else {
		    cout << value;
		}
#else
		cout << board->getOwnerView(row,col);
#endif
	    } else {	// Not owner view -- regular game update.
#ifdef _POSIX_SOURCE
		if( hLMostRecentShot && row==hLRow && col==hLCol )
		    cout << "\033[7m" <<board->getOpponentView(row,col) << "\033[0m";
		else
#endif
		    cout << board->getOpponentView(row,col);
	    }
	}
	cout << endl;
    }
}

// Clears the screen.
void AIContest::clearScreen() {
    if( silent ) return;
#ifdef _POSIX_SOURCE
    cout << "\033[H\033[2J";
#else
    for(int i=0; i<25; i++) cout << endl;
#endif
}

void AIContest::snooze( float seconds ) {
    // usleep() takes argument in microseconds, so need to convert
    // seconds to microseconds.
    long sleepTime = long(1000000 * seconds);
    usleep(sleepTime);
}

void AIContest::updateAI(PlayerV1 *player, BoardV2 *board) {
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

bool AIContest::processShot(string playerName, PlayerV1 *player, BoardV2 *board, 
                           int row, int col, bool& playerQuit ) 
{
    bool won = false;
    if( !silent ) cout << "Processing " << playerName 
                       << "'s shot [" <<row<< "," <<col<< "]." << endl;
    Message msg = board->processShot( row, col );
    // Hack because board doesn't set these properly.
    msg.setRow(row);
    msg.setCol(col);
    switch( msg.getMessageType() ) {
	case QUIT:
	    if( !silent ) cout << "Sorry you aren't up to the challenge." << endl;
	    playerQuit = true;
	    break;
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
	case PEEK:
	    if( !silent ) {
	        showBoard(board, true, player1Name + "'s Cheat Board", false, 0, 0);
		snooze( 1 );
	    }

	    break;
	default:
	    if( !silent ) cout << "Invalid return from processShot: "
	                       << msg.getMessageType() << "(" << msg.getString() << ")" << endl;
	    break;
    }

    return won;
}

void AIContest::play( float secondsDelay, int& totalMoves, bool& player1Won, bool& player2Won ) {
    int maxShots = boardSize*boardSize*2;
    totalMoves = 0;
    clearScreen();
    placeShips(player1Board);
    *player2Board = *player1Board;
    bool player1Quit=false;
    bool player2Quit=false;

    //showBoard(playerBoard, true, "Sneak peek at player's board");

    do {
	clearScreen();
Message shot1 = player1->getMove();
	player1Won = processShot(player1Name, player1, player1Board, 
                                 shot1.getRow(), shot1.getCol(), player1Quit);
	if( ! silent ) {
	    showBoard(player1Board, false, player1Name + "'s Board",
		      true, shot1.getRow(), shot1.getCol());
	    cout << endl;
	}

	Message shot2 = player2->getMove();
	player2Won = processShot(player2Name, player2, player2Board, 
                                 shot2.getRow(), shot2.getCol(), player2Quit);
	if( ! silent ) {
	    showBoard(player2Board, false, player2Name + "'s Board",
		      true, shot2.getRow(), shot2.getCol());
	}
	totalMoves++;

	if( ! silent ) {
	    if( secondsDelay > 0 ) {	// Slows program if call to sleep 0.
		snooze( secondsDelay );
	    }
	}

    } while ( !(player1Quit || player2Quit) && !(player1Won || player2Won) && totalMoves < maxShots );

    if( ! silent ) {
	clearScreen();
	showBoard(player1Board, true, "Final status of " + player1Name + "'s board", 
	          false, -1, -1);
	cout << endl;
	showBoard(player2Board, true, "Final status of " + player2Name + "'s board", 
	          false, -1, -1);
	cout << endl;
    }

    if( player1Quit ) { 
        player2Won = true; 
    } else if( player2Quit ) {
        player1Won = true; 
    }

    if( player1Won && player2Won ) {
	cout << "The game was a tie. Both players sunk all ships." << endl;
    } else if( player1Won ) {
	cout << player1Name << " won." << endl;
    } else if( player2Won ) {
	cout << player2Name << " won." << endl;
    } else {   // both timed out -- neither won
	cout << "The game was a tie. Neither player sunk all ships." << endl;
    }
    cout << "--- (Moves = " << totalMoves << ", percentage of board shot at = " <<
			    (100.0*(float)totalMoves)/(boardSize*boardSize) << "%.)" << endl;
    cout << endl;
    if( ! silent ) {
	snooze( 5 );
    }
}

