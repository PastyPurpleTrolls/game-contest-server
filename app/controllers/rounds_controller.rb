class RoundsController < ApplicationController
  before_action :ensure_user_logged_in, only: [:show]
	def show
		@round = Round.friendly.find(params[:id])
		# ensure that user is logged in, and that the user has a player in the challenge match
		@list_of_users_in_match = list_of_users_in_match(@round.match)
		ensure_correct_user_from_list(@list_of_users_in_match, 'You do not have a player in this round')
	end
end
