#Game Contest Server

Interactive, web based manager for automated turn-based game contests.

##Requirements

* Ruby on Rails
* [RubyGems](https://rubygems.org)

##User Documentation

The user documentation can be found in [documentation](/documentation)

##Setup

Clone the repo: `git clone https://github.com/PastyPurpleTrolls/test.git`

Install prerequisites:
```
$ bundle install
$ rake db:schema:load
```

##Running (dev)

Start the server

```
$ rails s -b 0.0.0.0 -p 8000
```

Start the daemon (checks for new tournaments and matches)

```
$ /usr/local/rvm/gems/ruby-2.2.0/bin/clockworkd -d . start ./clock.rb --log
```

Stop the dameon

```
$ /usr/local/rvm/gems/ruby-2.2.0/bin/clockworkd stop ./clock.rb --log
```

View the logs from the daemon: `tail -f [game_contest_server_root]/tmp/clockworkd.clock.output`

###Manage Users

Create user in web interface (host:port)

```
$ rails c
> User.all
> u = User.first
> u.contest_creator = true
> u.admin = true
> u.save
```

###Tests

Run tests: `rspec`


##Development

Frontend user interface files are located in `app/assets`. Views are in `app/views`

###Executable Environment

User players and referees inherently need to be executed. To faciliate this, several helper files are located in `exec_environment/`.

A daemon (powered by clockword) executes `check_for_matches.rb` and `check_for_tournaments.rb` every set period. These files check for new matches or tournaments that haven't been executed. 

When a new tournament is found, the tournament type is used to to generate a bracket that matches up player appropriately. Matches are created based upon the calculated bracket. These matches are treated like a queue and handled one at a time by `check_for_matches.rb`. 

The concept of rounds during a match (repeated games between the same opponents) is handled differently depending upon the type of referee uploaded. Referees that explicitly handle rounds are sent the number of rounds they should run. Some referees might not handle rounds, so the system will create N matches to simulate multiple rounds. 

Each match is executed by `match_wrapper.rb`. The referee is started and told to listen on a specific port for a set number of players. Then the players are started and told the port where they can find the referee. Referees are in charge of handling communication with the players, but they must check in with `match_wrapper.rb` or the match runner will assume the game has failed and will stop the match. 

