#include <iostream>
#include <cstdio>
#include <fstream>
#include <iomanip>

#include "JJplayer.h"

/**
 * @brief Constructor that initializes any inter-round data structures.
 * @param boardSize Indication of the size of the board that is in use.
 *
 * The constructor runs when the AI is instantiated (the object gets created)
 * and is responsible for initializing everything that needs to be initialized
 * before any of the rounds happen. The constructor does not get called
 * before rounds; newRound() gets called before every round.
 */
JJplayer::JJplayer( int boardSize )
    :PlayerV2(boardSize) {
    //Initialize learnDefBoard, learnOffBoard, and pattern
    int offset=1;
    for(int row = 0; row < boardSize; row++) {
        for(int col = 0; col < boardSize; col++) {
            learnDefBoard[row][col]=0;
            learnOffBoard[row][col]=0;
            if ((col+offset)%3==0) {
                pattern[row][col]=SHOT;
            }
        }
        offset++;
        if (offset>3) offset=1;
    }
    scatter=0;
//    dout.open("ResultsDebugging");
}

void JJplayer::newRound() {
    numShipsPlaced = 0;
    numKills = 0;
    newKills = 0;
    numHits  = 0;
    sinceHit = 0;
    for(int row = 0; row < boardSize; row++){
        for(int col = 0; col < boardSize; col++){
            defGameBoard[row][col] = WATER;
            offGameBoard[row][col] = WATER;
        }
    }
    for (int i=0;i<NumShips;i++) shipsArray[i]=(i%3)+3;
    calcBaseProbability();
}

void JJplayer::update(Message msg) {
    switch(msg.getMessageType()) {
        case KILL:
            newKills++;
            sinceHit=0;
            offGameBoard[msg.getRow()][msg.getCol()]=KILL;
            break;
        case HIT:
            numHits++;
            sinceHit=0;
            offGameBoard[msg.getRow()][msg.getCol()]=HIT;
            break;
        case MISS:
            offGameBoard[msg.getRow()][msg.getCol()]=MISS;
            sinceHit++;
            break;
        case WIN:
        case LOSE:
        case TIE:
            for(int row = 0; row < boardSize; row++) {
                for(int col = 0; col < boardSize; col++) {
                    if (offGameBoard[row][col]==HIT || offGameBoard[row][col]==KILL) {
                        learnOffBoard[row][col]+=1;
                    }
                }
            }
            if (stats.totalRounds<12) {
                stats.totalRounds++;
                switch (msg.getMessageType()) {
                    case WIN:
                        if (stats.totalRounds%2==0) stats.evenWins++;
                        else stats.oddWins++;
                    case LOSE:
                        if (stats.totalRounds%2==0) stats.evenLosses++;
                        else stats.oddLosses++;
                    case TIE:
                        if (stats.totalRounds%2==0) stats.evenTies++;
                        else stats.oddTies++;
                }
                if (stats.totalRounds==12) {
                    int evenScore=stats.evenWins+stats.oddLosses;
                    int oddScore=stats.oddWins+stats.evenLosses;
                    if (oddScore>evenScore) {
                        scatter=1;
                    } else {
                        scatter=2;
                    }
/*                    dout<<"Scatter: "<<scatter<<endl
                        <<"Even w/l: "<<stats.evenWins << " " << stats.evenLosses<< endl
                        <<"Odd w/l: "<<stats.oddWins << " " << stats.oddLosses<<endl;*/
                }
            }
        case OPPONENT_SHOT:
            learnDefBoard[msg.getRow()][msg.getCol()]+=10;
            break;
    }
}

Message JJplayer::getMove() {
//    dout<<"In getMove:"<<endl;
    if (newKills>0) {
        numHits-=newKills;
        numKills+=newKills;
        for (int i=0; i<NumShips; i++) {
            if (shipsArray[i]==newKills) {
                shipsArray[i]=0;
                break;
            }
        }
        newKills=0;
    }
//    dout<< "numHits: " << numHits<<endl;
    if (numHits==0) {
        huntMode();
        sinceHit++;
    } else {
        targetMode(numHits);
    }

    Message result(SHOT, rowToShoot, colToShoot, "Bang", None, 1);
    return result;
}

