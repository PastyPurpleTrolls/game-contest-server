module ApplicationHelper
    def setTitle(title)
        content_for(:title) { title }
    end

    def startTestMatch(player_id, contest)
	match_params = { player_ids: [player_id], num_rounds: 1, status:"waiting", earliest_start:Time.now }
	played_match = contest.matches.create!( match_params )
    end

    def timeRelativeToNow(time)
        time_in_words = distance_of_time_in_words_to_now(time).split.map { |i| i.capitalize }.join(' ')
        if time < Time.now
            "#{time_in_words} Ago"
        else
            "In #{time_in_words}"
        end
    end
end
