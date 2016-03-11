/**
 * @author Stefan Brandle and Jonathan Geisler
 * @date August, 2004
 * Main driver for BattleShipsV1 implementations.
 * Please type in your name[s] below:
 *
 *
 */

#include <iostream>
#include <iomanip>
#include <cctype>
#include <unistd.h>

// Next to access and setup the random number generator.
#include <cstdlib>
#include <ctime>

// BattleShips project specific includes.
#include "BoardV2.h"
#include "AIContest.h"
#include "PlayerV1.h"

// Include your player here

//	Professor's contestants
#include "HumanPlayer.h"
#include "OrigGamblerPlayer.h"
#include "CleanPlayer.h"


PlayerV1* getPlayer( int playerId, int boardSize );
int getPlayerChoice(string msg);

using namespace std;

int main() {
    int numGames;
    int boardSize;	// BoardSize
    bool silent = false;
    float secondsPerMove = 1;
    int totalGames = 0;
    int totalCountedMoves = 0;
    bool player1Won=false, player2Won=false;
    PlayerV1 *player1, *player2;
    AIContest *game;

    // Adjust based on the number of players!
    const int numPlayers = 3;
    int wins[numPlayers][numPlayers];
    int winCount[numPlayers];
    int statsShotsTaken[numPlayers];
    int statsGamesCounted[numPlayers];
    string playerNames[numPlayers] = { 
	"HumanPlayer",
	"CleanPlayer",
	"Original Gambler Player",
    };

    // Initialize various win statistics 
    for(int i=0; i<numPlayers; i++) {
	statsShotsTaken[i] = 0;
	statsGamesCounted[i] = 0;
	winCount[i] = 0;
	for(int j=0; j<numPlayers; j++) {
	    wins[i][j] = 0;
    	}
    }


    // Seed (setup) the random number generator.
    // This only needs to happen once per program run.
    srand(time(NULL));

    // Now to get the board size.
    cout << "Welcome to the AI Bot challenge." << endl << endl;
    cout << "What size board would you like? [Anything other than numbers 3-10 exits.] ";
    cin >> boardSize;
    // If have invalid board size input (non-number, or 0-2, or > 10).
    if ( !cin || boardSize < 3 || boardSize > 10 ) {
	cout << "Exiting" << endl;
	return 1;
    }

    // Find out how many times to fight the AI.
    cout << "How many times should I test the game AI? ";
    cin >> totalGames;

    cout << "The first game of each AI match is played at the specified speed," << endl
	 << "all subsequent games are done without visual display." << endl
	 << "How many seconds per move? (E.g., 1, 0.5, 1.3) : ";
    cin >> secondsPerMove;
    /*
    } else {
        milliSecondsPerMove = 0;
    }
    */

    // And now it's show time!
    int player1Wins, player2Wins, player1Ties, player2Ties;

    // Select player 1
    int player1Id = getPlayerChoice(("Select player 1"));
    while( player1Id < 0 && player1Id >= numPlayers ) {
	player1Id = getPlayerChoice("Select player 1");
    }

    // Select player 2
    int player2Id = getPlayerChoice(string("Select player 2"));
    while( player2Id < 0 && player2Id >= numPlayers ) {
	player2Id = getPlayerChoice("Select player 2");
    }

    // Reset match scores
    player1Wins=0; player2Wins=0; player1Ties=0; player2Ties=0;
    for( int count=0; count<totalGames; count++ ) {
	player1Won = false; player2Won = false;
	player1 = getPlayer(player1Id, boardSize);
	player2 = getPlayer(player2Id, boardSize);

	if( count==0 ) {
	    game = new AIContest( player1, playerNames[player1Id], 
				  player2, playerNames[player2Id],
		      boardSize, false /* !silent */ );
	    game->play( secondsPerMove, totalCountedMoves, player1Won, player2Won );
	} else {
	    game = new AIContest( player1, playerNames[player1Id], 
				  player2, playerNames[player2Id],
		      boardSize, true /* silent */ );
	    game->play( 0 /* no delay */, totalCountedMoves, player1Won, player2Won );
	}
	if((player1Won && player2Won) || !(player1Won || player2Won)) {
	    player1Ties++;
	    player2Ties++;
	    statsShotsTaken[player1Id] += totalCountedMoves;
	    statsGamesCounted[player1Id]++;
	    statsShotsTaken[player2Id] += totalCountedMoves;
	    statsGamesCounted[player2Id]++;
	} else if( player1Won ){
	    wins[player1Id][player2Id]++;
	    statsShotsTaken[player1Id] += totalCountedMoves;
	    statsGamesCounted[player1Id]++;
	} else {
	    wins[player2Id][player1Id]++;
	    statsShotsTaken[player2Id] += totalCountedMoves;
	    statsGamesCounted[player2Id]++;
	}
	delete player1;
	delete player2;
	delete game;
    }
    cout << endl << "********************" << endl;
    cout << playerNames[player1Id] << ": wins=" << wins[player1Id][player2Id] 
	 << " losses=" << totalGames-wins[player1Id][player2Id]-player1Ties 
	 << " ties=" << player1Ties << " (cumulative avg. shots/game = "
	 << (statsGamesCounted[player1Id]==0 ? 0.0 : 
	    (float)statsShotsTaken[player1Id]/(float)statsGamesCounted[player1Id])
	 << ")" << endl;
    cout << playerNames[player2Id] << ": wins=" << wins[player2Id][player1Id] 
	 << " losses=" << totalGames-wins[player2Id][player1Id]-player2Ties 
	 << " ties=" << player2Ties << " (cumulative avg. shots/game = "
	 << (statsGamesCounted[player2Id]==0 ? 0.0 : 
	    (float)statsShotsTaken[player2Id]/(float)statsGamesCounted[player2Id])
	 << ")" << endl;
    cout << "********************" << endl;
    usleep(5000000);	// Pause 5 seconds to let viewers see stats

    cout << endl << endl;
    int mostWins = -1;
    int winnerCount = 0;
    for( int i=0; i<numPlayers; i++ ) {
	for( int j=0; j<numPlayers; j++ )
	    winCount[i]+= wins[i][j];
	if( winCount[i] > mostWins ) {
	    mostWins = winCount[i];
	    winnerCount = 1;
	}
	else if( winCount[i] == mostWins ) {
	    winnerCount++;
	}
    }

    for( int i=0; i<numPlayers; i++ ) {
	cout << playerNames[i] << ": wins = " << winCount[i] 
	     << " (avg. shots/game = " << (statsGamesCounted[i]==0 ? 0.0 : 
		(float)statsShotsTaken[i]/(float)statsGamesCounted[i]) << ") ";

	if( winCount[i] == mostWins ) {
	    if( winnerCount == 1 ) {
		cout << "\t\033[1m(The WINNER!)\033[0m";
	    } else {	// tied win count
		cout << "\t\033[1m(Tied for First!!)\033[0m";
	    }
	}
	cout << endl;
    }

    return 0;
}

PlayerV1* getPlayer( int playerId, int boardSize ) {
    switch( playerId ) {
	// Professor provided
	case 0: return new HumanPlayer( boardSize );
	case 1: return new CleanPlayer( boardSize );
	case 2: return new OrigGamblerPlayer( boardSize );
	//case 3: return new Your_Player_Here( boardSize );
    }
}

int getPlayerChoice( string mesg ) {
    int choice;
    cout << mesg << endl
         << "0) Human Player" << endl
	 << "1) Clean Player" << endl
	 << "2) Original Gambler Player" << endl;
    cin >> choice;
    return choice;
}

