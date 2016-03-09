#include <string>

#include "player_connection.h"

PlayerConnection::PlayerConnection(net::socketstream* in_stream)
    : stream(in_stream), won(false), score(0.0)
{
    name = getline();
}

std::string PlayerConnection::getline() const {
    std::string buffer;
#if defined(USE_TELNET)
    std::getline(*stream, buffer, '\r');
    stream->ignore(1);
#else
    std::getline(*stream, buffer);
#endif

    return buffer;
}

void PlayerConnection::sendline(std::string line) {
    *stream << line << std::endl;
}

void PlayerConnection::set_won() {
    won = true;
}

void PlayerConnection::clear_won() {
    won = false;
}

double PlayerConnection::get_score() const {
    return score;
}

void PlayerConnection::set_score(double new_score) {
    score = new_score;
}

std::string PlayerConnection::get_results() const {
    std::string result = name;
    result += "|";
    if (won) {
	result += "Win";
    } else {
	result += "Loss";
    }
    result += "|";
    result += std::to_string(score);

    return result;
}

std::string PlayerConnection::get_name() const {
    return name;
}
