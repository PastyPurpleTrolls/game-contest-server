/**
 * @author Stefan Brandle and Jonathan Geisler
 * @date August, 2004
 * Main driver for BattleShipsV1 implementations.
 * Please type in your name[s] below:
 *
 *
 */

#ifndef AICONTEST_H
#define AICONTEST_H

// BattleShips project specific includes.
#include "Message.h"
#include "BoardV2.h"
#include "PlayerV1.h"

using namespace std;

class AIContest {
  public:
    AIContest( PlayerV1* player1, string player1Name,
               PlayerV1* player2, string player2Name,
	       int boardSize, bool silent );
    void play( float secondsDelay, int& totalMoves, bool& player1Won, bool& player2Won );

  private:
    void placeShips(BoardV2* board);
    void showBoard(BoardV2* board, bool ownerView, string playerName,
                   bool hLMostRecentShot, int hLRow, int hLCol );
    void clearScreen();
    void updateAI(PlayerV1 *player, BoardV2 *board);
    void snooze(float seconds);
    bool processShot(string playerName, PlayerV1 *player, BoardV2 *board, 
                     int row, int col, bool& playerQuit);

    // Data
    PlayerV1 *player1;
    PlayerV1 *player2;
    BoardV2 *player1Board;
    BoardV2 *player2Board;
    string player1Name;
    string player2Name;
    int boardSize;
    bool silent;
    bool player1Won;
    bool player2Won;
};

#endif
