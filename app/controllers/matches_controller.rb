class MatchesController < ApplicationController
  include MatchesHelper

  before_action :ensure_user_logged_in, except: [:index, :show]
  before_action :ensure_contest_creator, only: :destroy

  def new
    @contests = Contest.all
    if params[:contest_id] != 'not-specified'
      @contest = Contest.friendly.find(params[:contest_id])
      contest = Contest.friendly.find(params[:contest_id])
      @match = contest.matches.build
      @match.manager.players.each do |f|
        @match.player_matches.build(player: f)
      end
    end
  end

  def create
    @contest = Contest.friendly.find(params[:contest_id])
    player_ids = params[:match][:player_ids]
    if selected_own_players(params[:match][:player_ids])
      if players_unplayable(player_ids, current_user)
        flash.now[:danger] = 'Not all players are playable'
        redirect_to root_path
      elsif players_from_multiple_contests(player_ids)
        flash.now[:danger] = 'Players from multiple contests'
        render 'new'
      else
        @match = @contest.matches.build(acceptable_params)
        @match.status = "waiting"
        if @match.save
          redirect_to @match
        else
          @contests = Contest.all
          flash.now[:danger] = 'Match not saved'
          render 'new'
        end
      end
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
      ensure_correct_user_from_list(list_of_users_in_match(@match), 'You do not have a player in this challenge match')
    end
    @rounds = @match.rounds.paginate(:per_page =>10, :page => params[:page])
  end

  def destroy
    @match = Match.friendly.find(params[:id])
    @match.player_matches.each {|m| m.destroy}
    @match.parent_matches.each {|m| m.destroy}
    @match.child_matches.each {|m| m.destroy}
    @match.destroy
    redirect_to @match.manager
  end

  private

  def acceptable_params
    params.require(:match).permit(:earliest_start, :num_rounds, player_ids: [])
  end
end