void JJplayer::huntMode() {
    int current;
    int minVal=baseProbBoard[0][0]+learnOffBoard[0][0];
    int maxVal=baseProbBoard[0][0]+learnOffBoard[0][0];
    for(int row = 0; row < boardSize; row++) {
        for(int col = 0; col < boardSize; col++) {
            current=baseProbBoard[row][col]+learnDefBoard[row][col];
            if (current<minVal) minVal=current;
            if (current>maxVal) maxVal=current;
        }
    }
    int targetVal=maxVal;
    if ((scatter==0 && stats.totalRounds%2==1 && sinceHit%5==0) ||
        (scatter==1 && sinceHit%5==0)) {
        int val=sinceHit;
        if (val>15) val=15;
        targetVal=minVal+((maxVal-minVal)*(4-(val/5))*0.3);
    }

    rowToShoot=0;
    colToShoot=0;
    for(int row = 0; row < boardSize; row++) {
        for(int col = 0; col < boardSize; col++) {
            if (pattern[row][col]==SHOT &&
                offGameBoard[row][col] == WATER &&
                baseProbBoard[row][col]+learnOffBoard[row][col] >
                baseProbBoard[rowToShoot][colToShoot]+learnOffBoard[rowToShoot][colToShoot] &&
                baseProbBoard[row][col]+learnOffBoard[row][col] <= targetVal) {
                    rowToShoot = row;
                    colToShoot = col;
            }
        }
    }

    return;
}

void JJplayer::targetMode(int numHits) {
//    dout <<"In targetMode:"<<endl;
    bool valid;
    int length;
    int hitRow;
    int hitCol;
    int otherHits=0;
    int maxSoFar=0;
    int targetMap[boardSize][boardSize];
    struct Shot { int row; int col; };
    Shot* hitList[numHits];

    for (int row=0, i=0; row<boardSize; row++) {
        for (int col=0; col<boardSize; col++) {
            targetMap[row][col]=0;
            if (offGameBoard[row][col]==HIT) {
                hitList[i]=new Shot;
                hitList[i]->row=row;
                hitList[i]->col=col;
                i++;
            }
        }
    }

    for (int i=0; i<numHits; i++) {
//        dout<<" Hit "<<i+1<<endl;
        hitRow=hitList[i]->row;
        hitCol=hitList[i]->col;
        for (int j=0; j<NumShips; j++) {
            length=shipsArray[j];
            if (length!=0) {
//                dout<<"  Length "<<length<<endl;
                //Horizontal
                for (int startCol=hitCol-length+1; startCol<=hitCol; startCol++) {
                    valid=true;
                    otherHits=-1;
                    for (int colOffset=0; colOffset<length; colOffset++) {
                        if (hitRow<0 || hitRow>=boardSize) valid=false;
                        else if ((startCol+colOffset)<0 || (startCol+colOffset)>=boardSize) valid=false;
                        else if (offGameBoard[hitRow][startCol+colOffset]==MISS) valid=false;
                        else if (offGameBoard[hitRow][startCol+colOffset]==KILL) valid=false;
                        else if (offGameBoard[hitRow][startCol+colOffset]==HIT) otherHits++;
                    }
                    if (valid) {
                        for (int colOffset=0; colOffset<length; colOffset++) {
                            targetMap[hitRow][startCol+colOffset]++;
                            targetMap[hitRow][startCol+colOffset]+=(otherHits*3);
                        }
                    }
                }

                //Vertical
                for (int startRow=hitRow-length+1; startRow<=hitRow; startRow++) {
                    valid=true;
                    otherHits=-1;
                    for (int rowOffset=0; rowOffset<length; rowOffset++) {
                        if ((startRow+rowOffset)<0 || (startRow+rowOffset)>=boardSize) valid=false;
                        else if (hitCol<0 || hitCol>=boardSize) valid=false;
                        else if (offGameBoard[startRow+rowOffset][hitCol]==MISS) valid=false;
                        else if (offGameBoard[startRow+rowOffset][hitCol]==KILL) valid=false;
                        else if (offGameBoard[startRow+rowOffset][hitCol]==HIT) otherHits++;
                    }
                    if (valid) {
                        for (int rowOffset=0; rowOffset<length; rowOffset++) {
                            targetMap[startRow+rowOffset][hitCol]++;
                            targetMap[startRow+rowOffset][hitCol]+=(otherHits*3);
                        }
                    }
                }
            }
        }
    }

    for (int row=0; row<boardSize; row++) {
        for (int col=0; col<boardSize; col++) {
            switch (offGameBoard[row][col]) {
                case HIT:  targetMap[row][col]=-1; break;
                case KILL: targetMap[row][col]=-2; break;
                case MISS: targetMap[row][col]=-3; break;
            }
            if (targetMap[row][col]>=maxSoFar){
                maxSoFar=targetMap[row][col];
                rowToShoot=row;
                colToShoot=col;
            }
        }
    }

    for (int i=0; i<numHits; i++) delete hitList[i];
/*
    dout<<" Loc: "<<rowToShoot<<" "<<colToShoot<<endl;
    dout<<" Max: "<<maxSoFar<<endl<<" ";
    for (int row=0; row<boardSize; row++) {
        for (int col=0; col<boardSize; col++) {
            dout<<setw(2)<<targetMap[row][col]<<" ";
        }
        dout<<endl<<" ";
    }
    dout<<endl;
*/
    return;
}

