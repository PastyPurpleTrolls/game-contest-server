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

	describe "is created if there are already num_round rounds for that match" do
		before do
			match = FactoryBot.create(:tournament_match, num_rounds: 5)
			FactoryBot.create_list(:challenge_round, 5, match: match)
			match.rounds << round
		end

		it { should_not be_valid }
	end
end
