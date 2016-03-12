/**
 * @author Stefan Brandle and Jonathan Geisler
 * @date August, 2004
 * Main driver for BattleShipsV3 implementations.
 * Please type in your name[s] below:
 *
 *
 */

#include <iostream>
#include <iomanip>
#include <cctype>
#include <unistd.h>
#include <vector>

// Next 2 to access and setup the random number generator.
#include <cstdlib>
#include <ctime>

// BattleShips project specific includes.
#include "BoardV3.h"
#include "AIContest.h"
#include "PlayerV2.h"
#include "PlayerConnection.h"
#include "socketstream.h"

void playMatch(net::socketstream& manager,
	       PlayerConnection& p1, PlayerConnection& p2);

using namespace std;

int boardSize;	// BoardSize
int totalGames = 0;
int totalCountedMoves = 0;
const int NumPlayers = 2;

int wins[NumPlayers];
int playerIds[NumPlayers];
int lives[NumPlayers];
int winCount[NumPlayers];
int statsShotsTaken[NumPlayers];
int statsGamesCounted[NumPlayers];

int main(int argc, char **argv) {
    // Adjust based on the number of players!
    // Initialize various win statistics 
    for(int i=0; i<NumPlayers; i++) {
	statsShotsTaken[i] = 0;
	statsGamesCounted[i] = 0;
	winCount[i] = 0;
	lives[i] = NumPlayers/2;
	playerIds[i] = i;
	wins[i] = 0;
    }

    // Seed (setup) the random number generator.
    // This only needs to happen once per program run.
    srand(time(NULL));

    // Now to get the board size.
    boardSize = 10;

    // Find out how many times to test the AI.
    totalGames = atoi(argv[3]);

    net::socketstream manager("localhost", atoi(argv[1]));
    net::server referee;

    manager << "port:" << referee.get_port() << endl;
    manager << "match:start" << endl;

    vector<PlayerConnection> players;
    for (int i = 0; i < NumPlayers; ++i) {
	players.push_back(PlayerConnection(referee.serve(), boardSize));
    }

    // And now it's show time!
    playMatch(manager, players[0], players[1]);

    manager << "match:end" << endl;

    manager << "matchresult:" << players[0].get_name() << "|";
    if (wins[0] > wins[1]) {
	manager << "Win";
    } else if (wins[0] < wins[1]) {
	manager << "Lose";
    } else {
	manager << "Tie";
    }
    manager << "|" << wins[0] << endl;

    manager << "matchresult:" << players[1].get_name() << "|";
    if (wins[1] > wins[0]) {
	manager << "Win";
    } else if (wins[1] < wins[0]) {
	manager << "Lose";
    } else {
	manager << "Tie";
    }
    manager << "|" << wins[1] << endl;

    return 0;
}

void playMatch(net::socketstream& manager,
	       PlayerConnection& player1, PlayerConnection& player2)
{
    AIContest *game;
    bool player1Won=false, player2Won=false;
    int player1Ties=0, player2Ties=0;

    for( int count=0; count<totalGames; count++ ) {
	player1Won = false; player2Won = false;
	player1.newRound();
	player2.newRound();

	AIContest game(manager, player1, player2, boardSize);
	game.play( totalCountedMoves, player1Won, player2Won );

	if((player1Won && player2Won) || !(player1Won || player2Won)) {
	    player1Ties++;
	    player2Ties++;
	    statsShotsTaken[0] += totalCountedMoves;
	    statsGamesCounted[0]++;
	    statsShotsTaken[1] += totalCountedMoves;
	    statsGamesCounted[1]++;
	} else if( player1Won ) {
	    wins[0]++;
	    statsShotsTaken[0] += totalCountedMoves;
	    statsGamesCounted[0]++;
	} else if( player2Won ) {
	    wins[1]++;
	    statsShotsTaken[1] += totalCountedMoves;
	    statsGamesCounted[1]++;
	}
    }
}
