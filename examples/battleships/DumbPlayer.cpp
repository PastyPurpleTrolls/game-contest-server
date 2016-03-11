/**
 * @author Stefan Brandle, Jonathan Geisler
 * @date September, 2004
 *
 * Please type in your name[s] here:
 * Kyle Bavender
 */

#include <iostream>

using namespace std;

#include "DumbPlayer.h"

DumbPlayer::DumbPlayer( int boardSize ):
    PlayerV1(boardSize)
{
    //this->boardSize = boardSize;
    lastRow = 0;
    lastCol = -1;
}

DumbPlayer:: ~DumbPlayer()
{
	delete[]board;
}

/**
 * Gets the computer's shot choice. This is then returned to the caller.
 * @return Message The most important parts of the returned message are 
 * the row and column values. 
 * Position 0 of the int array should hold the row, position 1 the column.
 */
Message DumbPlayer::getMove() 
{
	// Checks if last shot was hit to hunt down the rest
	if( board[lastRow][lastCol] == HIT)
	{
		huntRow = lastRow;
		huntCol = lastCol;
		hunter(lastRow,lastCol,huntRow,huntCol);
//		hunter(row, col ... )  <-- from notes
		Message result( SHOT, huntRow, huntCol, "Bang" );
		return result;
	}

    lastCol = lastCol + 3;
    if( lastCol >= boardSize ) 
	{
		lastCol = lastCol - boardSize;
		// Special condition for board sizes of 3x
		if ( boardSize % 3 == 0 ) lastCol--;
		lastRow++;
    }
    if( lastRow >= boardSize ) 
	{
		lastCol = 0;
		lastRow = 0;
    }

    Message result( SHOT, lastRow, lastCol, "Bang" );
    return result;
}



void DumbPlayer :: hunter(int startRow, int startCol, 
						  int &shotRow, int &shotCol)
{
	if (goNorth(startRow,startCol,shotRow,shotCol))
		return;
	else if (goSouth(startRow,startCol,shotRow,shotCol))
		return;
	else if (goEast(startRow,startCol,shotRow,shotCol))
		return;
	else if (goWest(startRow,startCol,shotRow,shotCol))
		return;	

//	else call scanner  <-- from notes

	cout << endl << "Not N,E,S, or W!!" << endl << endl;
}



bool DumbPlayer :: goNorth (int startRow, int startCol,
							int &shotRow, int &shotCol)
{
	for (int i = 1; (startRow-i >= 0) && (i <= MAX_SHIPSIZE); i++)
	{
		switch( board[startRow-i][startCol] )
		{
			case WATER:
					shotRow = startRow - i;
					shotCol = startCol;
					return true;
					break;
			case MISS:
			case KILL:
					return false;
					break;
			case HIT:
					break;		// keep the loop going
		}
	}
	return false;
}




bool DumbPlayer :: goEast (int startRow, int startCol,
							int &shotRow, int &shotCol)
{
	for (int i = 1; (startCol+i < boardSize) && (i <= MAX_SHIPSIZE); i++)
	{
		switch( board[startRow][startCol+i] )
		{
			case WATER:
					shotRow = startRow;
					shotCol = startCol + i;
					return true;
					break;
			case MISS:
			case KILL:
					return false;
					break;
			case HIT:
					break;		// keep the loop going
		}
	}
	return false;
}





bool DumbPlayer :: goSouth (int startRow, int startCol,
							int &shotRow, int &shotCol)
{
	for (int i = 1; (startRow+i < boardSize) && (i <= MAX_SHIPSIZE); i++)
	{
		switch( board[startRow+i][startCol] )
		{
			case WATER:
					shotRow = startRow + i;
					shotCol = startCol;
					return true;
					break;
			case MISS:
			case KILL:
					return false;
					break;
			case HIT:
					break;		// keep the loop going
		}
	}
	return false;
}





bool DumbPlayer :: goWest (int startRow, int startCol,
							int &shotRow, int &shotCol)
{
	for (int i = 1; (startCol-i >= 0) && (i <= MAX_SHIPSIZE); i++)
	{
		switch( board[startRow][startCol - i] )
		{
			case WATER:
					shotRow = startRow;
					shotCol = startCol - i;
					return true;
					break;
			case MISS:
			case KILL:
					return false;
					break;
			case HIT:
					break;		// keep the loop going
		}
	}
	return false;	// ASK  <-- is this in the right place?
}



// Functions to be added
// ---------------------
//
//
// From notes, yet...ehhh?
// -----------------------
// bool DumbPlayer :: genericHunter(startR,startC,shotR,
// 									shotC,delta X, delta Y)
