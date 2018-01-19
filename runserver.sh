#!/bin/bash
function trap_ctrlc () {
	killall clockworkd.clock
	killall ruby
	exit 2
}
trap "trap_ctrlc" 2
/home/hannes/.rvm/gems/ruby-2.4.3/bin/clockworkd -d . start ./clock.rb --log &
/home/hannes/.rvm/gems/ruby-2.4.3/bin/rails s -b 0.0.0.0 -p 8010
