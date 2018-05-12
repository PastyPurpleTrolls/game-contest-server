#ifndef PLUTONIUM_H		// Double inclusion protection
#define PLUTONIUM_H

using namespace std;

#include "PlayerV2.h"
#include "Message.h"
#include "defines.h"
#include "PUPredictor.h"

// Plutonium inherits from/extends PlayerV2

class Plutonium : public PlayerV2 {
    public:
        Plutonium( int boardSize );
        ~Plutonium();
        void newRound();
        Message placeShip(int length);
        Message getMove();
        void update(Message msg);

    private:
        void initializeBoard();
        int lastRow;
        int lastCol;
        int numShipsPlaced;
        char board[MAX_BOARD_SIZE][MAX_BOARD_SIZE];

        int numShipPredictors;
        int numShotPredictors;
        Predictor* shipPredictors[5];
        Predictor* shotPredictors[5];
        Predictor* getBestPredictor(Predictor* predictors[], int predictorsCount);
        void doPredictions(Predictor* predictors[], int predictorsCount);
        void checkPredictions(Predictor* predictors[], int predictorsCount, int actualRow, int actualCol, bool miss);
};

#endif
