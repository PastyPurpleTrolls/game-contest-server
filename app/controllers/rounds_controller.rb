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
	end
end
