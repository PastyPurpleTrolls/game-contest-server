# Setting Up A Contest

### **Step 1**: Creating a Referee for a Game

> **Referees:** Sets of code used by the game server to
> create, manage and judge specific games.

Navigate to Referees page and tap the plus sign to get redirected to the new referees page.

- **Name**: A short name describing what game the referee judges
- **Rules URL**: this directs students to a website that should describe how to write an AI for this referee.
- **Referee File**: One file or a tar/zip of multiple files.  If using multiple files, a Makefile must be included and it must support "make run".  This is the code that is run in order to accomplish each game. E.g. **`test_referee.py`**
- **Player-Include Files**: One file or a tar/zip of multiple files. E.g. **`ref_helper.py`**
- **Replay Plugin**: A tar/zip containing a **`script.js`** and any assets necessary in order to visually represent each match.
- **Test Player**: File is typically written in Python and contains the player AI. E.g. **`test_player.py`**
- **Round Limit**: Defines how many rounds in a match the referee can handle.
- **Players Per Game**: How many players can participate in a match. Important, For standard tournaments use just **2** players per game.
- **Time Per Game**: How long in seconds the referee have to finish a match.
- **Referee Capable of handling rounds**: Can the referee start new rounds on its own, or does a new game have to be started for each round? Default to **no** unless you know you need it turned on.

### **Step 2**: Creating a Contest

> **Contests:** Track the results of one or more tournaments and store AI's to be run in those tournaments.

Navigate to Contests page and tap the plus sign to get redirected to the new contests page.

- **Referee**: Select the referee that will be used to your contest.
- **Deadline**: After this date, no new players are accepted.

### **Step 3**: Adding Players to your Contest

Once you have navigated to a specific contest, you will be presented with 3 different sections of information.
In the top center of page, you will see useful information pertaining to the contest.
Below that block of content, you will see two main categories of information; **Players** and **Tournaments** respectably. Important, you must first create players before you can run a tournament.

> **Players:** Players are AIs developed by students for the purpose of competing in various tournaments or challenges.

- **Selected Contest**: Choose the parent contest of your new player.
- **Player File**: File is typically written in Python and contains the player AI. E.g. **`test_player.py`**
- **Allow others to compete against this player**: Leave this checkmarked unless you don't want this player to be in tournaments or challenges.
- **Allow others to download this player**: This gives other users the ablity to download and examine the code of a Player's AI.

### **Step 4**: Creating a Tournament

> **Tournaments**: Tournaments orchestrate a series of games involving a set of player AI's, typically **Single Elimination** or **Round Robin**

- **Selected Contest**: Choose the parent contest of your new tournament.
- **Start**: Choose a start time for a tournament, if the time is set before the current time, the contest will automatically start.
- **Tournament Type**: Choose between a variety of tournament types like Single Elimination, Round Robin, and King of the Hill
- **Rounds Per Match**: The number of rounds to be played for a given match between players. Using multiple rounds helps  determine which AI is consistently preforming stronger.

### **Step 5**: Selecting Players

To add players to a tournament, select them from the left column listed as available players.
Once you select a player or group of players, select the right pointing arrow to add them to the
list of selected players for your tournament.

### **Step 6**: Viewing the Results

To view the results a tournament, select the tournament you are currently running from the contests page.
From there, you will be presented of different formatted visualization depending on game mode.
**Single Elimination** tournaments will have an real-time updating bracket. Note: Some information is 
displayed inaccurately while the tournament has not finished. Rest assured that once the tournament status is complete,
you will be able to a bracketed view of the final results.
**Round Robin** tournaments display a table of the results for all the given matchups.

Enjoy!