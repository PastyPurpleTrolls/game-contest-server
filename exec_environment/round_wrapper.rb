#! /usr/bin/env ruby

#round_wrapper.rb
#Alex Sjoberg, additional work by Bradley Rosenfeld


#TODO allow ref to specifiy a unique port for each player
# NOTE for testing arbitrary players and ref with the matchwrapper without having to worry about tournaments/daemons/etc, see wrapper_test.rb

#Imports
require 'socket'
require 'open-uri'
require 'timeout'

class RoundWrapper
    
    attr_accessor :results

    #Constructor, sets socket for communication to referee and starts referee and players
    def initialize(referee,number_of_players,max_match_time,players,rounds)  
        #Sets port for referee to talk to wrapper_server  
        @wrapper_server = TCPServer.new(0)
        
        @players = players
        @referee = referee
        @child_list = []
        @number_of_players = number_of_players
        @max_match_time = max_match_time
        
        @results = []
	    @num_rounds = rounds

        @command_char = ":"
        @value_char = "|"
    end

    def run_match
        puts "Starting match"
        if @referee.rounds_capable
            puts "Rounds capable"
            self.run_round
        else
            @num_rounds.times do |i| 
                self.run_round(i)
            end
        end
    end

    # Parse commands from the referee client
    # command (str), name of command that I'm looking for
    # str (str), string from client that looks like command:value
    def parse_command(command, str)
        #split on first instance of command char
        parsed = str.split(@command_char, 2)
        if parsed.first == command
            # Strip new line characters and split value if necessary
            value = parsed.last.gsub("\n", "")
            values = value.split(@value_char)
            return (values.length > 1) ? values : values.first
        else
            return nil
        end
    end

    def run_round(round = -1)
        #Start referee process, giving it the port to talk to us on
        wrapper_server_port = @wrapper_server.addr[1]
	    if File.exists?("#{File.dirname(@referee.file_location)}/Makefile")
		    command="make run port=#{wrapper_server_port} num_players=#{@number_of_players} num_rounds=#{@num_rounds}"
	    else
		    command="#{@referee.file_location} -p #{wrapper_server_port} -n  #{@number_of_players} -r #{@num_rounds}"
	    end
        @child_list.push(Process.spawn("cd #{File.dirname(@referee.file_location)}; #{command}"))

        #Wait for referee to tell wrapper_server what port to start players on
        begin
            Timeout::timeout(3) do
                #Wait for referee to connect
                @ref_client = @wrapper_server.accept
                @client_port = nil
                while @client_port.nil?
                    @client_port = parse_command("port", @ref_client.gets)
                end
                puts @client_port
            end
        rescue Timeout::Error
            @results = "INCONCLUSIVE: Referee failed to provide a port!"  
            reap_children
            return
        end

        #Start players
        @players.each do |player|
            #Name must be given before port because it crashes for mysterious ("--name not found") reasons otherwise
			name = player.name.gsub("'"){'\'"\'"\''}
			if File.exist?("#{File.dirname(player.file_location)}/Makefile")
                command="make contest name='#{name}' port=#{@client_port}"
			else
			    command="#{player.file_location} -n '#{name}' -p #{@client_port}"
			end
            @child_list.push(Process.spawn("cd #{File.dirname(player.file_location)}; #{command}"))
        end
        
        begin
            Timeout::timeout(@max_match_time) do
                self.wait_for_result(round)
            end
        rescue Timeout::Error
            @results = "INCONCLUSIVE: Game exceeded allowed time!"
            reap_children
            return
        end

        reap_children
    end

    def wait_for_result(round)
        puts "Waiting for results"
        while line = @ref_client.gets
            puts line
        end
    end
    
    def reap_children
        @child_list.each do |pid|
            Process.kill('SIGKILL', pid)
	        Process.wait pid
        end
    end 
end

