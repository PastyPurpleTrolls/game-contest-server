class MatchesController < ApplicationController
  before_action :ensure_user_logged_in, except: [:index, :show]
  before_action :ensure_contest_creator, only: [:edit, :update, :destroy]

 def new
	 @contests = Contest.all
    if params[:contest_id] != 'not-specified'
   		@contest = Contest.friendly.find(params[:contest_id])
			@match = @contest.matches.build
			@match.manager.players.each do |f|
				@match.player_matches.build(player: f )
			end
   	end
   #@match.earliest_start = Time.now
  end 

  def create	
    @contest = Contest.friendly.find(params[:contest_id])
    contest = Contest.friendly.find(params[:contest_id])
    round_limit = params[:match][:num_rounds]
    if params[:match][:player_ids] && params[:match][:player_ids].any? { |player_id, player_in_use| Player.find(player_id).user_id == current_user.id}
        if params[:match][:player_ids].uniq{|p| Player.find(p).contest_id}.length > 1
					flash.now[:danger] = 'Players from multiple contests'
					render 'new'					
					return
				end
				@match = @contest.matches.build(acceptable_params)
        @match.status = "waiting"
        if @match.save
						flash[:success] = 'Match created.'
				else
						@contests = Contest.all
						flash.now[:danger] = 'Match not saved'
						render 'new'
						return
				end
				redirect_to @match
    else   	
        @match = @contest.matches.build(acceptable_params)
				@contests = Contest.all
				flash.now[:danger] = 'You need to select at least one of your own players.'
				render action: 'new'
		end
  end

  def show
    @match = Match.friendly.find(params[:id])
		unless @match.tournament_match?
#			ensure that user is logged in, and that the user has a player in the challenge match
			ensure_correct_user_from_list(list_of_users_in_match(@match), 'You do not have a player in this challenge match')
		end
  end

  def index
    if params[:tournament_id]
			@is_challenge_matches = false
      @manager = Tournament.friendly.find(params[:tournament_id])
    elsif params[:contest_id]
			@is_challenge_matches = true
      @manager = Contest.friendly.find(params[:contest_id])
			
			@users_in_challenge_matches_of_contest = []
			@manager.matches.each do |match|
				@users_in_challenge_matches_of_contest.concat(list_of_users_in_match(match))
=begin
				match.players.each do |player|
					@users_in_challenge_matches_of_contest << player.user
				end
=end
			end

			# ensure that user is logged in, and that the user has a player in contest's challenge matches
			ensure_correct_user_from_list(@users_in_challenge_matches_of_contest, 'Unable to find matches')


			# the following code is relevant if ensure_correct_user_from_list does not redirect to root or a login
			# find all the contest's challenge matches in which the user has a player participating in
			@matches = Match.joins(:players).where(players: {user: current_user , contest:@manager })
			return 
=begin
			# store in an array all the user's players in the contest 
			@players_of_user_in_contest = Player.where(user: current_user, contest: @manager).to_a

			# store in an array all the contest's challenge matches
			@matches = @manager.matches.to_a #Match.where(manager: @manager)#, players: @users_players_in_contest)

			# loop for removing the contest's challenge matches that the user is not involved in 
			@matches.keep_if do |match| 
				@keep = false # boolean for determining if the match is to be kept in the array
				match.players.each do |player| 
					# if user has 1 or more players in the challenge match, keep the challenge match
					@keep = @players_of_user_in_contest.include?(player)
					break if @keep # break for sake of efficiency 
				end
				@keep
			end
=end

    else
      flash[:danger] = "Unable to find matches"
      redirect_to root_path
    end
  end

#  def edit
#    @match = Match.friendly.find(params[:id])
#  end


#  def update
#    @match = Match.frendly.find(params[:id])
#    @match.player_matches.each do |player_match|
#	player_match.destroy
#    end
#    if @match.update (acceptable_params)
#	flash[:success] = "Match updated."
#	redirect_to @match
#    else
#	render 'edit'
#    end
#  end

  def destroy
    @match = Match.friendly.find(params[:id])
    @match.player_matches.each{ |m|m.destroy}
    @match.parent_matches.each{ |m|m.destroy}
    @match.child_matches.each{ |m|m.destroy}
    @match.destroy
    redirect_to @match.manager
  end


  private

  def acceptable_params
    params.require(:match).permit(:earliest_start, :num_rounds, player_ids: [])
  end

end
