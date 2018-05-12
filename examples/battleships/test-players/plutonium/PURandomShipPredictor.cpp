#include "PUPredictor.h"

class RandomShipPredictor : public Predictor {
    public:
        RandomShipPredictor() {
            lastRow = 0;
            lastCol = 0;
            numCorrect = 0;
            numShots = 0;
            finishedSweep = false;
        }
        virtual void getPrediction(char board[MAX_BOARD_SIZE][MAX_BOARD_SIZE], int boardSize, int &pRow, int &pCol) {
            int maxProbability = -9999;
            pRow = 0;
            pCol = 0;
            for (int row=0; row<boardSize; row++) {
                for (int col=0; col<boardSize; col++) {
                    int prob = this->getProbabilityForCell(board, boardSize, row, col);
                    if (prob > maxProbability) {
                        pRow = row;
                        pCol = col;
                        maxProbability = prob;
                    }
                }
            }
            cerr << "PREDICTION: " << pRow << " " << pCol << " " << maxProbability << endl;
            if (pRow == 0 && pCol == 0) {
                finishedSweep = true;
            }
            lastRow = pRow;
            lastCol = pCol;
            numShots++;
        }
        virtual void getNextCounter(char board[MAX_BOARD_SIZE][MAX_BOARD_SIZE], int boardSize, int &pRow, int &pCol, int, int&) {
            pRow = lastRow;
            pCol = lastCol;
        }
    private:
        int lastRow;
        int lastCol;
        int numShots;
        bool finishedSweep;
        int getProbabilityForCell(char board[MAX_BOARD_SIZE][MAX_BOARD_SIZE], int boardSize, int row, int col) {
            if (board[row][col] != WATER) {
                // Location is already known; no reason to shoot here
                return 0;
            }
            const int HYPO_SHIP_SIZE = 4;
            int baseProbability = 1; // Reserve 0 for impossible locations
            
            // Horizontal possibilities
            // for condition covers boundary to the left
            for (int i=col; i>=0 && i>col-HYPO_SHIP_SIZE; i--) {
                if (col + HYPO_SHIP_SIZE > boardSize) {
                    // if condition covers boundary to the right
                    continue;
                }
                baseProbability++;
            }


            // Vertical possibilities
            // for condition covers boundary at the top
            for (int i=row; i>=0 && i>row-HYPO_SHIP_SIZE; i--) {
                if (row + HYPO_SHIP_SIZE > boardSize) {
                    // if condition covers boundary at the bottom
                    continue;
                }
                baseProbability++;
            }

            // Adjacent cells
            for (int curRow = row - 1; curRow < row + 2; curRow++) {
                if (curRow < 0 || curRow >= boardSize) continue;

                for (int curCol = col - 1; curCol < col + 2; curCol++) {
                    if (curCol < 0 || curCol >= boardSize) continue;

                    if (curRow == row && curCol == col) {
                        // Skip the cell in question
                        continue;
                    }
                    if (curRow != row && curCol != col) {
                        // Skip diagonals
                        continue;
                    }
                    if (board[curRow][curCol] == MISS) {
                        // Miss in same row or col as cell in question; less probable
                        baseProbability-=10;
                    }
                    if (board[curRow][curCol] == KILL) {
                        // Kill in same row or col as cell in question; less probable
                        if (! finishedSweep) {
                            // If already swept whole board, be less picky
                            baseProbability-=10;
                        }
                    }
                    if (board[curRow][curCol] == HIT) {
                        // Hit in same row or col as cell in question; more probable
                        baseProbability+=20;
                        if (curRow < row && curRow - 1 > 0 && board[curRow - 1][curCol] == HIT) {
                            // More probable if two consecutive (up) are hits
                            baseProbability+=5;
                        }
                        if (curRow > row && curRow + 1 < boardSize && board[curRow + 1][curCol] == HIT) {
                            // More probable if two consecutive (down) are hits
                            baseProbability+=5;
                        }
                        if (curCol < col && curCol - 1 > 0 && board[curRow][curCol - 1] == HIT) {
                            // More probable if two consecutive (left) are hits
                            baseProbability+=5;
                        }
                        if (curCol > col && curCol + 1 < boardSize && board[curRow][curCol + 1] == HIT) {
                            // More probable if two consecutive (right) are hits
                            baseProbability+=5;
                        }
                    }
                    if (curRow < row && board[curRow][curCol] == HIT && row < boardSize / 3) {
                        // Emphasize going up if we're on top of the board
                        baseProbability+=1;
                    }
                    if (curCol < col && board[curRow][curCol] == HIT && col < boardSize / 3) {
                        // Emphasize going right if we're on the left of the board
                        baseProbability+=1;
                    }
                }
            }

            // De-emphasize upper-left slightly (for late game)
            if (row < boardSize / 2 && col < boardSize / 2) {
                baseProbability-=1;
            }

            return baseProbability;
        }
};
