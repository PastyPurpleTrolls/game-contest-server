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

void PlayerConnection::update(Message msg) const {
    sendMessage(msg);
}

Message PlayerConnection::placeShip(int length) const {
    sendMessage(Message(PLACE_SHIP_REQUEST, -1, -1, "", None, length));
    return getMessage();
}

Message PlayerConnection::getMove() const {
    sendMessage(Message(MOVE_REQUEST));
    return getMessage();
}

Message PlayerConnection::getMessage() const {
    Message msg(INVALID_SHOT);
    *stream >> msg;

    return msg;
}

void PlayerConnection::sendMessage(Message msg) const {
    *stream << msg;
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
