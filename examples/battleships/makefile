AIContestMain = contest.o
Player = CleanPlayerV2

CXXFLAGS += -std=gnu++11 -g -DPLAYER=$(Player) -DPLAYER_H=\"$(Player).h\"
CC = $(CXX)

objects = AIContest.o BoardV3.o Message.o PlayerV2.o PlayerConnection.o

contest : $(AIContestMain) $(objects)
	g++ -o contest $(AIContestMain) $(objects)

player: player.o PlayerV2.o $(Player).o Message.o socketstream.h

clean:
	rm -f contest $(AIContestMain) $(objects)

