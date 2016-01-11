#Help - Referees

Referees are the central system for controlling games between players. These pieces of software connect with players via sockets, report game results, and enforce rules.

##Design

Referees may be uploaded as is, or in a `.zip` file that contains the referee and a makefile.

The makefile should implement three actions: manager, run, and contest. For example, a Python referee might have a makefile like this:

```makefile
.PHONY: run contest manager clean

include player.mk

manager:
    nc -l -p $(port)

run: test_referee.rb
    ./test_referee.py -p $(port) -n $(num_players) -r $(num_matches)

contest: $(PLAYER)
    ./$(PLAYER).py -p $(port) -n '$(name)'
```

Further examples can be found on [GitHub](https://github.com/PastyPurpleTrolls/test/tree/master/examples).

Referees should be implemented to support three flags from the game manager.

- `-p`: (int) TCP port to connect to the manager on. The referee must connect and send a player TCP port within 3 seconds of being started.
- `-n`: (int) The number of players that will connect to the referee.
- `-r`: (int) Number of rounds that the referee should run between the players. If your referee does not support rounds, you can ignore the value of this flag.

##Protocol

Referees must communicate with the game manager via a TCP socket. Three main pieces of information are expected: a player TCP port number, results of rounds, final results of match (if rounds are supported). The referee must also send the moves made in each round.

Every 10 moves, the referee should send the game state to the manager.

Commands are sent as key:value pairs. The first `:` in the command is seen as a special character and represents the end of a command name. Everything that follows is interpreted as the value. Pipes `|` represent separation between values that should be parsed.

Do **not** use `|` for any purpose except as a delimiter to represent lists in the protocol. It should not be used in game state representations.

- `port`: (int) TCP port that the players should connect on. This needs to be sent within the first 3 seconds of being started.
- `match`: Values: `start`, `end`. Tell the manager to expect information about the match.
- `round`: Pipe separated double. `start` or `end`. Round start can also contain any data about the round. 
- `move`: Human readable description of the move as well as any round data needed by the visualizer. Data should be formatted in JSON to make parsing easier. 
- `gamestate`: Implementation dependant value. Sent every 10 moves to represent the current state of the game. To ease parsing in the browser, please use JSON.
- `roundresult`: Sent directly after `round:end`. Pipe separated tuple with player name, result, and score. Score is implementation dependant. Result can only be `Win`, `Loss`, and `Tie`.
- `matchresult`: Sent directly after `match:end`. Pipe separated tuple with player name, result, and rounds won. 

####Example communication

```
port:2222
match:start
round:start|{}
move:description|movedata
gamestate:{}
round:end
roundresult:playername|result|score
roundresult:playername|result|score
match:end
matchresult:playername|result|roundswon
matchresult:playername|result|roundswon
```
