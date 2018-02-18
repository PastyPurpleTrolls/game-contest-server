.PRECIOUS: %.o
.PHONY: run contest manager clean

CXXFLAGS += -std=gnu++11
CC = $(CXX)

include cpp-player.mk

manager:
	nc -l -p $(port)

run: test_referee
	./test_referee $(port) $(num_players) $(num_rounds) $(max_time)

test_referee: test_referee.o player_connection.o
test_referee.cpp: socketstream.h player_connection.h
player_connection.cpp: player_connection.h socketstream.h

contest: $(PLAYER)
	./$(PLAYER) $(port) '$(name)' 1

$(PLAYER): $(PLAYER).o
$(PLAYER).cpp: socketstream.h

clean:
	rm -f test_referee test_player *.o
