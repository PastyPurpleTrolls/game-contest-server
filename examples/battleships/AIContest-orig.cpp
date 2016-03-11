/**
 * @author Stefan Brandle and Jonathan Geisler
 * @date August, 2004
 * Main driver for BattleShipsV2 implementations.
 * Please type in your name[s] below:
 *
 *
 */

#include <iostream>
#include <string>
#include <unistd.h>
#include <cstdlib>

// BattleShips project specific includes.
#include "defines.h"
#include "Message.h"
#include "BoardV3.h"
#include "AIContest.h"
#include "conio.h"

using namespace std;
using namespace conio;

AIContest::AIContest( PlayerV2* player1, string player1Name, 
                      PlayerV2* player2, string player2Name,
		      int boardSize, bool silent )
{
    // Set up player 1
    this->player1 = player1;
    this->player1Board = new BoardV3(boardSize);
    this->player1Name = player1Name;
    this->player1Won = false;

    // Set up player 2
    this->player2 = player2;
    this->player2Board = new BoardV3(boardSize);
    this->player2Name = player2Name;
    this->player2Won = false;

    // General
    this->boardSize = boardSize;
    this->silent = silent;
}

AIContest::~AIContest() {
    delete this->player1Board;
    delete this->player2Board;
}

/**
 * Places the ships. 
 */
//bool AIContest::placeShips( PlayerV2* player, BoardV3* board, BoardV3* testingBoard ) {
bool AIContest::placeShips( PlayerV2* player, BoardV3* board ) {
    const int NumShips = 6;
    string shipNames[NumShips]  = { "Submarine", "Destroyer", "Aircraft Carrier", 
			    "Destroyer 2", "Submarine 2", "Aircraft Carrier 2" };
    int shipLengths[NumShips];
    for(int i=0; i<NumShips; i++) {
	shipLengths[i] = random()%((MAX_SHIP_SIZE+1)-MIN_SHIP_SIZE) + MIN_SHIP_SIZE;
    }
    //= { 3,3,4,3,3,4 };

    int maxShips = boardSize-2;
    if( maxShips > NumShips ) {
    	maxShips = NumShips;
    }

    for( int i=0; i<maxShips; i++ ) {
	Message loc = player->placeShip( shipLengths[i] );
	bool placedOk = board->placeShip( loc.getRow(), loc.getCol(), shipLengths[i], loc.getDirection() );
	if( ! placedOk ) {
	    cerr << "Error: couldn't place "<<shipNames[i]<<" (length "<<shipLengths[i]<<")"<<endl;
	    return false;
	}
    }

    // All ships apparently placed ok.
    return true;
}

void AIContest::showBoard(BoardV3* board, bool ownerView, string playerName,
			  bool hLMostRecentShot, int hLRow, int hLCol ) {
    if( silent ) return;

    char ch;

    cout << endl << playerName << endl;
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
		ch = board->getOwnerView(row,col);
	    } else {
		ch = board->getOpponentView(row,col);
	    }

	    switch(ch) {
		case KILL: cout << fgColor(BLACK) << bgColor(LIGHT_RED); break;
	        case HIT: cout << fgColor(BLACK) << bgColor(LIGHT_MAGENTA); break;
	        case MISS: cout << fgColor(BLACK) << bgColor(GRAY); break;
	        case WATER: cout << fgColor(BLACK) << bgColor(LIGHT_CYAN); break;
	    }
	    if( ch>= 'a' && ch<='k' ) {
		cout << setTextStyle( NEGATIVE_IMAGE ) << ch << resetAll() << flush;
	    } else {
		if( hLMostRecentShot && hLRow==row && hLCol==col ) {
		    cout << setTextStyle( NEGATIVE_IMAGE ) << ch << setTextStyle( NEGATIVE_IMAGE ) << resetAll() << flush;
		} else {
		    cout << ch << resetAll() << flush;
		}
	    }
	}
	cout << resetAll() << endl;
    }
    cout << resetAll() << endl;
}

// Clears the screen.
void AIContest::clearScreen() {
    if( silent ) return;
    cout << clrscr() << flush;
}

void AIContest::snooze( float seconds ) {
    // usleep() takes argument in microseconds, so need to convert seconds to microseconds.
    long sleepTime = long(1000000 * seconds);
    usleep(sleepTime);
}

void AIContest::updateAI(PlayerV2 *player, string playerName, BoardV3 *board, int hitRow, int hitCol, int turn) {
    Message killMsg( KILL, -1, -1, "");
    char shipMark = board->getShipMark(hitRow, hitCol);

    for(int row=0; row<boardSize; row++) {
	for(int col=0; col<boardSize; col++) {
	    if(board->getShipMark(row,col) == shipMark) {
	        killMsg.setRow(row);
	        killMsg.setCol(col);
		player->update(killMsg);
		writeLog(turn, playerName, "KILL", row, col );
	    }
	}
    }
}

void AIContest::writeLog(int turn, string playerName, string status, int row, int col){
    cerr << '{' 
	 << " \"turn\":" << turn 
	 << ", \"player\":" << playerName 
	 << ", \"result\":\"" << status << "\""
	 << ", \"row\":" << row 
	 << ", \"col\":" << col 
	 << " }," << endl;
}

