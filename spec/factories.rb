require 'fileutils'

FactoryGirl.define do
  factory :user do
    sequence(:username) { |i| "User #{i}" }
    email    "john.doe@example.com"
    password "password"
    password_confirmation "password"
    chat_url "http://example.com/path/to/chat"

    factory :admin do
      admin true
    end

    factory :contest_creator do
      contest_creator true
    end

    factory :banned_user do
      banned true
    end
  end

  factory :referee do
    sequence(:file_location) do |i|
      location = Rails.root.join('code',
                                 'referees',
                                 'test',
                                 SecureRandom.hex)
      FileUtils.mkdir_p(location.to_s)
      finalLocation = location.join("FactoryGirl-fake-code-#{i}").to_s
      FileUtils.touch(finalLocation)
      finalLocation
    end
    sequence(:compressed_file_location) do |i|
      location = Rails.root.join('code',
                                 'environments',
                                 'test',
                                 SecureRandom.hex)
      FileUtils.mkdir_p(location.to_s)
      finalLocation = location.join("FactoryGirl-fake-code-#{i}").to_s
      FileUtils.touch(finalLocation)
      finalLocation
    end
    sequence(:name) { |i| "Referee #{i}" }
    rules_url "http://example.com/path/to/rules"
    players_per_game 4
    time_per_game 10
    user
    round_limit 150
		rounds_capable false 
  end

  factory :contest do
    user
    referee
    deadline 1.day.from_now
    description "Contest Description Here"
    sequence(:name) { |i| "Contest #{i}" }
  end

  factory :tournament do
    contest
    sequence(:name) { |i| "Tournament #{i}" }
    start Time.current
    tournament_type "round robin"
    rounds_per_match 1
    status "waiting"
  end

  factory :player_tournament do
    player
    tournament
  end

  factory :match do
    #
    # we cannot validate the match on save because we haven't created
    # all the proper associations for the match until after the save
    # is completed (e.g., players, player_matches, and possibly
    # player_tournaments).  We make sure to call match.save! after
    # they've all be created properly to ensure that the validations
    # are passed before the factory returns.
    #
    to_create {|instance| instance.save(validate: false) }

    ignore { player nil }

    status "waiting"
    completion Time.current
    earliest_start Time.current
		num_rounds 4

    factory :tournament_match do
      association :manager, factory: :tournament
      #association :match_log_info, factory: :match_log_info_referee
      
      factory :winning_match do
	after(:create) do |match, evaluator|
	  pm = PlayerMatch.where(match: match,
				 player: evaluator.player).first
	  pm.result = "Win"
	  pm.save!
	  match.reload
	end
      end

      factory :losing_match do
	after(:create) do |match, evaluator|
	  pm = PlayerMatch.where(match: match,
				 player: evaluator.player).first
	  pm.result = "Loss"
	  pm.save!
	  match.reload
	end
      end

      after(:create) do |match, evaluator|
	num_players = match.manager.referee.players_per_game

	if evaluator.player
	  num_players -= 1
	  create(:player_match, player: evaluator.player, match: match)
	  create(:player_tournament, player: evaluator.player, tournament: match.manager)
	end

	num_players.times do
	  player = create(:player, contest: match.manager.contest)
	  create(:player_match, player: player, match: match)
	  create(:player_tournament, player: player, tournament: match.manager)
	end

	match.num_rounds.times do
		round = create(:round, match: match)
	end

	match.save!
      end
    end

    factory :challenge_match do
      association :manager, factory: :contest

      after(:create) do |match, evaluator|
        num_players = match.manager.referee.players_per_game

       	if evaluator.player
	  num_players -= 1
	  create(:player_match, player: evaluator.player, match: match)
	end

        num_players.times do
	  player = create(:player, contest: match.manager.contest)
	  create(:player_match, player: player, match: match)
        end

		match.num_rounds.times do
			round = create(:round, match: match)
		end

        match.save!
      end
    end
  end

  factory :round do
    to_create {|instance| instance.save(validate: false) }
    factory :challenge_round do
      association :match, factory: :challenge_match
    end

    factory :tournament_round do
      association :match, factory: :tournament_match
    end
    after(:create) do |round, evaluator|
      round.match.players.each do |player|
        create(:player_round, round: round, player: player)
      end
    end 
  end


  factory :player do
    user
    contest
    sequence(:file_location) do |i|
      location = Rails.root.join('code',
                                 'players',
                                 'test',
                                 SecureRandom.hex)
      FileUtils.mkdir_p(location.to_s)
      finalLocation = location.join("FactoryGirl-fake-code-#{i}").to_s
      FileUtils.touch(finalLocation)
      finalLocation
    end
    description "Player Description Here"
    sequence(:name) { |i| "Player #{i}" }
  end

  factory :player_match do
    player
    association :match, factory: :tournament_match
    #association :match_log_info, factory: :match_log_info_player
    result "Unknown Result"
  end
  
  factory :player_round do 
    player
    association :round, factory: :challenge_round 
    result nil 
    score 1.0
  end

  factory :match_log_info do

    factory :match_log_info_referee do
      association :match_source, factory: :tournament_match

      after(:create) do |log_info, evaluator|
        location = File.dirname(log_info.match_source.manager.referee.file_location)+"/logs/"
        log_info.log_stdout = location+"test_out.tgz"
        log_info.log_stderr = location+"test_err.tgz"
	FileUtils.mkdir_p(location)
        FileUtils.touch(log_info.log_stdout)
        FileUtils.touch(log_info.log_stderr)
        log_info.save!
      end
    end

    factory :match_log_info_player do
      association :match_source, factory: :player_match
  
      after(:create) do |log_info, evaluator|
        location = File.dirname(log_info.match_source.player.file_location)+"/logs/"
        log_info.log_stdout = location+"test_out.tgz"
        log_info.log_stderr = location+"test_err.tgz"
        FileUtils.mkdir_p(location)
        FileUtils.touch(log_info.log_stdout)
        FileUtils.touch(log_info.log_stderr)
        log_info.save!
      end
    end
  end

end
