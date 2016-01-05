#Game Contest Server

Interactive, web based manager for automated turn-based game contests.

##Requirements

* Ruby on Rails
* [RubyGems](https://rubygems.org)

##User Documentation

The user documentation can be found in [/documentation](/documentation)

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

Temporary fix: `export DISABLE_SPRING=1`

Start the daemon (checks for new tournaments and matches)

```
$ /usr/local/rvm/gems/ruby-2.2.0/bin/clockworkd stop ./clock.rb --log
$ /usr/local/rvm/gems/ruby-2.2.0/bin/clockworkd -d . start ./clock.rb --log
```

View the logs from the daemon: `tail -f /home/mkammes/gcs/tmp/clockworkd.clock.output`

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
