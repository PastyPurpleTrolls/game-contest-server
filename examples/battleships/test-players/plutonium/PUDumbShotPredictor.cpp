#include "PUPredictor.h"

class DumbShotPredictor : public Predictor {
    public:
        DumbShotPredictor() {
            lastCounterRow = -1;
            lastCounterCol = -1;
        }
        virtual void getPrediction(char board[MAX_BOARD_SIZE][MAX_BOARD_SIZE], int boardSize, int &pRow, int &pCol) {
            lastCol++;
            if (lastCol >= boardSize) {
                lastCol = 0;
                lastRow++;
            }
            if (lastRow >= boardSize) {
                lastCol = 0;
                lastRow = 0;
            }
            pRow = lastRow;
            pCol = lastCol;
        }
        virtual void getNextCounter(char board[MAX_BOARD_SIZE][MAX_BOARD_SIZE], int boardSize, int &pRow, int &pCol, int shipLength, int &direction) {
            // Place ships along bottom
            if (lastCounterRow == -1) lastCounterRow = boardSize - 1;
            if (lastCounterCol == -1) lastCounterCol = boardSize;
            direction = (int)Horizontal;
            if (lastCounterCol - shipLength < 0) {
                // If ship is too large to fit on this row, go up one
                lastCounterRow--;
                lastCounterCol = boardSize - shipLength;

                pRow = lastCounterRow;
                pCol = lastCounterCol;

                return;
            } else {
                // If ship can fit on current row, place it
                lastCounterCol -= shipLength;
                
                pRow = lastCounterRow;
                pCol = lastCounterCol;
                
                return;
            }
        }
    private:
        int lastRow;
        int lastCol;
        int lastCounterRow;
        int lastCounterCol;
};
