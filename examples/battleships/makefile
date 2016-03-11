AITesterMain = AIContest.o
AIContestMain = contest.o

objects = AIContest.o BoardV3.o Message.o PlayerV2.o \
	CleanPlayerV2.o OrigGamblerPlayerV2.o HumanPlayer.o \
	DumbPlayerV2.o GamblerPlayerV2.o
	
contest : $(AIContestMain) $(objects)
	g++ -o contest $(AIContestMain) $(objects)

clean:
	rm -f contest $(objects) 

