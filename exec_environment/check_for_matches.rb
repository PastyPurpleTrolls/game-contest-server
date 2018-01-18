#! /usr/bin/env ruby
#Alex Sjoberg
#match_checker.rb
#Jan 2014
# Queries db for matches whose start date has passed and is "waiting" to be started
#
# TODO Queueing all available matches instead of just spawning one each time. Maybe using Delayed Job?

match = Match.where("earliest_start < ? and status = ?", Time.now.utc, "waiting").last
if not match.nil?
  match.status = "started"
  begin
    match.save!
    puts "  Daemon spawning match #" + match.id.to_s
    pid = Process.spawn("rails runner exec_environment/match_runner.rb -m #{match.id}")
    Process.wait pid
  rescue
    puts "Database was locked. Will retry next time."
  end
end
