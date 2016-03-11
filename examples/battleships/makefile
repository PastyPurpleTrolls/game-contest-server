AITesterMain = AIContest.o
AIContestMain = contest.o

objects = AIContest.o BoardV2.o Message.o PlayerV1.o \
	CleanPlayer.o OrigGamblerPlayer.o HumanPlayer.o
	
contest : $(AIContestMain) $(objects)
	g++ -o contest $(AIContestMain) $(objects)

clean:
	rm -f contest $(objects) 

