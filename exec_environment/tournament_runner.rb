#!/usr/bin/env ruby

require 'active_record'
require 'active_support/time'
require 'sqlite3'
#require './config/boot'
#require './config/environment'
require 'optparse'

#Parsing command line arguements
$options = {}
OptionParser.new do |opts|
    opts.banner = "Usage: tournament.rb -t [tournament_id]"

    opts.on('-t' , '--tournament_id [TOURNAMENT_ID]' , 'Tournament ID to start') { |v| $options[:TOURNAMENT_ID] = v}
    opts.on('-e' , '--useless [USELESS]' , '') { |v| $options[:USELESS] = v}

end.parse!


class TournamentRunner
    def initialize(tournament_id)
        @tournament_id = tournament_id
        @tournament = Tournament.find(@tournament_id)
        @referee = @tournament.contest.referee
        @tournament_players = @tournament.players
        @number_of_players = @referee.players_per_game
        @max_match_time = 30.seconds
    end

    def run_tournament
        puts " Tournament runner started creating matches for tournament #"+@tournament_id.to_s+" ("+@tournament.tournament_type+")"
        if @tournament_players.count < 2
            puts " ERROR: Can't run tournament with fewer than two players"
            return
        end
        @tournament.status = "pending"
        @tournament.save!
        case @tournament.tournament_type
            when "round robin"
                round_robin(@tournament_players)
            when "single elimination"
                if @number_of_players > 2
                    puts " ERROR: Single elimination doesn't work with more than 2 players per game"
                else
                    single_elimination(@tournament_players)
                end
                return
            else
                puts " ERROR: Tournament type is not recognized"
                return
        end
        puts " Tournament runner finished creating matches for tournament #"+@tournament_id.to_s
    end

    #Runs a round robin tournament with each player playing every other player twice.
    #Currently only works with 2 player games
    def round_robin(players)
        players.each do |player1|
            players.each do |player2|
                if player1 != player2 then
                    create_match(player1, player2)
                end
            end
        end
        #need to check matches completed
        #@tournament.status = "completed"
        #@tournament.save!
    end
    
    #Runs a single elimination tournament (two players per match)
    def single_elimination(players)
        count = players.count
        puts "This many players: "+count.to_s
        if count == 2
            #return create_match(players[0],players[1])
        elsif count == 3
            #match = create_match(players[0],players[1])
        else
            half = count/2
            single_elimination(players[0..half-1])
            single_elimination(players[half..count])
        end        
    end
    
    #Creates a match and the associated player_matches
    def create_match(*match_participants)
        match = create_raw_match(match_participants)
        create_player_matches(match,match_participants)
    end 
    #Creates a match
    def create_raw_match(match_participants,status = "waiting")
        match = Match.create!(
            manager: @tournament, 
            status: status,
            earliest_start: Time.now, 
            completion: Date.new,
            match_type: MatchType.first,
        )
        puts " Tournament runner created match #"+match.id.to_s
        return match
    end 
    #Creates player matches
    def create_player_matches(match,match_participants)
        match_participants.each do |player|
            PlayerMatch.create!(
                match: match,
                player: player,
                result: "Pending",
                score: nil,
            )
            puts "   Added "+player.name
        end
    end    

end

#What gets run when the daemon starts up a new tournament
new_tournament = TournamentRunner.new($options[:TOURNAMENT_ID])
new_tournament.run_tournament
