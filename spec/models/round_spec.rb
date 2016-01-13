require 'rails_helper'

describe Round do
  let (:round) { FactoryGirl.create(:challenge_round) }
  subject { round }

  # Tables
  it { should respond_to(:match) }
	it { should respond_to(:player_rounds) }
	it { should respond_to(:players) }

	describe "validations" do 
    it { should be_valid }
		specify { expect_required_attribute(:match) }
	end

=begin
	describe "does not have the same players as the match" do
		before do
			match = FactoryGirl.create(:tournament_match)
      match.players.clear
			player1 = FactoryGirl.create(:player)
			player2 = FactoryGirl.create(:player)
			player3 = FactoryGirl.create(:player)
			player_match1 = FactoryGirl.create(:player_match, match: match, player: player1)
			player_match2 = FactoryGirl.create(:player_match, match: match, player: player2)
			player_round1 = FactoryGirl.create(:player_round, match: match, player: player1)
			player_round3 = FactoryGirl.create(:player_round, match: match, player: player3)
end
			# set up the match to have players p1 and p2
			match = FactoryGirl.create(:tournament_match)
      ref = FactoryGirl.create(:referee, players_per_game: 2)
      contest = FactoryGirl.create(:contest, referee: ref)
      tournament = FactoryGirl.create(:tournament, contest: contest)
      p1 = FactoryGirl.create(:player, contest: contest)
      p1.tournaments << tournament
      p2 = FactoryGirl.create(:player, contest: contest)
      p2.tournaments << tournament
      match.manager = tournament
      match.players.clear
      match.players << p1 << p2

			# set up the round to have players p1 and p3
      p3 = FactoryGirl.create(:player, contest: contest)
      p3.tournaments << tournament
			round.match = match
			round.players.clear
			round.players << p1 << p3
		end

		it { should_not be_valid }
	end
=end
	
end
