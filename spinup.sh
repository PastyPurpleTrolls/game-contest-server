#!/bin/bash

BASE=0.0.0.0
PORT=8000

while getopts b:p: option
do
	case "${option}"
	in
		b) BASE=${OPTARG};;
		p) PORT=${OPTARG};;
	esac
done

/usr/local/rvm/gems/ruby-2.2.0/bin/clockworkd -d . start ./clock.rb --log
rails s -b $BASE -p $PORT