Message JJplayer::placeShip(int length) {
    int chancesPerShip;
    int HoV;
    int bestArray[4]={0,0,0,0};
    bool firstTime=true;
    bool bad=false;

    HoV=1;
    for (int row=0; row<boardSize; row++) {
        for (int col=0; col<=boardSize-length; col++) {
            bad=false;
            chancesPerShip=0;
            for (int colOffset=0; colOffset<length; colOffset++) {
                chancesPerShip+=baseProbBoard[row][col+colOffset]+learnDefBoard[row][col+colOffset];
                if (defGameBoard[row][col+colOffset]==SHIP) bad=true;
            }
            if (!bad && (firstTime || chancesPerShip<=bestArray[0])) {
                if (firstTime) firstTime=false;
                bestArray[0]=chancesPerShip;
                bestArray[1]=HoV;
                bestArray[2]=row;
                bestArray[3]=col;
            }
        }
    }

    HoV=2;
    for (int row=0; row<=boardSize-length; row++) {
        for (int col=0; col<boardSize; col++) {
            bad=false;
            chancesPerShip=0;
            for (int rowOffset=0; rowOffset<length; rowOffset++) {
                chancesPerShip+=baseProbBoard[row+rowOffset][col]+learnDefBoard[row+rowOffset][col];
                if (defGameBoard[row+rowOffset][col]==SHIP) bad=true;
            }
            if (!bad && (chancesPerShip<=bestArray[0])) {
                bestArray[0]=chancesPerShip;
                bestArray[1]=HoV;
                bestArray[2]=row;
                bestArray[3]=col;
            }
        }
    }

    shipsArray[numShipsPlaced]=length;

    int row=bestArray[2];
    int col=bestArray[3];
/*    dout << "Chances: " << bestArray[0]
         << " HoV: " << bestArray[1]
         << " Row: " << row
         << " Col: " << col << endl;
*/
    if (bestArray[1]==1){
        for (int colOffset=0; colOffset<length; colOffset++) {
            defGameBoard[row][col+colOffset]=SHIP;
        }
    } else {
        for (int rowOffset=0; rowOffset<length; rowOffset++) {
            defGameBoard[row+rowOffset][col]=SHIP;
        }
    }

/*    dout<<"PlaceShip:"<<endl;
    for (int row=0; row<boardSize; row++) {
        for (int col=0; col<boardSize; col++) {
            dout<<defGameBoard[row][col]<<" ";
        }
        dout<<endl;
    }
    dout<<endl;
*/
    Direction dir=Direction(bestArray[1]);

    char shipName[10];
    // Create ship names each time called: Ship0, Ship1, Ship2, ...
    snprintf(shipName, sizeof shipName, "Ship%d", numShipsPlaced);

    // parameters = mesg type (PLACE_SHIP), row, col, a string, direction (Horizontal/Vertical)
    Message response( PLACE_SHIP, bestArray[2], bestArray[3], shipName, dir, length );
    numShipsPlaced++;

    return response;
}

void JJplayer::calcBaseProbability() {
    //Initialize all to zero
    for (int row=0; row<boardSize; row++) {
        for (int col=0; col<boardSize; col++) {
            baseProbBoard[row][col]=0;
        }
    }

    //cout << "Calculating: ";
    for (int i=0; i<NumShips; i++) {
        int shipLength=shipsArray[i];
        if (shipLength <= boardSize) {
            //cout << "Horizontal: ";
            for (int row=0; row<boardSize; row++) {
                for (int col=0; col<=boardSize-shipLength; col++) {
                    for (int colOffset=0; colOffset<shipLength; colOffset++) {
                        baseProbBoard[row][col+colOffset]++;
                    }
                }
            }
            //cout << "Vertical: ";
            for (int row=0; row<=boardSize-shipLength; row++) {
                for (int col=0; col<boardSize; col++) {
                    for (int rowOffset=0; rowOffset<shipLength; rowOffset++) {
                        baseProbBoard[row+rowOffset][col]++;
                    }
                }
            }
        }
    }
}


