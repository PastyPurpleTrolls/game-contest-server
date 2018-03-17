module TournamentsHelper
  def get_player_results(tournament)
    @results = {}
    initialize_hash(tournament)
    populate_hash(tournament)
    @results
  end

  def initialize_hash(tournament)
    tournament.players.each do |p1|
      @results[p1.id] = {}
      tournament.players.each do |p2|
        @results[p1.id][p2.id] = {}
        @results[p1.id][p2.id]["Win"] = 0
        @results[p1.id][p2.id]["Loss"] = 0
        @results[p1.id][p2.id]["Tie"] = 0
      end
    end
  end

  def populate_hash(tournament)
    tournament.matches.each do |m|
      m.rounds.each do |r|
        r.player_rounds.each do |pr|
          cur = pr.player_id
          player_ids = []
          r.players.each { |p| player_ids << p.id }
          other = player_ids.detect { |id| cur != id }
          @results[cur][other][pr.result] += 1
        end
      end
    end
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

  def get_player_wins(results, player_id)
    wins = 0
    results[player_id].each do |match_result|
      if match_result[1]["Win"] > match_result[1]["Loss"]
        wins += 1
      end
    end
    wins
  end
end