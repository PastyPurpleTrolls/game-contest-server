class BracketsController < ApplicationController
  # 32 155~170 34~18
  # 33 171~188 34~16
  # handle ties referee has to decide winner
  def show
    tourney = Tournament.friendly.find(params[:id])
    match_ids = get_match_ids(tourney.id)
    player_ids = get_player_ids(tourney.id)
    stage1 = gen_match_paths(match_ids, player_ids)
    stage2 = gen_scores(stage1)
    # bracket = generate_bracket(player_ids, match_ids, get_names(player_ids))
    render json: stage1.to_json
  end

  private
  def get_match_ids(tourney_id)
    matches = []
    res = Match.where(manager_id: tourney_id).reorder(id: :asc)
    res.each do |row|
      matches.push(row.id)
    end
    return matches
  end

  def get_player_ids(tourney_id)
    players = []
    res = PlayerTournament.where(tournament_id: tourney_id).reorder(id: :asc)
    res.each do |row|
      players.push(row.player_id)
    end
    return players
  end

  def get_names(player_ids)
    names = []
    res = Player.select(:id, :name).where(id: player_ids).reorder(id: :asc)
    res.each do |row|
      names.insert(0, row.name)
    end
    return names
  end

  def gen_match_paths(matches, players)
    i = 1
    j = 0
    matches_per_round = 2
    names = get_names(players)
    round_depth = Math.log2(names.length).ceil
    final_match = matches.first
    num_of_players = players.count
    res = MatchPath.select(:parent_match_id, :child_match_id, :result)
    .where(parent_match_id: matches).reorder(parent_match_id: :asc)
    
    match_paths = Array.new(round_depth, [])
    match_paths[0] = [final_match]

    while (i < round_depth)
      j = 0
      k = 0
      match_paths[i] = Array.new(matches_per_round, nil)
      while (k < match_paths[i-1].count)
        results = res.where(child_match_id: match_paths[i - 1][k])
        if (!results.blank?)
          results.each do |row|
            match_paths[i][j] = row.parent_match_id
            j += 1
          end
        else
          match_paths[i][j] = nil
          j += 1
        end
        k += 1
      end

      i += 1
      matches_per_round *= 2
    end
    return match_paths
  end

  def gen_scores()
    
  end

  # def number_of_matches(round_depth)
  #   return 2 ** (round_depth - 1)
  # end

  # def extra_players?(names)
  #   team_size_diff = names.length - (2 ** Math.log2(names.length).floor)
  #   if(team_size_diff == 0)
  #     return 0
  #   else
  #     return team_size_diff
  #   end
  # end

  # def generate_bracket(player_ids, match_ids, names)
  #   i = 0
  #   players = []
  #   extra_players = []
  #   depth = Math.log2(names.length).floor
  #   team_matchups = number_of_matches(depth) * 2
  #   extra_names = extra_players?(names)
  #   bracket = {:teams => [], :results =>  []}

  #   if(extra_names != 0)
  #     extra_players = names.pop(extra_names)
  #   end

  #   while i < (team_matchups / 2)
  #     players[i] = [names.shift, names.shift]
  #     i += 1
  #   end

  #   bracket[:teams] = players
  #   bracket[:results] = generate_results(Math.log2(team_matchups).to_i)
  #   return bracket
  # end

  # def generate_results(depth)
  #   results = Array.new(depth, [])
  #   matches_per_round = number_of_matches(depth)

  #   (0..(depth - 1)).step(1) do |i|
  #     matches_per_round = number_of_matches(depth)
  #     results[i] = Array.new(matches_per_round, [nil, nil])
  #     depth -= 1
  #   end

  #   return results
  # end

  # def populate_bracket()
  #   return nil
  # end

  # def build_results(results, match_results, number_of_matches, bracket, depth)
  #   i = 0
  #   round_depth = Math.log2(number_of_matches).ceil
  #   number_of_matches = 2 ** (round_depth - 1)

  #   results = Array.new(round_depth, []) if results.nil?
  #   results[depth] = Array.new(number_of_matches, [])

  #   while i < (number_of_matches)
  #     if (!match_results.any?)
  #       results[depth][i] = [nil, nil]
  #     elsif (match_results.length == 1)
  #       results[depth][i] = [match_results.shift(1), nil]
  #     else
  #       results[depth][i] = match_results.shift(2)
  #     end
  #     i += 1
  #   end

  #   if round_depth <= depth
  #     return bracket[:results] = results
  #   else
  #     depth += 1
  #     build_results(results, match_results, number_of_matches, bracket, depth)
  #   end
  # end
end