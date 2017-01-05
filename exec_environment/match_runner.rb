#!/usr/bin/env ruby


require 'active_record'
require 'active_support/time'
require 'sqlite3'
require './exec_environment/round_wrapper.rb'
require 'optparse'
require 'json'
require 'fileutils'

#This may be an alternative to running the file using 'rails runner'. These provide access to the rails environment
#require './config/boot'
#require './config/environment'

#Parsing command line arguements
$options = {}
OptionParser.new do |opts|
    opts.banner = "Usage: match_runner.rb -m [match_id]"

    opts.on('-m' , '--match_id [MATCH_ID]' , 'Match ID to start') { |v| $options[:MATCH_ID] = v}

    # This is to allow specifying a rails environment when using 'rails runner'
    # A command of the form "rails runner -e test match_runner.rb -m 5" will make optionparser complain that it doesn't know what the -e flag is unless we accept it here.
    opts.on('-e' , '--useless [USELESS]' , '') { |v| $options[:USELESS] = v} 

end.parse!
    
class MatchRunner
    
    #Get necessary info from the database
    def initialize(match_id)
       @match_id = match_id 
       @match = Match.find(match_id)
       @match_participants = @match.players

       #Grab referee based upon polymorphic association
       if @match.manager_type.to_s == "Contest"
         @referee = @match.manager.referee
       else
	    @referee = @match.manager.contest.referee
       end

       @number_of_players = @referee.players_per_game
       @max_match_time = @referee.time_per_game
       @tournament = @match.manager
       @num_rounds = @match.num_rounds

       @logs_directory = Rails.root.join("public", "match-logs")
    end 
    
    #Uses a MatchWrapper to run a match between the given players and send the results to the database
    def run_match
        if @number_of_players != @match_participants.count()
            puts "   Match runner skipping match #"+@match_id.to_s+
                 " ("+@match_participants.count().to_s+"/"+@number_of_players.to_s+" in player_matches)"
            return
        end
        #Call round wrapper which runs the executables and generates game hashes
        round_wrapper = RoundWrapper.new(@referee,@match_id,@number_of_players,@max_match_time,@match_participants,@num_rounds)
        puts "   Match runner running match #"+@match_id.to_s
        round_wrapper.run_match
        self.send_results_to_db(round_wrapper)
    end

    #Creates PlayerMatch objects for each player using the results dictionary we got back from the MatchWrapper
    def send_results_to_db(round_runner)
        puts round_runner.status
        if round_runner.status[:error]
            report_error
            return
        else
            if not self.save_rounds(round_runner.rounds)
                report_error
                return false
            end
            #Print and save results, schedule follow-up matches
            child_matches = MatchPath.where(parent_match_id: @match_id)
            puts "   Match runner writing results match #"+@match_id.to_s
            #Loop through participants and find their results
            @match_participants.each do |player|
                player_match = PlayerMatch.where(match_id: @match_id, player_id: player.id).first
                player_match.result = round_runner.match[player.name][:result]
		##player_match.log = :banana
		player_match.log_out = round_runner.match[:logs][player.name]+"_log.txt"
		player_match.log_err = round_runner.match[:logs][player.name]+"_err.txt"
                player_match.save!
                print_results(player.name, player_match.result, round_runner.match[player.name][:score])
                self.schedule_matches(player, player_match, child_matches)
            end
            puts "   Match runner finished match #"+@match_id.to_s
            self.complete_match
        end
        #Check to see if the tournament can be completed
        self.complete_tournament
    end

    def report_error
        @match_participants.each do |player|
            player_match = PlayerMatch.where(match_id: @match_id, player_id: player.id).first
            player_match.result = "Error"
            player_match.save!
            print_results(player.name, "Error", nil)
        end
        puts "    Match runner could not finish match #" + @match.id.to_s
    end

    def save_rounds(rounds)
        if rounds.length != @num_rounds
            return false
        end
        #Loop through all the rounds and create a new record in the DB
        rounds.each do |round|
            round_obj = Round.create!(
                match: Match.find(@match_id)
            )
            #Loop through participants and add their results to the DB
            @match_participants.each do |player|
                PlayerRound.create!(
                    round: round_obj,
                    player: player,
                    result: round[:results][player.name][:result],
                    score: round[:results][player.name][:score]
                )
            end
            #Save round data to json file
            self.save_round_json(round_obj.slug, round)
        end
        return true
    end

    #Generate log files for playing back rounds
    def save_round_json(slug, round)
        #Check if the match directory exists already
        match_directory = File.join(@logs_directory, @match.slug)
        unless File.directory?(match_directory)
            FileUtils.mkdir_p(match_directory)
        end
        filename = File.join(match_directory, slug + ".json")
        #Write round hash to json file
        File.open(filename, "w") do |file|
            file.write(round.to_json)
        end
    end

    def schedule_matches(player, player_match, child_matches)
        child_matches.each do |match|
            if match.result == player_match.result
                create_player_match(Match.find(match.child_match_id), player)
            end
        end
    end

    def complete_match
        @match.status = "completed"
        @match.completion = Time.now
        @match.save!
    end


    def complete_tournament
        if @match.manager_type.to_s != "Tournament"
            return false
        end
        tournament = Tournament.find(@match.manager_id)
        tournament.matches.each do |childmatch|
            if childmatch.status == "started"
                return false
            end
        end
        tournament.status = "completed"
        tournament.save!
        return true
    end
    
    #Prints a name, result, and score
    def print_results(name,result,score,separator="\n")
        print "    "+name.ljust(24).slice(0,23)+
         " Result: "+result.ljust(10).slice(0,9)+
         " Score: "+score.to_s.ljust(10).slice(0,9)+
         separator
    end
    
    #Creates player_match and updates the match status to waiting if necessary 
    def create_player_match(match,player)
        #Create player_match
        PlayerMatch.create!(
            match: match,
            player: player,
            result: "Pending",
        )
        print "=> Match #"+match.id.to_s
        #Change status of match if necessary
        if match.players.count == @number_of_players
            match.status = "waiting"
        end
        match.save!
    end
end 

match_runner = MatchRunner.new($options[:MATCH_ID])
match_runner.run_match
