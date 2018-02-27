#ifndef PU_PREDICTOR_H
#define PU_PREDICTOR_H

class Predictor {
    public:
        Predictor() {
            this->numCorrect = 0;
            this->lastWasCorrect = false;
            this->lastPredictionRow = 0;
            this->lastPredictionCol = 0;
        }

        virtual void getNextPrediction(char board[MAX_BOARD_SIZE][MAX_BOARD_SIZE], int boardSize, int &pRow, int &pCol) {
            this->getPrediction(board, boardSize, pRow, pCol);
            this->lastPredictionRow = pRow;
            this->lastPredictionCol = pCol;
        }
        virtual void getPreviousPrediction(int &pRow, int &pCol) {
            pRow = this->lastPredictionRow;
            pCol = this->lastPredictionCol;
        }
        virtual void getNextCounter(char board[MAX_BOARD_SIZE][MAX_BOARD_SIZE], int boardSize, int &pRow, int &pCol, int addlParam, int &addlOut) = 0;
        virtual void reset() {

        }

        virtual void informCorrect(bool correct) {
            if (correct)
                this->numCorrect++;
            else
                this->numCorrect--;
            this->lastWasCorrect = correct;
        }
        virtual int getNumCorrect() {
            return this->numCorrect;
        }
    protected:
        int numCorrect;
        int lastPredictionRow;
        int lastPredictionCol;
        bool lastWasCorrect;
        virtual void getPrediction(char board[MAX_BOARD_SIZE][MAX_BOARD_SIZE], int boardSize, int &pRow, int &pCol) = 0;
};

#endif
