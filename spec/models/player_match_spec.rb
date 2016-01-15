require 'rails_helper'

describe PlayerMatch do
	let! (:match) { FactoryGirl.create(:challenge_match) }
  let (:player_match) { FactoryGirl.create(:player_match) }
  subject { player_match }

  # Tables
  it { should respond_to(:player) }
  it { should respond_to(:match) }

  # Attributes
  it { should respond_to(:result) }

  describe "validations" do
    it { should be_valid }
    specify { expect_required_attribute(:player) }
    specify { expect_required_attribute(:match) }
  end
=begin
<<<<<<< HEAD
=end

	describe "result is (case-sensitive)" do
		let (:list) { [nil, 'Win', 'Loss', 'Tie', 'Unknown Result'] }
		it "in the list [nil, 'Win', 'Loss', 'Tie', 'Unknown Result']" do
			list.each do |list_item|
				player_match.result = list_item
    		should be_valid 
			end
		end

		it "not in the list [nil, 'Win', 'Loss', 'Tie', 'Unknown Result']" do
			player_match.result = 'garbage'
    	should_not be_valid
		end
	end

	describe "has same player and match as a different player match" do	
		before do
			player_match.match_id = match.player_matches.first.match_id
			player_match.player_id = match.player_matches.first.player_id
		end

		it { should_not be_valid }
	end
end
