/**
 * @author Stefan Brandle and Jonathan Geisler
 * @date August, 2004
 * @date March, 2016
 *
 */

#include <algorithm>
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
    : manager(contact), player1(p1), player2(p2),
      player1Board(boardSize), player2Board(boardSize)
{
    // General
    this->boardSize = boardSize;

    numShips = min(boardSize-2, +MAX_SHIPS);

    for(int i=0; i<numShips; i++) {
	shipLengths.push_back(random() % MIN_SHIP_SIZE + 3);
    }
}

/**
 * Places the ships. 
 */
bool AIContest::placeShips( PlayerConnection& player, BoardV3& board ) {
    for (int length : shipLengths) {
	Message loc = player.placeShip(length);
	bool placedOk = board.placeShip( loc.getRow(), loc.getCol(), length, loc.getDirection() );

	manager << "move:" << player.get_name() << " place @ "
		<< loc.getCol() << "," << loc.getRow()
		<< "|{\"player\": \"" << player.get_name() << "\", "
		<< "\"action\": \"place\", "
		<< "\"row\": " << loc.getRow() << ", "
		<< "\"col\": " << loc.getCol() << ", "
		<< "\"result\": " << placedOk << ", "
		<< "\"direction\": " << loc.getDirection() << ", "
		<< "\"length\": " << length
		<< "}" << endl;

	if( ! placedOk ) {
	    return false;
	}
    }

    // All ships apparently placed ok.
    return true;
}

void AIContest::updateAI(PlayerConnection& player, BoardV3& board, int hitRow, int hitCol) {
    Message killMsg( KILL, -1, -1, "");
    char shipMark = board.getShipMark(hitRow, hitCol);

    for(int row=0; row<boardSize; row++) {
	for(int col=0; col<boardSize; col++) {
	    if(board.getShipMark(row,col) == shipMark) {
	        killMsg.setRow(row);
	        killMsg.setCol(col);
		player.update(killMsg);
	    }
	}
    }
}

bool AIContest::processShot(PlayerConnection& player, BoardV3& board, 
	                   int row, int col, PlayerConnection& otherPlayer)
{
    bool won = false;

    Message msg(board.processShot( row, col ), row, col, "Shot results");

    manager << "move:" << player.get_name()
	    << " shot @ " << col << "," << row
	    << "|{\"player\": \"" << player.get_name() << "\", "
	    << "\"action\": \"shot\", "
	    << "\"row\": " << row << ", "
	    << "\"col\": " << col << ", "
	    << "\"result\": \"" << msg.getMessageType() << "\"}" << endl;

    if (msg.getMessageType() != KILL) {
	player.update(msg);
    } else {
	player.inc_kills();

	// Notify that is a hit
	msg.setMessageType(HIT);
	player.update(msg);

	// and notify that all segments of ship are now a KILL
	updateAI(player, board, row, col);

	// Chance to win after every kill. Check
	won = board.hasWon();
    }

    // Notify the other player of the shot
    msg.setMessageType(OPPONENT_SHOT);
    otherPlayer.update(msg);

    return won;
}

static void logResult(net::socketstream& manager,
		      const PlayerConnection& player,
		      string result)
{
    manager << "roundresult:" << player.get_name() << "|"
	    << result << "|" << player.get_kills() << endl;
}

void AIContest::play( bool& player1Won, bool& player2Won )
{
    manager << "round:start|{}" << endl;

    if( ! placeShips(player1, player1Board) ) {
	player2Won = true;
    }

    if( ! placeShips(player2, player2Board) ) {
	player1Won = true;
    }

    const int maxShots = boardSize*boardSize*2;
    int totalMoves = 0;

    while ( !(player1Won || player2Won) && totalMoves < maxShots ){
	Message shot1 = player1.getMove();
	player1Won = processShot(player1, player2Board, 
		shot1.getRow(), shot1.getCol(), player2);

	Message shot2 = player2.getMove();
	player2Won = processShot(player2, player1Board, 
		shot2.getRow(), shot2.getCol(), player1);

	totalMoves++;
    }

    manager << "round:end" << endl;

    if( player1Won && player2Won ) {
	player1.update(TIE);
	player2.update(TIE);
	logResult(manager, player1, "Tie");
	logResult(manager, player2, "Tie");
    } else if( player1Won ) {
	player1.update(WIN);
	player2.update(LOSE);
	logResult(manager, player1, "Win");
	logResult(manager, player2, "Loss");
    } else if( player2Won ) {
	player1.update(LOSE);
	player2.update(WIN);
	logResult(manager, player1, "Loss");
	logResult(manager, player2, "Win");
    } else {   // both timed out -- neither won
	player1.update(LOSE);
	player2.update(LOSE);
	logResult(manager, player1, "Loss");
	logResult(manager, player2, "Loss");
    }
}
