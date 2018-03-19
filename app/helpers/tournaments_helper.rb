module TournamentsHelper
  def get_player_results(tournament)
    @results = {}
    initialize_hash(tournament)
    populate_results(tournament)
    populate_wins
    populate_ranks
    @results
  end

  def initialize_hash(tournament)
    tournament.players.each do |p1|
      @results[p1.id] = {}
      @results[p1.id][:results] = {}
      tournament.players.each do |p2|
        @results[p1.id][:results][p2.id] = {}
        @results[p1.id][:results][p2.id]['Win'] = 0
        @results[p1.id][:results][p2.id]['Loss'] = 0
        @results[p1.id][:results][p2.id]['Tie'] = 0
        @results[p1.id][:wins] = 0
        @results[p1.id][:rank] = 0
      end
    end
  end

  def populate_results(tournament)
    tournament.matches.each do |match|
      match.rounds.each do |round|
        round.player_rounds.each do |player_round|
          player_id = player_round.player_id
          player_ids = []
          round.players.each { |p| player_ids << p.id }
          opponent_id = player_ids.detect { |id| player_id != id }
          @results[player_id][:results][opponent_id][player_round.result] += 1
        end
      end
    end
  end

  def populate_wins
    @results.keys.each do |p1_id, data|
      wins = 0
      @results[p1_id][:results].each do |p2_id, result|
        if result['Win'] > result['Loss']
          wins += 1
        end
      end
      @results[p1_id][:wins] = wins
    end
  end

  def populate_ranks
    player_wins_arr = get_player_wins_array
    rank = 0
    previous_win_count = nil

    player_wins_arr.each do |arr|
      player_id = arr[0]
      current_win_count = @results[player_id][:wins]

      if previous_win_count != current_win_count
        rank += 1
        previous_win_count = current_win_count
      end

      @results[player_id][:rank] = rank
    end
  end

  def get_player_wins_array
    player_wins_arr = []
    @results.each do |player_id, data|
      player_wins_arr << [player_id, data[:wins]]
    end
    player_wins_arr.sort_by(&:last).reverse
  end

  def get_player_attributes(tournament)
    data = {}
    tournament.players.each do |player|
      data[player.id] = {}
      data[player.id]['user_name'] = player.user.username
      data[player.id]['player_name'] = player.name
    end
    data
  end

  def get_player_attrs_with_rank(player_wins, player_attributes, rank)
    players_with_rank = []
    player_wins.each do |player_win|
      if @results[player_win[0]][:rank] == rank
        players_with_rank << player_attributes[player_win[0]]
      end
    end
    players_with_rank
  end
end