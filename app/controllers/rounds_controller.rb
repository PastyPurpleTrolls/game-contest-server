class RoundsController < ApplicationController
  before_action :ensure_user_logged_in, only: [:show]

	def new
		@round = Round.new
		
	end

	def create
		@round = Round.create		
	end	

	def show
		@round = Round.friendly.find(params[:id])
        @match = @round.match

        if @match.manager_type.to_s == "Contest"
            @referee = @match.manager.referee
        else
            @referee = @match.manager.contest.referee
        end
	end
end
