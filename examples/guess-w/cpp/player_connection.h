#ifndef PLAYER_CONNECTION_H
#define PLAYER_CONNECTION_H

#include "socketstream.h"

class PlayerConnection {
    net::socketstream *stream;
    std::string name;
    bool won;
    double score;

  public:
    PlayerConnection(net::socketstream* in_stream);
    std::string getline() const;
    void sendline(std::string line);

    void set_won();
    void clear_won();
    void set_score(double new_score);

    double get_score() const;
    std::string get_results() const;
    std::string get_name() const;
};

#endif
