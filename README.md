#Game Contest Server

Interactive, web based manager for automated turn-based game contests.

##Requirements

* Ruby on Rails 4.2.0
* [RubyGems](https://rubygems.org)

##Setup

Clone the repo: `git clone https://github.com/PastyPurpleTrolls/test.git`

Install prerequisites: `gem install`

Temporary fix: `export DISABLE_SPRING=1`

##Running

Start the daemon (checks for new tournaments and matches)

```
$ /usr/local/rvm/gems/ruby-2.2.0/bin/clockworkd stop ./clock.rb --log
$ /usr/local/rvm/gems/ruby-2.2.0/bin/clockworkd -d . start ./clock.rb --log
```

View the logs from the daemon: `tail -f /home/mkammes/gcs/tmp/clockworkd.clock.output`

