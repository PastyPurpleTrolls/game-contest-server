module MatchesHelper
  def list_of_users_in_match(match) # given a match, it returns a list of users participating in the match. It is possible that duplicates of users are included in the list.
    list = []
    match.players.each do |player|
      list << player.user
    end
    list
  end

  def selected_own_players(player_ids)
    player_ids&.any? {|player_id, player_in_use| Player.find(player_id).user_id == current_user.id}
  end

  def players_from_multiple_contests(player_ids)
    player_ids&.uniq {|p| Player.find(p).contest_id}.length > 1
  end

  # Makes sure each player is either playable or owned by the current user
  def players_unplayable(player_ids, user)
    player_ids.each do |pid|
      player = Player.find(pid)
      unless player.playable
        if player.user != user
          return true
        end
      end
    end
    false
  end
end
