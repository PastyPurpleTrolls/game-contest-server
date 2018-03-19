#include <iostream>
#include <cstdlib>
#include <string>

#include "socketstream.h"
#include "defines.h"
#include "Message.h"
#include PLAYER_H

#include <csignal>
sig_atomic_t last_wait;

const int boardSize = 10;

void send_result(const Message& msg, net::socketstream& referee) {
    referee << msg.getMessageType() << " "
	    << msg.getRow() << " "
	    << msg.getCol() << " "
	    << msg.getDirection() << " "
	    << msg.getLength() << " "
	    << msg.getString() << std::endl;
}

int main(int argc, char **argv) {
    srand(time(NULL));

    net::socketstream referee(argv[1]);

    referee << argv[2] << std::endl;

    while (1) {
	PLAYER player(boardSize);

	bool done = false;
	char messageType;
	int row, col, length;
	Direction dir;

	while (   !done
	       && referee >> messageType >> row >> col >> dir >> length)
	{
	    std::string str;
	    std::getline(referee, str);

	    switch (messageType) {
	      case WIN:
	      case LOSE:
	      case TIE:
	      case QUIT:
		done = true;
		break;

	      case MOVE_REQUEST:
		send_result(player.getMove(), referee);
		break;

	      case PLACE_SHIP_REQUEST:
		send_result(player.placeShip(length), referee);
		break;

	      case NEW_ROUND:
		player.newRound();
		break;

	      default:
		player.update(Message(messageType, row, col, str));
	    }
	}

	if (!done) {
	    return 0;
	}
    }
}
