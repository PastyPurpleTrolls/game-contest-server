/**
 * @author Stefan Brandle and Jonathan Geisler
 * @date August, 2004
 * @date March, 2016
 *
 */

#ifndef AICONTEST_H
#define AICONTEST_H

// BattleShips project specific includes.
#include "BoardV3.h"
#include "PlayerConnection.h"
#include "socketstream.h"

using namespace std;

class AIContest {
  public:
    AIContest( net::socketstream& manager,
	       PlayerConnection& player1, PlayerConnection& player2,
	       int boardSize );
    void play( bool& player1Won, bool& player2Won );

  private:
    bool placeShips( PlayerConnection& player, BoardV3& board);
    void updateAI(PlayerConnection& player, string playerName, BoardV3& board, int hitRow, int hitCol);
    bool processShot(string playerName, PlayerConnection& player, BoardV3& board,
	             int row, int col, PlayerConnection& otherPlayer);

    // Data
    PlayerConnection& player1;
    PlayerConnection& player2;
    BoardV3 player1Board;
    BoardV3 player2Board;
    net::socketstream& manager;

    string player1Name;
    string player2Name;

    int boardSize;

    // Ship information
    static const int MAX_SHIPS = 6;
    int shipLengths[MAX_SHIPS];
    int numShips;
};

#endif
