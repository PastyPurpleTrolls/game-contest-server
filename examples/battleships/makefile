AIContestMain = contest.o

include cpp-player.mk

CXXFLAGS += -std=gnu++11 -g -DPLAYER=$(Player) -DPLAYER_H=\"$(Player).h\"
CC = $(CXX)

objects = AIContest.o BoardV3.o Message.o PlayerV2.o PlayerConnection.o

contest : $(AIContestMain) $(objects)
	g++ -o contest $(AIContestMain) $(objects)

player: player.o PlayerV2.o $(Player).o Message.o
player.o: player.cpp socketstream.h
$(Player).o: $(Player).cpp socketstream.h

clean:
	rm -f contest $(AIContestMain) $(objects)

