module ApplicationHelper
    def setTitle(title)
        content_for(:title) { title }
    end

    def startTestMatch(player_id, contest)
	match_params = { player_ids: [player_id], num_rounds: 1, status:"waiting", earliest_start:Time.now }
	played_match = contest.matches.create!( match_params )
    end
end
