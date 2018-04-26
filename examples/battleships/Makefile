.PRECIOUS: %.o
.PHONY: run contest manager clean

AIContestMain = referee.o

ifeq ($(wildcard cpp-player.mk),)
    Player =
else
    include cpp-player.mk
endif

CXXFLAGS += -std=gnu++11 -ggdb -O3 -DPLAYER=$(Player) -DPLAYER_H=\"$(Player).h\"
LDFLAGS += -ggdb
CC = $(CXX)

objects = AIContest.o BoardV3.o conio.o Message.o PlayerV2.o PlayerConnection.o

referee: $(AIContestMain) $(objects)
referee.o: referee.cpp AIContest.h PlayerConnection.h socketstream.h
AIContest.o: AIContest.cpp BoardV3.h PlayerConnection.h socketstream.h

conio.o: conio.h conio.cpp
player: player.o $(Player).o $(objects)
player.o: player.cpp socketstream.h
$(Player).o: $(Player).cpp socketstream.h

clean:
	rm -f contest $(AIContestMain) $(objects)

manager:
	nc -lU $(path)

run: referee
	./referee $(path) $(num_players) $(num_rounds) $(max_time)

contest: contest_compile
	./player $(path) '$(name)'

contest_compile: player
