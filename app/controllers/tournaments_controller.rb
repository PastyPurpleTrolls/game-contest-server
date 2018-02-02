class TournamentsController < ApplicationController
  before_action :ensure_user_logged_in, except: :show
  before_action :ensure_contest_creator, except: :show
  before_action :ensure_contest_owner, only: [:new ,:edit, :update , :destroy]

  include TournamentsHelper

  def new
    @contests = Contest.all
    if params[:contest_id] != 'not-specified'
      @tournament = @contest.tournaments.build
      @tournament.contest.players.each do |f|
        @tournament.player_tournaments.build(player: f )
      end
      @tournament.start = Time.now
    end
  end

  def create
    @contest = Contest.friendly.find(params[:contest_id])
    if params[:tournament][:player_ids] && params[:tournament][:player_ids].uniq{|p| Player.find(p).contest_id}.length > 1
      flash.now[:danger] = 'Players from multiple contests'
      render 'new'					
      return
    end
    @tournament = @contest.tournaments.build(acceptable_params)
    @tournament.status = "waiting"
    if @tournament.save
      redirect_to @tournament
    else
      @contests = Contest.all
      render 'new'
    end
  end

  def edit
    @tournament = Tournament.friendly.find(params[:id])
  end

  def update
    @tournament = Tournament.friendly.find(params[:id])
    @tournament.player_tournaments.each do |player_tournament|
      player_tournament.destroy
    end
    if @tournament.update(acceptable_params)
      redirect_to @tournament
    else
      render 'edit'
    end
  end

  def show
    @tournament = Tournament.friendly.find(params[:id])
    @results = get_player_results(@tournament)
    @player_attributes = get_player_attributes(@tournament)
  end

  def destroy
    @tournament = Tournament.friendly.find(params[:id])
    @tournament.player_tournaments.each{|m|m.destroy}
    @tournament.matches.each{|m|m.destroy}
    @tournament.destroy
    redirect_to contest_path(@tournament.contest)
  end

  private

  def acceptable_params
    # Status should not be acceptable.
    # The backend should set it.
    params.require(:tournament).permit(:name , :start, :tournament_type,:rounds_per_match, :total_matches, player_ids: [])
  end

  def ensure_contest_owner
    if params.include?(:contest_id) && params[:contest_id] != "not-specified"
      @contest = Contest.friendly.find(params[:contest_id])
      ensure_correct_user(@contest.user_id)
    elsif params.include? :id
      @contest = Tournament.friendly.find(params[:id]).contest
      ensure_correct_user(@contest.user_id)
    end
  end

end
