#include "PUPredictor.h"

class DumbShipPredictor : public Predictor {
    public:
        DumbShipPredictor() {
            lastRow = 0;
            lastCol = 0;
        }
        virtual void getPrediction(char board[MAX_BOARD_SIZE][MAX_BOARD_SIZE], int boardSize, int &pRow, int &pCol) {
            if (lastCol + 1 <= MAX_SHIP_SIZE && (lastWasCorrect || lastRow == 0)) {
                // Guess horizontally as long as we keep making hits
                lastCol++;
                pRow = lastRow;
                pCol = lastCol;
            } else {
                // Either we missed or exceeded MAX_SHIP_SIZE; move on to next row
                lastCol = 0;
                lastRow++;
                if (lastRow >= boardSize) {
                    // Ran out of rows.  At this point, we SHOULD have hit every ship if this is the dumb player
                    lastRow = 0;
                    lastCol = 0;
                }
                pRow = lastRow;
                pCol = lastCol;
            }
            cerr << "DUMB PREDICTION: " << pRow << " " << pCol << endl;
        }
        virtual void getNextCounter(char board[MAX_BOARD_SIZE][MAX_BOARD_SIZE], int boardSize, int &pRow, int &pCol, int, int&) {
            pRow = lastRow;
            pCol = lastCol;
        }
    private:
        int lastRow;
        int lastCol;
};
