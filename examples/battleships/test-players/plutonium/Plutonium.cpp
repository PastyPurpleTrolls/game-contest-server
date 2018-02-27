#include <iostream>
#include <cstdio>
#include <stdexcept>

#include "conio.h"
#include "Plutonium.h"

#include "PUPredictor.h"
#include "PUDumbShotPredictor.cpp"
#include "PUDumbShipPredictor.cpp"
#include "PUCleanShotPredictor.cpp"
#include "PURandomShipPredictor.cpp"

using namespace conio;
using namespace std;

/**
 * @brief Constructor that initializes any inter-round data structures.
 * @param boardSize Indication of the size of the board that is in use.
 *
 * The constructor runs when the AI is instantiated (the object gets created)
 * and is responsible for initializing everything that needs to be initialized
 * before any of the rounds happen. The constructor does not get called 
 * before rounds; newRound() gets called before every round.
 */
Plutonium::Plutonium( int boardSize )
    :PlayerV2(boardSize)
{
//    shipPredictors[0] = new DumbShipPredictor();
    shipPredictors[0] = new RandomShipPredictor();
    
    shotPredictors[0] = new DumbShotPredictor();
    shotPredictors[1] = new CleanShotPredictor();

    numShipPredictors = 1;
    numShotPredictors = 2;

    cerr << "PLUTONIUM CONSTRUCTOR" << endl;
}

/**
 * @brief Destructor 
 */
Plutonium::~Plutonium( ) {
}

/*
 * Private internal function that initializes a MAX_BOARD_SIZE 2D array of char to water.
 */
void Plutonium::initializeBoard() {
    for(int row=0; row<boardSize; row++) {
        for(int col=0; col<boardSize; col++) {
            this->board[row][col] = WATER;
        }
    }
}


/**
 * @brief Specifies the AI's shot choice and returns the information to the caller.
 * @return Message The most important parts of the returned message are 
 * the row and column values. 
 *
 * See the Message class documentation for more information on the 
 * Message constructor.
 */
Message Plutonium::getMove() {
    Predictor* opponentShipStrategy = this->getBestPredictor(shipPredictors, numShipPredictors);
    int moveRow;
    int moveCol;
    int dummyOut;
    opponentShipStrategy->getNextCounter(board, boardSize, moveRow, moveCol, -1, dummyOut);
    cerr << "SHOT: " << moveRow << " " << moveCol << endl;
    Message result(SHOT, moveRow, moveCol, "Bang", None, 1);
    return result;
}

/**
 * @brief Tells the AI that a new round is beginning.
 * The AI show reinitialize any intra-round data structures.
 */
void Plutonium::newRound() {
    this->lastRow = 0;
    this->lastCol = -1;
    this->numShipsPlaced = 0;

    this->initializeBoard();

    for (int i=0; i<numShipPredictors; i++) {
        shipPredictors[i]->reset();
    }
    for (int i=0; i<numShotPredictors; i++) {
        shotPredictors[i]->reset();
    }
    cerr << "PLUTONIUM NEWROUND" << endl;
}

/**
 * @brief Gets the AI's ship placement choice. This is then returned to the caller.
 * @param length The length of the ship to be placed.
 * @return Message The most important parts of the returned message are 
 * the direction, row, and column values. 
 *
 * The parameters returned via the message are:
 * 1. the operation: must be PLACE_SHIP 
 * 2. ship top row value
 * 3. ship top col value
 * 4. a string for the ship name
 * 5. direction Horizontal/Vertical (see defines.h)
 * 6. ship length (should match the length passed to placeShip)
 */
Message Plutonium::placeShip(int length) {
    char shipName[15];
    // Create ship names each time called: Ship0, Ship1, Ship2, ...
    snprintf(shipName, sizeof shipName, "Ship%d", numShipsPlaced);

    // parameters = mesg type (PLACE_SHIP), row, col, a string, direction (Horizontal/Vertical)
    int row;
    int col;
    int direction;
    Predictor* opponentShotStrategy = this->getBestPredictor(shotPredictors, numShotPredictors);
    opponentShotStrategy->getNextCounter(board, boardSize, row, col, length, direction);
    Message response(PLACE_SHIP, row, col, shipName, (Direction)direction, length);
    numShipsPlaced++;

    return response;
}

