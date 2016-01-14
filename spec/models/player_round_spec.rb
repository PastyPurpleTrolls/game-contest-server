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

=begin
<<<<<<< HEAD
	describe "validations" do
		it { should be_valid }
		specify { expect_required_attribute(:player) }
		specify { expect_required_attribute(:round) }
=======
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
>>>>>>> 2042a496d8a3de42ef23b5007c647a47bb77bb47
	end
=end
	describe "validations" do
		it { should be_valid }
		specify { expect_required_attribute(:player) }
		specify { expect_required_attribute(:round) }
	end

	describe "result is (case-sensitive)" do
		let (:list) { [nil, 'Win', 'Loss', 'Tie', 'Crash', 'Time out', 'Unknown Round Result'] }
		it "in the list [nil, 'Win', 'Loss', 'Tie', 'Crash', 'Time out', 'Unknown Round Result']" do
			list.each do |list_item|
				player_round.result = list_item
    		should be_valid 
			end
		end

		it "not in the list [nil, 'Win', 'Loss', 'Tie', 'Crash', 'Time out', 'Unknown Round Result']" do
			player_round.result = 'garbage'
    	should_not be_valid
		end
	end

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
