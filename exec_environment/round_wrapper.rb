#! /usr/bin/env ruby

#round_wrapper.rb

#Imports
require 'socket'
require 'open-uri'
require 'timeout'
require 'json'
require 'shellwords'

class RoundWrapper
  attr_accessor :status, :rounds, :match

  #Constructor, sets socket for communication to referee and starts referee and players
  def initialize(referee, match_id, number_of_players, max_match_time, players, rounds, duplicate_players)
    #Sets path for referee to talk to wrapper_server
    @aires_path = "/tmp/aires-manager"
    File.delete @aires_path if File.exists? @aires_path
    @wrapper_server = UNIXServer.new(@aires_path)

    @players = players
    @referee = referee
    @match_id = match_id
    @child_list = []
    @number_of_players = number_of_players
    @max_match_time = max_match_time
    @num_rounds = rounds
    @duplicate_players = duplicate_players

    @status = {}
    @rounds = []
    @match = {}
    @match[:logs] = {}

    @command_char = ":"
    @value_char = "|"
  end

  def run_match
    if @referee.rounds_capable
      self.run_round
    else
      @num_rounds.times do
        if @max_match_time >= 1
          begin_time = Time.now
          self.run_round
          end_time = Time.now
          @max_match_time -= (end_time - begin_time)
          if @status[:error]
            return
          end
        end
      end
      calculate_results
    end
    compress_logs
  end

  #Used if referee is not rounds capable and can't calculate it's own match results
  def calculate_results
    players = {}
    @rounds.each do |round|
      round[:results].each do |player, result|
        if not players.has_key?(player)
          players[player] = 0
        end
        if result[:result] == "Win"
          players[player] += 1
        end
      end
    end
    winner = players.max_by { |k, v| v }
    players.each do |player, wins|
      @match[player] = {
        "result": (player == winner[0]) ? "Win" : "Loss",
        "score": wins,
      }
      if @duplicate_players
        @match[player][:result] = "Tie"
      end
    end
  end

  # Parse commands from the referee client
  # command (str), name of command that I'm looking for
  # str (str), string from client that looks like command:value
  def find_command(command, str)
    #split on first instance of command char
    parsed = str.split(@command_char, 2)
    if parsed.first == command
      return self.parse_value(parsed.last)
    else
      return nil
    end
  end

  def parse_value(value)
    value = value.gsub("\n", "")
    values = value.split(@value_char)
    return (values.length > 1) ? values : value
  end

  def parse_command(str)
    cmd = {}
    parsed = str.split(@command_char, 2)
    cmd[:command] = parsed.first
    cmd[:value] = self.parse_value(parsed.last)
    return cmd
  end

  def run_round
    #Wait for referee in separate thread to fix race condition
    t = Thread.start(@wrapper_server) { |server|
      client = server.accept
      begin
        Timeout::timeout(5) do
          #Wait for referee to connect
          @client_path = nil
          while @client_path.nil?
            line = client.gets
            @client_path = self.find_command("path", line)
            @ref_client = client
          end
        end
      rescue Timeout::Error
        @status[:error] = true
        @status[:message] = "INCONCLUSIVE: Referee failed to provide a port!"
        reap_children
        return
      end
    }
    sleep 0.1
    #Start referee process, giving it the port to talk to us on
    if Dir.glob("#{File.dirname(@referee.file_location)}/[Mm]akefile").size > 0
      file_location = Shellwords.escape File.dirname(@referee.file_location)
      command = "cd #{file_location}; make run path=#{@aires_path} num_players=#{@number_of_players} num_rounds=#{@num_rounds} max_time=#{@max_match_time.to_i}"
    else
      file_location = Shellwords.escape @referee.file_location
      command = "#{file_location} -p #{@aires_path} -n  #{@number_of_players} -r #{@num_rounds} -t #{@max_match_time}"
    end

    loc = get_log_location(@referee)
    @child_list.push(Process.spawn("#{command}", :out => "#{loc}_log.txt", :err => "#{loc}_err.txt"))
    @match[:ref_logs] = loc

    #Wait for referee to tell wrapper_server what port to start players on
    t.join
    return if @status[:error]

    if @players.uniq.length == 1
      `cd #{Shellwords.escape File.dirname(@players.first.file_location)}; make contest_compile`
    end

    #Start players
    @players.each do |player|
      player_name = Shellwords.escape player.name

      #Name must be given before port because it crashes for mysterious ("--name not found") reasons otherwise
      if Dir.glob("#{File.dirname(player.file_location)}/[Mm]akefile").size > 0
        file_location = Shellwords.escape File.dirname(player.file_location)
        command = "cd #{file_location}; make contest name=#{player_name} path=#{@client_path}"
      else
        file_location = Shellwords.escape player.file_location
        command = "#{file_location} -n #{player_name} -p #{@client_path}"
      end

      loc = get_log_location(player)
      @child_list.push(Process.spawn("#{command}", :out => "#{loc}_log.txt", :err => "#{loc}_err.txt"))
      @match[:logs][player.name] = loc
    end

    begin
      #Pad the max match time by 20% to allow for communication latency
      Timeout::timeout(@max_match_time * 1.2) do
        self.handle_tcp_input
      end
    rescue Timeout::Error
      @status[:error] = true
      @status[:message] = "INCONCLUSIVE: Game exceeded allowed time!"
      reap_children
      return
    end

    reap_children
  end

  def get_log_directory(entity)
    file_location_parts = entity.file_location.split('/')
    file_location_parts.pop
    dir_location = file_location_parts.join('/')
    "#{Shellwords.escape dir_location}/logs/"
  end

  def get_log_location(entity)
    log_directory = get_log_directory(entity)
    file_name = "#{entity.name}_match_#{@match_id}_round_#{@rounds.length + 1}"
    log_directory + file_name
  end

  #Receive input from referee and perform actions
  def handle_tcp_input
    while line = @ref_client.gets
      input = self.parse_command(line)
      #Match on command and perform actions
      case input[:command]
      when "round"
        #Add a new round to the rounds array when a round starts
        if input[:value][0] == "start"
          @rounds.push({
            "results": {},
            "moves": [],
            "info": input[:value][1],
          })
        end
      when "roundresult"
        @rounds.last[:results][input[:value][0]] = {
          "result": input[:value][1],
          "score": input[:value][2],
        }
      when "matchresult"
        @match[input[:value][0]] = {
          "result": input[:value][1],
          "score": input[:value][2],
        }
      when "move"
        # Add move to current round
        @rounds.last[:moves].push({
          "description": input[:value][0],
          "data": input[:value][1],
        })
      when "gamestate"
        #Ignore game state
        lastmove = @rounds.last[:moves].last
        #Ignore game state if there aren't any moves
        if lastmove.nil?
          break
        end
        lastmove[:gamestate] = input[:value]
      end
    end
    @status[:error] = false
  end

  def reap_children
    @child_list.each do |pid|
      Process.kill('SIGKILL', pid)
      Process.waitpid(pid)
    end
    @child_list = []
  end

  def compress_logs
    locs = []
    locs << get_log_directory(@referee)
    @match[:ref_logs] = locs.last + "match_#{@match_id}_logs"
    @players.each do |player|
      locs << get_log_directory(player)
      @match[:logs][player.name] = locs.last + "match_#{@match_id}_logs"
    end

    locs.each do |loc|
      command = "tar czf match_#{@match_id}_logs_out.tgz *log.txt; tar czf match_#{@match_id}_logs_err.tgz *err.txt; rm *.txt"
      Process.spawn(command, :chdir => loc)
    end
  end
end