/**
 * @brief Updates the AI with the results of its shots and where the opponent is shooting.
 * @param msg Message specifying what happened + row/col as appropriate.
 */
void Plutonium::update(Message msg) {
    cerr << "MSG: " << msg.getMessageType() << " " << msg.getRow() << " " << msg.getCol() << endl;
    switch(msg.getMessageType()) {
        case HIT:
            this->checkPredictions(shipPredictors, numShipPredictors, msg.getRow(), msg.getCol(), false);
            board[msg.getRow()][msg.getCol()] = msg.getMessageType();
            this->doPredictions(shipPredictors, numShipPredictors);
            break;
        case KILL:
            board[msg.getRow()][msg.getCol()] = msg.getMessageType();
            break;
        case MISS:
            board[msg.getRow()][msg.getCol()] = msg.getMessageType();
        case DUPLICATE_SHOT:
            this->checkPredictions(shipPredictors, numShipPredictors, msg.getRow(), msg.getCol(), true);
            cerr << "MISS, making new prediction" << endl;
            this->doPredictions(shipPredictors, numShipPredictors);
            break;
        case WIN:
            break;
        case LOSE:
            break;
        case TIE:
            break;
        case OPPONENT_SHOT:
            this->checkPredictions(shotPredictors, numShotPredictors, msg.getRow(), msg.getCol(), false);
            this->doPredictions(shotPredictors, numShotPredictors);
            break;
    }
}

/**
 * @brief Get the predictor in the given array that has made the best preditions so far
 * @param Predictor* predictors[] - the array of Predictor pointers that are all trying to predict the same thing
 * @param int predictorsCount - how many predictors are in the array
 * @return Predictor* - a pointer to the best predictor in the array
 * @throw logic_error - if predictorsCount < 1
 */
Predictor* Plutonium::getBestPredictor(Predictor* predictors[], int predictorsCount) {
    if (predictorsCount < 1) throw logic_error("Predictors count less than 1");
    int max = predictors[0]->getNumCorrect();
    int maxIndex = 0;
    for (int i=0; i<predictorsCount; i++) {
        if (predictors[i]->getNumCorrect() > max) {
            max = predictors[i]->getNumCorrect();
            maxIndex = i;
        }
        cerr << "PREDICTOR #" << i << " has " << predictors[i]->getNumCorrect() << " correct predictions" << endl;
    }
    cerr << "BEST PREDICTOR: " << maxIndex << endl;
    return predictors[maxIndex];
}

/**
 * @brief Runs all of the predictors in the given set of predictors
 * @param Predictor* predictors[] - the array of Predictor pointers
 * @param int predictorsCount - how many predictors are in the array
 * @throw logic_error - if predictorsCount < 1
 */
void Plutonium::doPredictions(Predictor* predictors[], int predictorsCount) {
    if (predictorsCount < 1) throw logic_error("Predictors count less than 1");
    for (int i=0; i<predictorsCount; i++) {
        int pRow;
        int pCol;
        predictors[i]->getNextPrediction(board, boardSize, pRow, pCol);
    }
}

 /**
  * @brief Checks each prediction to see if it was correct
  * @param Predictor* predictors[] - the array of Predictor pointers
  * @param int predictorsCount - how many predictors are in the array
  * @param int actualRow - the actual row to check against
  * @param int actualCol - the actual col to check against
  * @param bool miss - true if the shot we're processing is a miss
  * @throw logic_error - if predictorsCount < 1
  */
void Plutonium::checkPredictions(Predictor* predictors[], int predictorsCount, int actualRow, int actualCol, bool miss) {
    if (predictorsCount < 1) throw logic_error("Predictors count less than 1");
    for (int i=0; i<predictorsCount; i++) {
        int pRow;
        int pCol;
        predictors[i]->getPreviousPrediction(pRow, pCol);
        bool match = (pRow == actualRow && pCol == actualCol);
        if (miss) {
            if (match) {
                // If the predictor picked this spot and it was a miss, inform it of a wrong prediction
                predictors[i]->informCorrect(false);
            }
        } else {
            // If the shot was a hit and the predictor picked this spot, it was right
            if (match) {
                predictors[i]->informCorrect(true);
            }
        }
    }
}
