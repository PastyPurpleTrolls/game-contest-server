/**
 * @author Stefan Brandle and Jonathan Geisler
 * @date August, 2004
 * Main driver for BattleShipsV2 implementations.
 * Please type in your name[s] below:
 *
 *
 */

#include <iostream>
#include <iomanip>
#include <string>
#include <unistd.h>
#include <cstdlib>

// BattleShips project specific includes.
#include "defines.h"
#include "Message.h"
#include "BoardV3.h"
#include "AIContest.h"

using namespace std;

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

    // Ship stuff
    shipNames[0] = "Submarine";
    shipNames[1] = "Destroyer";
    shipNames[2] = "Aircraft Carrier";
    shipNames[3] = "Destroyer 2";
    shipNames[4] = "Submarine 2";
    shipNames[5] = "Aircraft Carrier 2";
    
    numShips = boardSize-2;
    if( numShips > MAX_SHIPS ) {
    	numShips = MAX_SHIPS;
    }

    for(int i=0; i<numShips; i++) {
	shipLengths[i] = random()%(MIN_SHIP_SIZE) + 3;
    }
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
    for( int i=0; i<numShips; i++ ) {
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
	                   Side side, int row, int col, PlayerV2* otherPlayer, int turn)
{
    bool won = false;
    int resultsRow = 16;
    int shotColOffset = side == Right ? 1 : 50;
    int boardColOffset = side == Left ? 1 : 50;
    // Wipe any previous contents clean first
    if( !silent ) cout << playerName
                       << "'s shot: [" <<row<< "," <<col<< "]" << endl;
    Message msg = board->processShot( row, col );
    // Hack because board doesn't set these properly.
    msg.setRow(row);
    msg.setCol(col);

    switch( msg.getMessageType() ) {
	case MISS:
	    if( !silent ) cout << setw(30) << "";
	    if( !silent ) cout << "Miss" << flush;
	    writeLog( turn, playerName, "MISS", row, col );
	    player->update(msg);
	    break;
	case HIT:
	    if( !silent ) cout << setw(30) << "";
	    if( !silent ) cout << "Hit" << flush;
	    writeLog( turn, playerName, "HIT", row, col );
	    player->update(msg);
	    break;
	case KILL:
	    if( !silent ) cout << setw(30) << "";
	    if( !silent ) cout << "It's a KILL! " << msg.getString() << flush;
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
	    if( !silent ) {
	        cout << setw(30) << "";
	        cout << "You already shot there.";
		cout << flush;
	    }
	    writeLog( turn, playerName, "DUPLICATE_SHOT", row, col );
	    player->update(msg);
	    break;
	case INVALID_SHOT:
	    if( !silent ) {
		cout << setw(30) << "";
	        cout << playerName << "Invalid coordinates: [row="<<row<<
	             ", col="<<col<<"]" << flush;
		cout << flush;
	    }
	    writeLog( turn, playerName, "INVALID_SHOT", row, col );
	    player->update(msg);
	    break;
	default:
	    if( !silent ) {
		cout << setw(30) << "";
	        cout << "Invalid return from processShot: "
	                       << msg.getMessageType() << "(" << msg.getString() << ")";
		cout << flush;
	    }
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
    cerr << "[" ;

    if( ! placeShips(player1, player1Board) ) {
	cout << endl;
	cout << player1Name << " placed ship in invalid location and forfeits game." << endl;
	cout << endl;
	player2Won = true;
    }

    if( ! placeShips(player2, player2Board) ) {
	cout << endl;
	cout << player2Name << " placed ship in invalid location and forfeits game." << endl;
	cout << endl;
	player1Won = true;
    }


    while ( !(player1Won || player2Won) && totalMoves < maxShots ){
	Message shot1 = player1->getMove();
	player1Won = processShot(player1Name, player1, player2Board, 
		Left, shot1.getRow(), shot1.getCol(), player2, turnCount);
	Message shot2 = player2->getMove();
	++turnCount;
	player2Won = processShot(player2Name, player2, player1Board, 
		Right, shot2.getRow(), shot2.getCol(), player1, turnCount);

	totalMoves++;
	++turnCount;

    }

    if( player1Won && player2Won ) {
	cout << "The game was a tie. Both players sunk all ships." << endl;
	Message msg(TIE);
	player1->update(msg);
	player2->update(msg);
	writeLog( turnCount, player1Name, "TIE", -1, -1 );
	writeLog( turnCount, player2Name, "TIE", -1, -1 );
    } else if( player1Won ) {
	cout << player1Name << " won." << endl;
	Message msg(WIN);
	player1->update(msg);
	msg.setMessageType(LOSE);
	player2->update(msg);
	writeLog( turnCount, player1Name, "WIN", -1, -1 );
	writeLog( turnCount, player2Name, "LOSE", -1, -1 );
    } else if( player2Won ) {
	cout << player2Name << " won." << endl;
	Message msg(WIN);
	player2->update(msg);
	msg.setMessageType(LOSE);
	player1->update(msg);
	writeLog( turnCount, player1Name, "LOSE", -1, -1 );
	writeLog( turnCount, player2Name, "WIN", -1, -1 );
    } else {   // both timed out -- neither won
	cout << "The game was a tie. Neither player sunk all ships." << endl;
	Message msg(LOSE);
	player1->update(msg);
	player2->update(msg);
    }
    cout << "--- (Moves = " << totalMoves << ", percentage of board shot at = " <<
			    (100.0*(float)totalMoves)/(boardSize*boardSize) << "%.)" << endl;
    cout << endl;
    cerr << "]" ;
}
