#ifndef JJPLAYER_H
#define JJPLAYER_H

#include "PlayerV2.h"
#include <fstream>

using namespace std;

class JJplayer: public PlayerV2 {
    public:
        //Predefined:
        JJplayer( int boardSize );
        void newRound();
        Message placeShip( int length );
        Message getMove( );
        void update( Message msg );
        
        //Custom:
        void calcBaseProbability();
        void huntMode();
        void targetMode(int numHits);
    private:
        //Shooting info
        int rowToShoot;
        int colToShoot;
        int numKills;
        int newKills;
        int numHits;
        int sinceHit;
       
        //Win/Loss/Tie Stats
        struct Statistics {
            int totalRounds;
            int oddWins;
            int oddTies;
            int oddLosses;
            int evenWins;
            int evenTies;
            int evenLosses;
        };
        Statistics stats;
        int scatter;
 
        //Boards
        char offGameBoard[10][10];
        char defGameBoard[10][10];
        int baseProbBoard[10][10];
        double learnOffBoard[10][10];
        int learnDefBoard[10][10];
        int pattern[10][10];


        //Ships info:
        const static int NumShips = 6;
        int numShipsPlaced;
        int shipsArray[NumShips];

        //Debugging output
//        ofstream dout;
};

#endif

