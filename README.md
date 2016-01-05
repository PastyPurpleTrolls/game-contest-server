#Game Contest Server

Interactive, web based manager for automated turn-based game contests.

##Requirements

* Ruby on Rails 4.2.0
* [RubyGems](https://rubygems.org)

##Setup

Clone the repo: `git clone https://github.com/PastyPurpleTrolls/test.git`

Install prerequisites: `gem install`

First thing that needs to be run until buf fix: `export DISABLE_SPRING=1`

Before a tournament is run you must run the following commands:

`/usr/local/rvm/gems/ruby-2.2.0/bin/clockworkd stop ./clock.rb --log

/usr/local/rvm/gems/ruby-2.2.0/bin/clockworkd -d . start ./clock.rb --log`

For development purposes to see the tournament run with individual matches you can type in: `tail -f /home/mkammes/gcs/tmp/clockworkd.clock.output`

