require 'rails_helper'

#Check that creating a MatchWrapper works
describe "RoundWrapper" do
  before :each do
    @user = FactoryGirl.create(:user)
    @contest = FactoryGirl.create(:contest)
    @player1 = FactoryGirl.create(:player, user: @user, contest: @contest, name: 'dumb_player', file_location: Rails.root.join('examples', 'test_player.py').to_s )
    @player2 = FactoryGirl.create(:player, user: @user, contest: @contest, name: 'stupid_player', file_location: Rails.root.join('examples', 'test_player.py').to_s )
    @referee = FactoryGirl.create(:referee, name: "referee", file_location: Rails.root.join('examples', 'test_referee.py').to_s )
    @match_wrapper = RoundWrapper.new(@referee , 2, 5, [@player1, @player2], 1)
  end

  describe "create successful match" do
    it "should exist" do
      expect(@match_wrapper).to be_an_instance_of RoundWrapper
    end
    it "sucessful game should have results" do
      @match_wrapper.run_match
#      @match_wrapper.results.should have(2).string
      expect(@match_wrapper.match).to include("dumb_player")
      expect(@match_wrapper.match).to include("stupid_player")
    end
  end
end

describe "RoundWrapper" do
  before :each do
    @user = FactoryGirl.create(:user)
    @contest = FactoryGirl.create(:contest)
    @player1 = FactoryGirl.create(:player, user: @user, contest: @contest, name: 'dumb_player', file_location: Rails.root.join('examples', 'test_player.py').to_s )
    @player2 = FactoryGirl.create(:player, user: @user, contest: @contest, name: 'stupid_player', file_location: Rails.root.join('examples', 'test_player.py').to_s )
    @referee = FactoryGirl.create(:referee, name: "referee", file_location: Rails.root.join('spec', 'files', 'dumb_referee.py').to_s )
    @match_wrapper = RoundWrapper.new(@referee , 2, 5, [@player1, @player2], 1)
  end

  it "bad game, results should be inconclusive - referee timed out" do
    expect(@match_wrapper).to be_an_instance_of RoundWrapper
    @match_wrapper.run_match
    expect(@match_wrapper.status[:message]).to eql "INCONCLUSIVE: Referee failed to provide a port!"
  end
end

describe "RoundWrapper" do
  before :each do
    @user = FactoryGirl.create(:user)
    @contest = FactoryGirl.create(:contest)
    @player1 = FactoryGirl.create(:player, user: @user, contest: @contest, name: 'dumb_player', file_location: Rails.root.join('spec', 'files', 'dumb_player.py').to_s )
    @player2 = FactoryGirl.create(:player, user: @user, contest: @contest, name: 'stupid_player', file_location: Rails.root.join('spec', 'files', 'dumb_player.py').to_s )
    @referee = FactoryGirl.create(:referee, name: "referee", file_location: Rails.root.join('examples', 'test_referee.py').to_s )
    @match_wrapper = RoundWrapper.new(@referee , 2, 5, [@player1, @player2], 1)
  end
	after :each do
		system("killall python3")
	end

  it "bad game, results should be inconclusive - game exceeded allowed time" do
    expect(@match_wrapper).to be_an_instance_of RoundWrapper
    @match_wrapper.run_match
    expect(@match_wrapper.status[:message]).to eql "INCONCLUSIVE: Game exceeded allowed time!"
  end
end

#Test timeout for final game results
