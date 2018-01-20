class RoundsController < ApplicationController
  before_action :ensure_user_logged_in, only: [:show]

  def show
    @round = Round.friendly.find(params[:id])

    # ensure that user is logged in, and that the user has a player in the challenge match
    @list_of_users_in_match = list_of_users_in_match(@round.match)
    ensure_correct_user_from_list(@list_of_users_in_match, 'You do not have a player in this round')

    @match = @round.match

    if @match.manager_type.to_s == "Contest"
      @referee = @match.manager.referee
    else
      @referee = @match.manager.contest.referee
    end

    @assets_url = URI.join(root_url, url_for(@referee) + "/", "assets/")
  end
end
