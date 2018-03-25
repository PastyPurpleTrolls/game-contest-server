module ApplicationHelper
  def setTitle(title)
    content_for(:title) {title}
  end

  def startTestMatch(player_id, contest)
    match_params = {player_ids: [player_id], num_rounds: 1, status: "waiting", earliest_start: Time.now}
    played_match = contest.matches.create!(match_params)
  end

  def timeRelativeToNow(time)
    time_in_words = distance_of_time_in_words_to_now(time).split.map {|i| i.capitalize}.join(' ')
    if time < Time.now
      "#{time_in_words} Ago"
    else
      "In #{time_in_words}"
    end
  end

  def getRangeFromPage(page, num_on_page)
    if page.nil?
      page = 1
    else
      page = page.to_i
    end
    first_record = (page-1) * 10 + 1
    last_record = (page-1) * 10 + num_on_page
    "#{first_record}-#{last_record}"
  end

  def yesno(bool)
    bool ? 'Yes' : 'No'
  end

  def display_results_found(collection, collection_name, current_page, results_per_page)
    if collection.count > 0
      text = "#{collection.count} found"
      if collection.count > results_per_page
        text += " (displaying #{getRangeFromPage(current_page, collection.length)})"
      end
      text
    else
      "No #{collection_name} found"
    end
  end
end
