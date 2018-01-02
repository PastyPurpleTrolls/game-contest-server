require 'rails_helper'

describe PlayerRound do
	let! (:round) { FactoryBot.create(:challenge_round) }
  let (:player_round) { FactoryBot.create(:player_round, result: "Win") }
  subject { player_round } 

  # Tables
  it { should respond_to(:player) }
  it { should respond_to(:round) }

	# Attributes
  it { should respond_to(:result) }
	it { should respond_to(:score) }

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

		describe "not in the list [nil, 'Win', 'Loss', 'Tie', 'Crash', 'Time out', 'Unknown Round Result']" do
			before do
				player_round.result = 'garbage'
			end
    	it { should_not be_valid }
		end
	end

end
