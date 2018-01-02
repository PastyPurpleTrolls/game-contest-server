require 'rails_helper'

describe Match do
  let (:match) { FactoryBot.create(:tournament_match) }
  subject { match }

  # Tables
  it { should respond_to(:players) }
  it { should respond_to(:player_matches) }
  it { should respond_to(:manager) }
  # Attributes
  it { should respond_to(:manager_type) }
  it { should respond_to(:status) }
  it { should respond_to(:earliest_start) }
  it { should respond_to(:completion) }
	it { should respond_to(:num_rounds) }

  # Do not do manager_type tests as it is set by rails

  describe "empty status" do
    before { match.status = '' }

    it { should_not be_valid }
  end

  describe "blank status" do
    before { match.status = ' ' }

    it { should_not be_valid }
  end

  describe "valid status" do
    valid_statuses = %w[unassigned waiting started completed]
    valid_statuses.each do |status|
      it "is valid" do
        match.status = status
        expect(match).to be_valid
      end
    end
  end

  describe "invalid status" do
    invalid_statuses = %w[
      Unassigned Waiting Started Completed Pending
      unassign wait start complete pend
      u w s c p
      before during after
      ]
    invalid_statuses.each do |status|
      it "is invalid" do
        match.status = status
        expect(match).not_to be_valid
      end
    end
  end

  describe "empty earliest_start" do
    describe "waiting" do
      before do
        match.status = 'waiting'
        match.earliest_start = ''
      end

      it { should_not be_valid }
    end

    describe "started" do
      before do
        match.status = 'started'
        match.earliest_start = ''
      end

      it { should be_valid }
    end

    describe "completed" do
      before do
        match.status = 'completed'
        match.earliest_start = ''
      end

      it { should be_valid }
    end
  end

  describe "blank earliest_start" do
    describe "waiting" do
      before do
        match.status = 'waiting'
        match.earliest_start = ' '
      end

      it { should_not be_valid }
    end

    describe "started" do
      before do
        match.status = 'started'
        match.earliest_start = ' '
      end

      it { should be_valid }
    end

    describe "completed" do
      before do
        match.status = 'completed'
        match.earliest_start = ' '
      end

      it { should be_valid }
    end
  end

  describe "completion in past" do
    before do
      match.status = 'completed'
      match.completion = 1.day.ago
    end

    it { should be_valid }
  end

  describe "completion now" do
    before do
      match.status = 'completed'
      Timecop.freeze
      match.completion = Time.current
    end

    after { Timecop.return }

    it { should be_valid }
  end

  describe "completion in future" do
    before do
      match.status = 'completed'
      match.completion = 1.day.from_now
    end

    it { should_not be_valid }
  end

  describe "not completed in future" do
    before do
      match.completion = 1.day.from_now
    end

    it { should be_valid }
  end

  describe "too few players" do
    failures = %w( waiting started completed )
    failures.each do |status|
      describe "status #{status}" do
        before do
          match.status = status
          match.players.clear
          (match.manager.referee.players_per_game - 1).times do
            player = FactoryBot.create(:player, contest: match.manager.contest)
            player.tournaments << match.manager
            match.players << player
          end
        end
        it { should_not be_valid }
      end # status #{}
    end # loop

    describe "status unassigned" do
      before do
        match.status = 'unassigned'
        match.players.clear
        (match.manager.referee.players_per_game - 1).times do
          player = FactoryBot.create(:player, contest: match.manager.contest)
          player.tournaments << match.manager
          match.players << player
        end
      end
      it { should be_valid }
    end # waiting
  end

  describe "exactly right players" do
    before do
      match.players.clear
      match.manager.referee.players_per_game.times do
        player = FactoryBot.create(:player, contest: match.manager.contest)
        player.tournaments << match.manager
        match.players << player
      end
    end

    it { should be_valid }
  end

  describe "too many players" do
    before do
      match.players.clear
      (match.manager.referee.players_per_game + 1).times do
        player = FactoryBot.create(:player, contest: match.manager.contest)
        player.tournaments << match.manager
        match.players << player
      end
    end

    it { should_not be_valid }
  end

  # Players should be allowed to play each other
  describe "match players set up properly" do
    before do
      ref = FactoryBot.create(:referee, players_per_game: 2)
      contest = FactoryBot.create(:contest, referee: ref)
      tournament = FactoryBot.create(:tournament, contest: contest)
      match.manager = tournament
      match.player.clear
      match.manager.referee.players_per_game do
        player = FactoryBot.create(:player, contest: contest)
        player.tournaments << tournament
        match.players << player
      end
    end
  end

  # This is a kinda confusing test.
  # It makes players that are in the same contest
  # but not in the same tournament try to play in the same
  # match in a tournament, which should not be allowed.
  describe "players are in the same contest, but are not in same tournament" do
    before do
      match.players.clear
      contest = FactoryBot.create(:contest)
      match.manager.referee.players_per_game.times do
        player = FactoryBot.create(:player, contest: contest)
        player.tournaments = FactoryBot.create_list(:tournament, 1, contest: contest)
        # The proof is in the puts
        # puts "player.name        " + player.name
        # puts "player.contest_id  " + player.contest_id.to_s
        # puts "player.tournaments " + player.tournaments[0].id.to_s
        match.players << player
      end
    end

    it { should_not be_valid }
  end

  # This is another kinda confusing test.
  # It makes players that are in different contests try to play
  # in the same match in a tournament, which should not be allowed.
  describe "players not in same contest" do
    before do
      match.players.clear
      match.manager.referee.players_per_game.times do
        player = FactoryBot.create(:player)
        player.tournaments = FactoryBot.create_list(:tournament, 1, contest: player.contest)
        # The proof is in the puts
        # puts "player.name        " + player.name
        # puts "player.contest_id  " + player.contest_id.to_s
        # puts "player.tournaments " + player.tournaments[0].id.to_s
        match.players << player
      end
    end

    it { should_not be_valid }
  end

  describe "players are in same contest and tournament, but the match is in a tournament they do not share" do
    before do
      ref = FactoryBot.create(:referee, players_per_game: 2)
      contest = FactoryBot.create(:contest, referee: ref)
      shared_tournament = FactoryBot.create(:tournament, contest: contest)
      not_shared_tournament = FactoryBot.create(:tournament, contest: contest)
      p1 = FactoryBot.create(:player, contest: contest)
      p1.tournaments << shared_tournament << not_shared_tournament
      p2 = FactoryBot.create(:player, contest: contest)
      p2.tournaments << shared_tournament
      match.manager = not_shared_tournament
      match.players.clear
      match.players << p1 << p2

    end

    it { should_not be_valid }
  end


	describe "has 0 rounds" do
		before do
			match.num_rounds = 0
		end
    it { should_not be_valid }
	end

	describe "has 1 round" do
		before do
			match.num_rounds = 1
		end

		it { should be_valid }	
	end

	describe "num_rounds > referee round_limit" do
		before do
			match.num_rounds = match.manager.contest.referee.round_limit+1
		end
		it { should_not be_valid }
	end


  describe "validations" do
    it { should be_valid }
    specify { expect_required_attribute(:manager) }
  end

end
