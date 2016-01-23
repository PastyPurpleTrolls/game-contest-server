#Game Contest Server

Interactive, web based manager for automated turn-based game contests.

##Requirements

* Ruby on Rails
* [RubyGems](https://rubygems.org)

##User Documentation

The user documentation can be found in [documentation](/documentation)

##Setup

Clone the repo: `git clone https://github.com/PastyPurpleTrolls/game-contest-server.git`

Install prerequisites:
```bash
$ bundle install
$ rake db:schema:load
```

##Running (dev)

Start the server

```bash
$ rails s -b 0.0.0.0 -p 8000
```

Start the daemon (checks for new tournaments and matches)

```bash
$ /usr/local/rvm/gems/ruby-2.2.0/bin/clockworkd -d . start ./clock.rb --log
```

Stop the dameon

```bash
$ /usr/local/rvm/gems/ruby-2.2.0/bin/clockworkd stop ./clock.rb --log
```

View the logs from the daemon (from the root of the game server directory: 

```bash 
tail -f tmp/clockworkd.clock.output
```

###Manage Users

Create user in web interface (host:port)

```bash
$ rails c
> User.all
> u = User.first
> u.contest_creator = true
> u.admin = true
> u.save
```

###Tests

Run tests: `rspec`


###Migrations

See the folder db/migrate. If there are new migrations, then perform the following at the command line:
```bash
$ rake db:migrate
$ rake db:migrate RAILS_ENV=test
```

However, do not perform these command line arguments while the clockwork daemon is running (see the top of the section "Running (dev)"). If you do, this locks the database (because the daemon is not up to date with the database). One way to unlock the database is to perform the following at the command line:
```bash
$ rake db:reset
```

However, make sure that you understand the ramifications of this command- the database's existing data is deleted. See [seeds.rb](/db/seeds/development.rb) for what the default values of the db after the db is reset.

##Development

Frontend user interface files are located in `app/assets`. Views are in `app/views`

###Test-Driven Development
Both the 2015 and the 2016 Jterm teams recommend strongly that you stick with test-driven development. The long-term benefits outweigh the short-term struggles. 
####Pending tests
The 2016 Jterm team has left some (not many) tests (in the branch 'uiBranch') as pending and incompletely filled out. These pending tests are a suggestion to the next team that these tests should be fully written and made official tests.

###Tracking Issues with GitHub
The 2016 Jterm team recommends using GitHub's [Issues](https://github.com/PastyPurpleTrolls/game-contest-server/issues) tracker. There, we have listed issues that are not described in pending tests.
Here are necessary definitions of some of the labels on Github Issues:
* enhancement- it would be nice to close the issue, but it is not strictly required that it become closed
* futurework- a shortcoming of the application that must inevitably be resolved for basic functionality of the site
* bug- a technical mistake that must inevitably be resolved for basic functionality of the site
* uiBranch or master- the issue would be best resolved in one of these two branches. Only use one of these labels with a given issue.
	* when uiBranch and master finally merge (which should be as soon as possible), if the issue has been addressed in one of the branches, then the merge will hopefully resolve it in both branches (if the issue was in both branches; it is possible that the issue was only in one branch) 

##Referees

Referees are executable files that are uploaded by instructors to enforce the rules in a competition match. The Game Contest Server does not have any concept of what a "game" is, rather the referee is in charge of defining what that means (chess, checkers, risk, etc...) 

For security and practical purposes, players and referees are started as seperate processes on the system. Communication is handled via a TCP socket that the referee creates. The protocol that referees and players use to communicate is entirely dependant upon the game, but the protocol that referees use to report results back to the game manager is carefully defined in the [referee documentation](documentation/creator/referee.md). Please refer to this documentation for any additional information on how to build a referee.

Example referees are located in [/examples](examples). Python referees should take advantage of [ref_helper.py](examples/ref_helper.py) which implements several useful classes and methods for managing communication with the game manager.

###Replay Plugin

Every referee should be uploaded with a replay plugin. This piece of code handles calculating and rendering replays of games in the web browser. The Game Contest Server automatically creates log files from data sent via the protocol during each round. These log files are parsed and made available to replay plugins. 

Please refer to the [replay plugin documentation](documentation/creator/referee.md#replay-plugin) for more information.

##Design

The Game Contest Server employs two different services: a web server and a background daemon that runs tournaments and matches. The web server allows users to upload players and referees, manage tournaments, and view replays of rounds that have been played on the system. The background daemon continuously checks for new tournaments and matches, runs matches, and adds the results to the database.

###Executable Environment

User players and referees inherently need to be executed. To faciliate this, several helper files are located in `exec_environment/`.

A daemon (powered by clockword) executes `check_for_matches.rb` and `check_for_tournaments.rb` every set period. These files check for new matches or tournaments that haven't been executed. 

When a new tournament is found, the tournament type is used to to generate a bracket that matches up player appropriately. Matches are created based upon the calculated bracket. These matches are treated like a queue and handled one at a time by `check_for_matches.rb`. 

The concept of rounds during a match (repeated games between the same opponents) is handled differently depending upon the type of referee uploaded. Referees that explicitly handle rounds are sent the number of rounds they should run. Some referees might not handle rounds, so the system will create *N* matches to simulate multiple rounds. 

Matches are executed and saved by `match_runner.rb`. This executable is in charge of starting the rounds, getting the results back, saving wins/losses, and updating the status of the tournament on match completion. 

Each round is executed by `round_wrapper.rb`. The referee is started and told to listen on a specific port for a set number of players. Then the players are started and told the port where they can find the referee. Referees are in charge of handling communication with the players, but they must check in with `round_wrapper.rb` or the match runner will assume the game has failed and will stop the match. 

###ERD
![Image of ERD document](/documentation/GameContestServerERD.png)

Many to many relationships are represented with a colored connection. This represents an additional associative entity (such as player_rounds) that connects the two entities. 
