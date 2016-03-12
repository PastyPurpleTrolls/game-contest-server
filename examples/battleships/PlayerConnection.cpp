#include <string>

#include "PlayerConnection.h"

PlayerConnection::PlayerConnection(net::socketstream* in_stream, int boardSize)
    : stream(in_stream), kills(0)
{
    std::getline(*stream, name);
}

void PlayerConnection::newRound() {
    sendMessage(Message(NEW_ROUND));
    kills = 0;
}

void PlayerConnection::update(Message msg) {
    sendMessage(msg);
}

Message PlayerConnection::placeShip(int length) {
    sendMessage(Message(PLACE_SHIP_REQUEST, -1, -1, "", None, length));
    return getMessage();
}

Message PlayerConnection::getMove() {
    sendMessage(Message(MOVE_REQUEST));
    return getMessage();
}

Message PlayerConnection::getMessage() const {
    char messageType;
    int row, col, length;
    Direction dir;
    std::string str;

    *stream >> messageType >> row >> col >> dir >> length;
    std::getline(*stream, str);

    return Message(messageType, row, col, str, dir, length);
}

void PlayerConnection::sendMessage(Message msg) {
    *stream << msg.getMessageType() << " "
	    << msg.getRow() << " "
	    << msg.getCol() << " "
	    << msg.getDirection() << " "
	    << msg.getLength() << " "
	    << msg.getString() << std::endl;
}

void PlayerConnection::inc_kills() {
    ++kills;
}

int PlayerConnection::get_kills() const {
    return kills;
}

std::string PlayerConnection::get_name() const {
    return name;
}
