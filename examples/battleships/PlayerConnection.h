#ifndef PLAYER_CONNECTION_H
#define PLAYER_CONNECTION_H

#include "socketstream.h"
#include "Message.h"

class PlayerConnection {
    net::socketstream *stream;
    std::string name;
    int kills;

  public:
    PlayerConnection(net::socketstream* in_stream, int boardSize);
    void newRound();
    void update(Message msg);
    Message placeShip(int length);
    Message getMove();

    std::string get_name() const;

    void inc_kills();
    int get_kills() const;

  private:
    Message getMessage() const;
    void sendMessage(Message msg);
};

#endif
