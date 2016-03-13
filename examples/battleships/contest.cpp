/**
 * @author Stefan Brandle and Jonathan Geisler
 * @date August, 2004
 * @date March, 2016
 *
 */

#include <iostream>
#include <unistd.h>
#include <cstring>
#include <csignal>
#include <vector>

// Next 2 to access and setup the random number generator.
#include <cstdlib>
#include <ctime>

// BattleShips project specific includes.
#include "AIContest.h"
#include "PlayerConnection.h"
#include "socketstream.h"

void playMatch(net::socketstream& manager, int totalGames, int *wins,
	       PlayerConnection& p1, PlayerConnection& p2);

using namespace std;

const int boardSize = 10;
const int NumPlayers = 2;

int main(int argc, char **argv) {
    int wins[NumPlayers];

    // Initialize various win statistics
    for(int i=0; i<NumPlayers; i++) {
	wins[i] = 0;
    }

    // Seed (setup) the random number generator.
    // This only needs to happen once per program run.
    srand(time(NULL));

    // Find out how many times to test the AI.
    int totalGames = atoi(argv[3]);

    struct sigaction sa;
    memset( &sa, 0, sizeof(sa) );
    sa.sa_handler = SIG_IGN;
    sigaction( SIGPIPE, &sa, NULL);

    net::socketstream manager("localhost", atoi(argv[1]));
    net::server referee;

    manager << "port:" << referee.get_port() << endl;
    manager << "match:start" << endl;

    vector<PlayerConnection> players;
    for (int i = 0; i < NumPlayers; ++i) {
	players.push_back(PlayerConnection(referee.serve(), boardSize));
    }

    // And now it's show time!
    playMatch(manager, totalGames, wins, players[0], players[1]);

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

void playMatch(net::socketstream& manager, int totalGames, int *wins,
	       PlayerConnection& player1, PlayerConnection& player2)
{
    bool player1Won=false, player2Won=false;
    int player1Ties=0, player2Ties=0;

    for( int count=0; count<totalGames; count++ ) {
	player1Won = false; player2Won = false;
	player1.newRound();
	player2.newRound();

	AIContest game(manager, player1, player2, boardSize);
	game.play( player1Won, player2Won );

	if((player1Won && player2Won) || !(player1Won || player2Won)) {
	    player1Ties++;
	    player2Ties++;
	} else if( player1Won ) {
	    wins[0]++;
	} else if( player2Won ) {
	    wins[1]++;
	}
    }
}