bool AIContest::processShot(string playerName, PlayerV2 *player, BoardV3 *board, 
                           int row, int col, PlayerV2 *otherPlayer, int turn) 
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
	    //{ player: 1, result: "MISS", row: 1, col: 1 },
	    writeLog( turn, playerName, "MISS", row, col );
	    player->update(msg);
	    break;
	case HIT:
	    if( !silent ) cout << "Hit." << endl;
	    writeLog( turn, playerName, "HIT", row, col );
	    player->update(msg);
	    break;
	case KILL:
	    if( !silent ) cout << "It's a KILL! " << msg.getString() << endl;
	    // Notify that is a hit
	    msg.setMessageType(HIT);
	    player->update(msg);
	    writeLog( turn, playerName, "HIT", row, col );

	    // Probably not needed, but just to be safe ...
	    msg.setMessageType(KILL);
	    // and notify that all segments of ship are now a KILL
	    updateAI(player, playerName, board, row, col, turn);

	    // Chance to win after every kill. Check
	    won = board->hasWon();
	    break;
	case DUPLICATE_SHOT:
	    if( !silent ) cout << "You already shot there." << endl;
	    writeLog( turn, playerName, "DUPLICATE_SHOT", row, col );
	    player->update(msg);
	    break;
	case INVALID_SHOT:
	    cout << playerName << " shot at invalid board coordinates [row="<<row<<
	             ", col="<<col<<"]." << endl;
	    writeLog( turn, playerName, "INVALID_SHOT", row, col );
	    player->update(msg);
	    break;
	default:
	    if( !silent ) cout << "Invalid return from processShot: "
	                       << msg.getMessageType() << "(" << msg.getString() << ")" << endl;
	    writeLog( turn, playerName, "INVALID_SHOT", row, col );
	    player->update(msg);
	    break;
    }
    //{ player: 1, result: "MISS", row: 1, col: 1 },
    // TODO: write something to log to mark off the end of each game

    // Notify the other player of the shot
    msg.setMessageType(OPPONENT_SHOT);
    otherPlayer->update(msg);

    return won;
}

void AIContest::play( float secondsDelay, int& totalMoves, bool& player1Won, bool& player2Won ) {
    int maxShots = boardSize*boardSize*2;
    totalMoves = 0;
    int turnCount = 0;
    clearScreen();
    cerr << "[" ;

    //showBoard(playerBoard, true, "Sneak peek at player's board");
    //BoardV3 testingBoard1(boardSize);
    //if( ! placeShips(player1, player1Board, testingBoard1) ) {
    if( ! placeShips(player1, player1Board) ) {
	//if( ! silent ) {
	    cout << endl;
	    cout << player1Name << " placed ship in invalid location and forfeits game." << endl;
	    cout << endl;
	    snooze( secondsDelay*4 );
	//}
	player2Won = true;
    }

    //BoardV3 testingBoard2(boardSize);
    //if( ! placeShips(player2, player2Board, testingBoard2) ) {
    if( ! placeShips(player2, player2Board) ) {
	//if( ! silent ) {
	    cout << endl;
	    cout << player2Name << " placed ship in invalid location and forfeits game." << endl;
	    cout << endl;
	    snooze( secondsDelay*4 );
	//}
	player1Won = true;
    }


    while ( !(player1Won || player2Won) && totalMoves < maxShots ){
	clearScreen();

	Message shot1 = player1->getMove();
	player1Won = processShot(player1Name, player1, player2Board, 
                                 shot1.getRow(), shot1.getCol(), player2, turnCount);
	if( ! silent ) {
	    showBoard(player2Board, false, player2Name + "'s Board",
		      true, shot1.getRow(), shot1.getCol());
	}

	++turnCount;
	Message shot2 = player2->getMove();
	player2Won = processShot(player2Name, player2, player1Board, 
                                 shot2.getRow(), shot2.getCol(), player1, turnCount);
	if( ! silent ) {
	    showBoard(player1Board, false, player1Name + "'s Board",
		      true, shot2.getRow(), shot2.getCol());
	    cout << endl;
	}

	totalMoves++;

	if( ! silent ) {
	    if( secondsDelay > 0 ) {	// Slows program if call to sleep 0.
		snooze( secondsDelay );
	    }
	}
	++turnCount;

    }

    if( ! silent ) {
	clearScreen();
	showBoard(player1Board, true, "Final status of " + player1Name + "'s board", 
	          false, -1, -1);
	cout << endl;
	showBoard(player2Board, true, "Final status of " + player2Name + "'s board", 
	          false, -1, -1);
	cout << endl;
    }

    if( player1Won && player2Won ) {
	cout << "The game was a tie. Both players sunk all ships." << endl;
	writeLog( turnCount, player1Name, "TIE", -1, -1 );
	writeLog( turnCount, player2Name, "TIE", -1, -1 );
    } else if( player1Won ) {
	cout << player1Name << " won." << endl;
	writeLog( turnCount, player1Name, "WIN", -1, -1 );
	writeLog( turnCount, player2Name, "LOSE", -1, -1 );
    } else if( player2Won ) {
	cout << player2Name << " won." << endl;
	writeLog( turnCount, player1Name, "LOSE", -1, -1 );
	writeLog( turnCount, player2Name, "WIN", -1, -1 );
    } else {   // both timed out -- neither won
	cout << "The game was a tie. Neither player sunk all ships." << endl;
    }
    cout << "--- (Moves = " << totalMoves << ", percentage of board shot at = " <<
			    (100.0*(float)totalMoves)/(boardSize*boardSize) << "%.)" << endl;
    cout << endl;
    if( ! silent ) {
	snooze( 5 );
    }
    cerr << "]" ;
}

