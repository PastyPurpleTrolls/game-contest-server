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
    def initialize(referee, match_id, number_of_players, max_match_time, players, rounds)  
        #Sets port for referee to talk to wrapper_server  
        @wrapper_server = TCPServer.new(0)
        
        @players = players
        @referee = referee
	@match_id= match_id
        @child_list = []
        @number_of_players = number_of_players
        @max_match_time = max_match_time
        @num_rounds = rounds
 
        @status = {}
        @rounds = []
        @match = {}

        @command_char = ":"
        @value_char = "|"
    end

    def run_match
        if @referee.rounds_capable
            self.run_round
        else
            @num_rounds.times do |i| 
                self.run_round
                if @status[:error] == true
                    return
                end
            end
            calculate_results
        end
    end
    
    #Used if referee is not rounds capable and can't calculate it's own match results
    def calculate_results
        players = {}
        @rounds.each do |round|
            round[:results].each do |player,result|
                if not players.has_key?(player)
                    players[player] = 0
                end
                if result[:result] == "Win"
                    players[player] += 1
                end
            end
        end
        winner = players.max_by{|k,v| v}
        players.each do |player, wins|
            @match[player] = {
                "result": (player == winner[0]) ? "Win" : "Loss",
                "score": wins
            }
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
        #Start referee process, giving it the port to talk to us on
        wrapper_server_port = @wrapper_server.addr[1]
	    if Dir.glob("#{File.dirname(@referee.file_location)}/[Mm]akefile").size > 0
		    command="cd #{Shellwords.escape File.dirname(@referee.file_location)}; make run port=#{wrapper_server_port} num_players=#{@number_of_players} num_rounds=#{@num_rounds} max_time=#{@max_match_time}"
	    else
		    command="#{Shellwords.escape @referee.file_location} -p #{wrapper_server_port} -n  #{@number_of_players} -r #{@num_rounds} -t #{@max_match_time}"
	    end

	loc = "#{Shellwords.escape @referee.file_location[0, @referee.file_location.length-@referee.name.length]}/match_#{@match_id}_round_#{@rounds.length + 1}" 
        @child_list.push(Process.spawn("#{command}", :out=>"#{loc}_log.txt", :err=>"#{loc}_err.txt"))
        
        #Wait for referee to tell wrapper_server what port to start players on
        begin
            Timeout::timeout(3) do
                #Wait for referee to connect
                @ref_client = @wrapper_server.accept
                @client_port = nil
                while @client_port.nil?
                    @client_port = self.find_command("port", @ref_client.gets)
                end
            end
        rescue Timeout::Error
            @status[:error] = true
            @status[:message] = "INCONCLUSIVE: Referee failed to provide a port!"  
            reap_children
            return
        end

        #Start players
        @players.each do |player|
            #Name must be given before port because it crashes for mysterious ("--name not found") reasons otherwise
			if Dir.glob("#{File.dirname(player.file_location)}/[Mm]akefile").size > 0
                command="cd #{Shellwords.escape File.dirname(player.file_location)}; make contest name=#{Shellwords.escape player.name} port=#{@client_port}"
			else
			    command="#{Shellwords.escape player.file_location} -n #{Shellwords.escape player.name} -p #{@client_port}"
			end

	    loc = "#{Shellwords.escape player.file_location[0, player.file_location.length-player.name.length]}/match_#{@match_id}_round_#{@rounds.length + 1}"
            @child_list.push(Process.spawn("#{command}", :out=>"#{loc}_log.txt", :err=>"#{loc}_err.txt"))
        end
        
        begin
            #Pad the max match time by 20% to allow for communication latency
            Timeout::timeout(@max_match_time*1.2) do
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
                        "info": input[:value][1]
                    })
                end
            when "roundresult"
                @rounds.last[:results][input[:value][0]] = {
                    "result": input[:value][1],
                    "score": input[:value][2]
                }
            when "matchresult"
                @match[input[:value][0]] = {
                    "result": input[:value][1],
                    "score": input[:value][2]
                }
            when "move"
                # Add move to current round
                @rounds.last[:moves].push({
                    "description": input[:value][0],
                    "data": input[:value][1]
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
end

