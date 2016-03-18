/**
 * @author Stefan Brandle and Jonathan Geisler
 * @date August, 2004
 * @date March, 2016
 *
 */

#include <iostream>
#include <unistd.h>
#include <cstring>
#include <vector>

// Next 2 to access and setup the random number generator.
#include <cstdlib>
#include <ctime>

// Next 2 to handle timeout through SIGALRM
#include <csignal>
#include <csetjmp>

// BattleShips project specific includes.
#include "AIContest.h"
#include "PlayerConnection.h"
#include "socketstream.h"

static void playMatch(net::socketstream& manager, int& totalGames,
		      vector<int>& wins,
		      PlayerConnection& p1, PlayerConnection& p2);

using namespace std;

const int boardSize = 10;
const int NumPlayers = 2;

static void logResult(net::socketstream& manager, string name,
		      int wins, int losses)
{
    manager << "matchresult:" << name << "|";
    if (wins > losses) {
	manager << "Win";
    } else if (wins < losses) {
	manager << "Loss";
    } else {
	manager << "Tie";
    }
    manager << "|" << wins << endl;
}

static jmp_buf alarm_buf;
sig_atomic_t last_wait;

static void timeout(int signal) {
    longjmp(alarm_buf, signal);
}

int main(int argc, char **argv) {
    // Initialize various win statistics
    vector<int> wins = { 0, 0 };

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

    memset( &sa, 0, sizeof(sa) );
    sa.sa_handler = timeout;
    sigaction( SIGALRM, &sa, NULL);
    alarm(atoi(argv[4]));

    manager << "port:" << referee.get_port() << endl;
    manager << "match:start" << endl;

    vector<PlayerConnection> players;

    if (setjmp(alarm_buf) == 0) {
	last_wait = 0;
	players.emplace_back(PlayerConnection(0, referee.serve(),
					      boardSize));
	last_wait = 1;
	players.emplace_back(PlayerConnection(1, referee.serve(),
					      boardSize));

	// And now it's show time!
	playMatch(manager, totalGames, wins, players[0], players[1]);
    } else {
	if (last_wait == 0) {
	    wins[1] += totalGames;
	} else {
	    wins[0] += totalGames;
	}
    }

    manager << "match:end" << endl;

    logResult(manager, players[0].get_name(), wins[0], wins[1]);
    logResult(manager, players[1].get_name(), wins[1], wins[0]);

    return 0;
}

void playMatch(net::socketstream& manager, int& totalGames,
	       vector<int>& wins,
	       PlayerConnection& player1, PlayerConnection& player2)
{
    bool player1Won=false, player2Won=false;

    while (totalGames) {
	player1Won = false; player2Won = false;
	player1.newRound();
	player2.newRound();

	AIContest game(manager, player1, player2, boardSize);
	game.play( player1Won, player2Won );

	if ( player1Won && !player2Won ) {
	    wins[0]++;
	} else if ( player2Won && !player1Won ) {
	    wins[1]++;
	}

	--totalGames;
    }
}
