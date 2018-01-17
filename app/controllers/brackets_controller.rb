class BracketsController < ApplicationController
  # Display Single Elimination Tournament Bracket Visualized
  def show
    tourney = Tournament.friendly.find(params[:id])
    match_ids = get_match_ids(tourney.id)
    player_ids = get_player_ids(tourney.id)
    tournament_tree = generate_match_paths(match_ids, player_ids)
    results = generate_scores(tournament_tree, match_ids, player_ids)
    players = generate_players(tournament_tree, results, match_ids, player_ids)
    render json: players.to_json
  end

  private
  def get_match_ids(tourney_id)
    matches = []
    query = Match.where(manager_id: tourney_id).reorder(id: :asc)
    query.each do |row|
      matches.push(row.id)
    end
    return matches
  end

  def get_player_ids(tourney_id)
    players = []
    query = PlayerTournament.where(tournament_id: tourney_id).reorder(id: :asc)
    query.each do |row|
      players.push(row.player_id)
    end
    return players
  end

  def get_names(player_ids)
    names = []
    query = Player.select(:id, :name).where(id: player_ids).reorder(id: :asc)
    query.each do |row|
      names.insert(0, row.name)
    end
    return names
  end

  # Build the match tree structure that represents the tournament
  def generate_match_paths(matches, players)
    i, matches_per_round = 1, 2
    round_depth = Math.log2(players.length).ceil
    query = MatchPath.select(:parent_match_id, :child_match_id, :result)
    .where(parent_match_id: matches).reorder(parent_match_id: :asc)
    
    match_paths = Array.new(round_depth, [])
    match_paths[0] = [matches.first]

    while (i < round_depth)
      j, k = 0, 0
      match_paths[i] = Array.new(matches_per_round, nil)
      while (k < match_paths[i - 1].count)
        results = query.where(child_match_id: match_paths[i - 1][k])
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

  # Build the respective scoring for the matches in the tournament
  def generate_scores(stage1, matches, players)
    i, matches_per_round = 0, 1
    round_depth = Math.log2(players.length).ceil
    query = PlayerMatch.select(:player_id, :match_id, :result)
    .where(match_id: matches).reorder(match_id: :asc)
    scores = Array.new(round_depth, [])

    while (i < round_depth)
      j, k = 0, 0
      scores[i] = Array.new(matches_per_round, nil)
      while (k < scores[i].count)
        results = query.where(match_id: stage1[i][k]).first
        if (!results.blank?)
          if results['result'] == "Win"
            scores[i][j] = [1,0]
          else
            scores[i][j] = [0,1]
          end
        else
          scores[i][j] = [nil, nil]
        end
        j += 1
        k += 1
      end

      i += 1
      matches_per_round *= 2
    end
    return scores
  end

  # Build player array for final JSON tournament bracket object
  def generate_players(stage1, stage2, matches, players)
    i, j, x = 0, 0, 0
    names = get_names(players)
    first_round_size = 2 ** (Math.log2(names.length).ceil - 1)
    player_names = Array.new(first_round_size, [])
    extra_players = []
    temp_scores = []
    extra_matchups = stage1.reverse[0].compact()
    query = PlayerMatch.select(:player_id, :match_id, :result)
    .where(match_id: extra_matchups).reorder(match_id: :asc)
    query.each do |row|
      extra_players.push(get_names(row.player_id)[0])
    end

    while (names.length != 0)
      if (extra_players.include? names.first)
        player_names[i] = [extra_players[j], extra_players[j + 1]]
        names.delete(extra_players[j])
        names.delete(extra_players[j + 1])
        j += 2
      else
        player_names[i] = [names.shift(), nil]
      end
      i += 1
    end

    original_scores = stage2.reverse[0]
    while (original_scores.length != 0)
      if ( (original_scores[x].to_s.include? "nil") )
        original_scores.shift
      else
        temp_scores.push(original_scores.shift)
      end
    end

    scores = Array.new(first_round_size, [])
    x = 0
    while (x < first_round_size)
      if (player_names[x].to_s.include? "nil")
        scores[x] = [nil, nil]
      else
        scores[x] = (temp_scores.shift)
      end
      x += 1
    end
    
    stage2[stage2.length - 1] = scores
    bracket = {:teams => player_names, :results => stage2.reverse}
    return bracket
  end
end