require 'rails_helper'

describe PlayerRound do
  let (:player_round) { FactoryGirl.create(:player_round) }
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
		before do
			p1 = FactoryGirl.create(:player)
			r1 = FactoryGirl.create(:challenge_round)
			pr2 = FactoryGirl.create(:player_round, round_id: r1.id, player_id: p1.id)
			
			player_round.round_id = r1.id
			player_round.player_id = p1.id
		end

		it { should_not be_valid }
		

	end

end
