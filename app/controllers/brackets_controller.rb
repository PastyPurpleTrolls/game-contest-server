class BracketsController < ApplicationController
  # incorrect scoring
  # scoring when more than 1 match
  # handle ties referee has to decide winner
  def show
    tourney = Tournament.friendly.find(params[:id])
    match_ids = get_match_ids(tourney.id)
    player_ids = get_player_ids(tourney.id)
    names = get_names(player_ids)
    bracket = create_json_bracket(player_ids, match_ids, names)
    render json: bracket
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
    res = Player.where(id: player_ids).reorder(id: :asc)
    res.each do |row|
      names.insert(0, row.name)
    end
    return names
  end

  def get_match_results(matches)
    results = []
    matches.each do |row|
      x = row.result
      if (row.result.eql? 'Win')
        results.push(1)
      else
        results.push(0)
      end
    end
    return results
  end

  def create_json_bracket(player_ids, match_ids, names)
    if (names.length == 0)
      raise 'No players were found'
    end
    return build_tournament_bracket(names, player_ids, match_ids).to_json
  end

  def build_results(results, match_results, number_of_matches, bracket, depth)
    i = 0
    round_depth = Math.log2(number_of_matches).ceil
    number_of_matches = 2 ** (round_depth - 1)

    results = Array.new(round_depth, []) if results.nil?
    results[depth] = Array.new(number_of_matches, [])

    while i < (number_of_matches)
      if (!match_results.any?)
        results[depth][i] = [nil, nil]
      elsif (match_results.length == 1)
        results[depth][i] = [match_results.shift(1), nil]
      else
        results[depth][i] = match_results.shift(2)
      end
      i += 1
    end 

    if round_depth <= depth
      return bracket[:results] = results
    else
      depth += 1
      build_results(results, match_results, number_of_matches, bracket, depth)
    end
  end

  def build_tournament_bracket(names, player_ids, match_ids)
    i = 0
    count = names.length
    round_depth = Math.log2(count).ceil
    teams_size = 2 ** (round_depth - 1)

    results = []
    bracket = {:teams => [], :results =>  []}
    matches = PlayerMatch.where(match_id: match_ids).reorder(id: :asc)
    match_results = get_match_results(matches)

    while i < (teams_size)
      if (!names.any?)
        results[i] = ( [nil, nil] )
      elsif (names.length == 1)
        results[i] = [names.pop, nil]
      else
        results[i] = names.pop(2)
      end
      i += 1
    end 

    bracket[:teams] = results.reverse
    bracket[:results] = build_results(nil, match_results, count, bracket, 0)
    return bracket
  end
end