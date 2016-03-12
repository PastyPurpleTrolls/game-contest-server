CXXFLAGS += -std=gnu++11 -g
CC = $(CXX)

AIContestMain = contest.o

objects = AIContest.o BoardV3.o Message.o PlayerV2.o PlayerConnection.o \
	CleanPlayerV2.o OrigGamblerPlayerV2.o HumanPlayer.o \
	DumbPlayerV2.o GamblerPlayerV2.o
	
contest : $(AIContestMain) $(objects)
	g++ -o contest $(AIContestMain) $(objects)

player: player.o PlayerV2.o DumbPlayerV2.o Message.o socketstream.h

clean:
	rm -f contest $(AIContestMain) $(objects)

