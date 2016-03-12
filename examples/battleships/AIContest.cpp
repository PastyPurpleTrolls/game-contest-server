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

AIContest::AIContest( net::socketstream& contact,
		      PlayerConnection& p1, PlayerConnection& p2,
		      int boardSize )
    : manager(contact), player1(p1), player2(p2)
{
    // Set up player 1
    this->player1Board = new BoardV3(boardSize);
    this->player1Name = player1.get_name();
    this->player1Won = false;

    // Set up player 2
    this->player2Board = new BoardV3(boardSize);
    this->player2Name = player2.get_name();
    this->player2Won = false;

    // General
    this->boardSize = boardSize;

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
bool AIContest::placeShips( PlayerConnection& player, BoardV3* board ) {
    for( int i=0; i<numShips; i++ ) {
	Message loc = player.placeShip( shipLengths[i] );
	bool placedOk = board->placeShip( loc.getRow(), loc.getCol(), shipLengths[i], loc.getDirection() );
	if( ! placedOk ) {
	    return false;
	}
    }

    // All ships apparently placed ok.
    return true;
}

void AIContest::updateAI(PlayerConnection& player, string playerName, BoardV3 *board, int hitRow, int hitCol) {
    Message killMsg( KILL, -1, -1, "");
    char shipMark = board->getShipMark(hitRow, hitCol);

    for(int row=0; row<boardSize; row++) {
	for(int col=0; col<boardSize; col++) {
	    if(board->getShipMark(row,col) == shipMark) {
	        killMsg.setRow(row);
	        killMsg.setCol(col);
		player.update(killMsg);
	    }
	}
    }
}

bool AIContest::processShot(string playerName, PlayerConnection& player, BoardV3 *board, 
	                   int row, int col, PlayerConnection& otherPlayer)
{
    bool won = false;

    Message msg = board->processShot( row, col );
    // Hack because board doesn't set these properly.
    msg.setRow(row);
    msg.setCol(col);

    manager << "move:" << playerName << " shot @ " << row << "," << col
	    << "|{\"player\": \"" << playerName << "\", "
	    << "\"row\": " << row << ", "
	    << "\"col\": " << col << ", "
	    << "\"result\": \"";

    switch( msg.getMessageType() ) {
	case MISS:
	    manager << "miss";
	    player.update(msg);
	    break;
	case HIT:
	    manager << "hit";
	    player.update(msg);
	    break;
	case KILL:
	    manager << "kill";
	    player.inc_kills();

	    // Notify that is a hit
	    msg.setMessageType(HIT);
	    player.update(msg);

	    // and notify that all segments of ship are now a KILL
	    updateAI(player, playerName, board, row, col);

	    // Chance to win after every kill. Check
	    won = board->hasWon();
	    break;
	case DUPLICATE_SHOT:
	    manager << "duplicate";
	    player.update(msg);
	    break;
	default:
	case INVALID_SHOT:
	    manager << "invalid";
	    player.update(msg);
	    break;
    }

    manager << "\"}" << endl;

    // Notify the other player of the shot
    msg.setMessageType(OPPONENT_SHOT);
    otherPlayer.update(msg);

    return won;
}

void AIContest::play( int& totalMoves, bool& player1Won, bool& player2Won )
{
    manager << "round:start|{}" << endl;

    int maxShots = boardSize*boardSize*2;
    totalMoves = 0;

    if( ! placeShips(player1, player1Board) ) {
	player2Won = true;
    }

    if( ! placeShips(player2, player2Board) ) {
	player1Won = true;
    }


    while ( !(player1Won || player2Won) && totalMoves < maxShots ){
	Message shot1 = player1.getMove();
	player1Won = processShot(player1Name, player1, player2Board, 
		shot1.getRow(), shot1.getCol(), player2);

	Message shot2 = player2.getMove();
	player2Won = processShot(player2Name, player2, player1Board, 
		shot2.getRow(), shot2.getCol(), player1);

	totalMoves++;
    }

    manager << "round:end" << endl;

    if( player1Won && player2Won ) {
	Message msg(TIE);
	player1.update(msg);
	player2.update(msg);
	manager << "roundresult:" << player1Name << "|Tie|" << player1.get_kills() << endl;
	manager << "roundresult:" << player2Name << "|Tie|" << player2.get_kills() << endl;
    } else if( player1Won ) {
	Message msg(WIN);
	player1.update(msg);
	msg.setMessageType(LOSE);
	player2.update(msg);
	manager << "roundresult:" << player1Name << "|Win|" << player1.get_kills() << endl;
	manager << "roundresult:" << player2Name << "|Lose|" << player2.get_kills() << endl;
    } else if( player2Won ) {
	Message msg(WIN);
	player2.update(msg);
	msg.setMessageType(LOSE);
	player1.update(msg);
	manager << "roundresult:" << player1Name << "|Lose|" << player1.get_kills() << endl;
	manager << "roundresult:" << player2Name << "|Win|" << player2.get_kills() << endl;
    } else {   // both timed out -- neither won
	Message msg(LOSE);
	player1.update(msg);
	player2.update(msg);
	manager << "roundresult:" << player1Name << "|Lose|" << player1.get_kills() << endl;
	manager << "roundresult:" << player2Name << "|Lose|" << player2.get_kills() << endl;
    }
}
