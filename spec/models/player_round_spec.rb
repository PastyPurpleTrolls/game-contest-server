require 'rails_helper'

describe PlayerRound do
  let (:player_round) { FactoryGirl.create(:player_round, result: "Win") }
  subject { player_round }

  # Tables
  it { should respond_to(:player) }
  it { should respond_to(:round) }

	# Attributes
  it { should respond_to(:result) }
  it { should respond_to(:score) }

	# Validations
	it { should be_valid }
	
	describe "has same player and round as a different player round" do
		let (:player_round2) { FactoryGirl.create(:player_round, player_id: 1, round_id: 1) }
		before do
			player_round.round_id = 1
			player_round.player_id = 1
		end
		subject { player_round2 }

		it { should_not be_valid }
	end

end
