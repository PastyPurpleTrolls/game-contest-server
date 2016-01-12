module MatchesHelper
	def list_of_users_in_match(match) # given a match, it returns a list of users participating in the match. It is possible that duplicates of users are included in the list.
		@list = []
		match.players.each do |player|
			@list << player.user
		end
		@list
	end
end
