require 'rails_helper'

describe Round do
  let (:round) { FactoryBot.create(:challenge_round) }
  subject { round }

  # Tables
  it { should respond_to(:match) }
	it { should respond_to(:player_rounds) }
	it { should respond_to(:players) }

	describe "validations" do 
    it { should be_valid }
		specify { expect_required_attribute(:match) }
	end

	describe "does not have the same players as the match" do
		before do
			round.match.players.destroy(round.match.players.first)
			player1 = FactoryBot.create(:player)
			player_match1 = FactoryBot.create(:player_match, player: player1, match: round.match)
			player1.save	
			player_match1.save
			round.match.reload
		end
    it { should_not be_valid }
	end
=begin
	describe "does not have the same players as the match" do
		before do
			match = FactoryBot.create(:tournament_match)
      match.players.clear
			player1 = FactoryBot.create(:player)
			player2 = FactoryBot.create(:player)
			player3 = FactoryBot.create(:player)
			player_match1 = FactoryBot.create(:player_match, match: match, player: player1)
			player_match2 = FactoryBot.create(:player_match, match: match, player: player2)
			player_round1 = FactoryBot.create(:player_round, match: match, player: player1)
			player_round3 = FactoryBot.create(:player_round, match: match, player: player3)
end
			# set up the match to have players p1 and p2
=begin			
			match = FactoryBot.create(:tournament_match)
      ref = FactoryBot.create(:referee, players_per_game: 2)
      contest = FactoryBot.create(:contest, referee: ref)
      tournament = FactoryBot.create(:tournament, contest: contest)
      p1 = FactoryBot.create(:player, contest: contest)
      p1.tournaments << tournament
      p2 = FactoryBot.create(:player, contest: contest)
      p2.tournaments << tournament
      match.manager = tournament
      match.players.clear
      match.players << p1 << p2

			# set up the round to have players p1 and p3
      p3 = FactoryBot.create(:player, contest: contest)
      p3.tournaments << tournament
			round.match = match
			round.players.clear
			round.players << p1 << p3
		end
		it { should_not be_valid }
	end
=end

	describe "is created if there are already num_round rounds for that match" do

		before do
			match = FactoryBot.create(:tournament_match, num_rounds: 5)
			FactoryBot.create_list(:challenge_round, 5, match: match)
			match.rounds << round
		end

		it { should_not be_valid }
	end

end
