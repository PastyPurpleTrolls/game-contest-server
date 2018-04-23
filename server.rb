#! /usr/bin/env ruby

def start_server(is_production)
  if is_production
    `RAILS_ENV=production rails s -b 0.0.0.0 -p 80 -d`
    `RAILS_ENV=production clockworkd -d . start ./clock.rb --log`
  else
    `rails s -d`
    `clockworkd -d . start ./clock.rb --log`
  end
end

def stop_server(is_production)
  begin
    pid_file = 'tmp/pids/server.pid'
    pid = File.read(pid_file).to_i
    Process.kill 15, pid
    File.delete pid_file
    if is_production
      `RAILS_ENV=production clockworkd -d . stop ./clock.rb --log`
    else
      `clockworkd -d . stop ./clock.rb --log`
    end
  rescue
    nil
  end
end

def main
  is_production = ARGV.include?('-p') or ARGV.include?('--production')
  if ARGV.include? 'start'
    start_server(is_production)
  elsif ARGV.include? 'stop'
    stop_server(is_production)
  elsif ARGV.include? 'restart'
    stop_server(is_production)
    start_server(is_production)
  else
    puts 'Error: must specify start/stop/restart'
  end
end

main