/**
 * Message.h: Defines a primitive message class.
 * Authors:   Stefan Brandle and Jonathan Geisler
 * Date:      December 2004
 */

#include <string>
#include "defines.h"

using namespace std;

#ifndef MESSAGE_H		// Double inclusion protection
#define MESSAGE_H

class Message {
    public:
	Message( char messageType );              // Constructors
	Message( char messageType, int row, int col, string str );
	Message( char messageType, int row, int col, string str, Direction direction, int length );

	// General set function
	void setMessage( char messageType, int row, int col, string str, Direction dir, int length );

	void setMessageType( char messageType );  // set/get message type functions
	char getMessageType( ) const;

	void setRow( int row );                   // set/get row functions
	int getRow( ) const;

	void setCol( int col );                   // set/get column functions
	int getCol( ) const;

	void setString( string str );             // set/get string functions
	string getString( ) const;

	void setDirection( Direction dir );       // set/get direction functions
	Direction getDirection( ) const;

	void setLength( int length );       // set/get length functions
	int getLength( ) const;

    private:
        char messageType;                         // Fields
        int row;
        int col;
	int length;
        string str;
	Direction dir;
};

ostream& operator<<(ostream& stream, const Message& msg);
istream& operator>>(istream& stream, Message& msg);

#endif
