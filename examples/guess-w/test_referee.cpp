#include <iostream>
#include <cstdlib>
#include <string>
#include <vector>

#include "socketstream.h"
#include "player_connection.h"

void display_results(std::string result_type,
		     net::socketstream& manager,
		     std::vector<PlayerConnection>& players)
{
    manager << result_type << ":end" << std::endl;

    for (auto player : players) {
	manager << result_type << "result:";
	manager << player.get_results() << std::endl;
    }
}

void run_game(net::socketstream& manager,
	      std::vector<PlayerConnection>& players)
{
    manager << "round:start|{}" << std::endl;
    for (auto& player : players) {
	player.clear_won();
    }

    std::string buffer;
    std::string winner;
    bool done = false;
    for (int i = 0; !done; ++i) {
	for (auto& player : players) {
	    player.sendline("move");

	    buffer = player.getline();

	    manager << "move: turn " << i << " is " << buffer;
	    manager << "|{player: \"" << player.get_name() << "\", ";
	    manager << "value: \"" << buffer << "\", ";
	    manager << "win: \"" << (buffer == "w") << "\"}" << std::endl;

	    if (buffer == "w") {
		winner = player.get_name();
		player.set_won();
		player.set_score(player.get_score() + 1.0);
		done = true;
		break;
	    }
	}
    }

    for (auto player : players) {
	player.sendline(winner + " wins!");
    }

    display_results("round", manager, players);
}

int main(int argc, char **argv) {
    net::socketstream manager("localhost", std::atoi(argv[1]));
    net::server referee;

    manager << "port:" << referee.get_port() << std::endl;
    manager << "match:start" << std::endl;

    int num_players = std::atoi(argv[2]);
    std::vector<PlayerConnection> players;
    for (int i = 0; i < num_players; ++i) {
	players.push_back(PlayerConnection(referee.serve()));
    }

    for (int i = 0; i < std::atoi(argv[3]); ++i) {
	run_game(manager, players);
    }

    display_results("match", manager, players);

    return 0;
}
