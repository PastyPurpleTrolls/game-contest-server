class ContestsController < ApplicationController
  include ContestsHelper

  before_action :ensure_user_logged_in, except: [:index, :show]
  before_action :ensure_contest_creator, except: [:index, :show]
  before_action :ensure_contest_owner, only: [:edit, :update, :destroy]

  def index
    @per_page = 10
    @contests = Contest
                    .search(params[:search])
                    .paginate(per_page: @per_page, page: params[:page])
  end

  def new
    @referees = Referee.all
    @contest = Contest.new
  end

  def create
    @contest = current_user.contests.build(acceptable_params)
    if @contest.save
      redirect_to @contest
    else
      @referees = Referee.all
      render 'new'
    end
  end

  def edit
  end

  def update
    if @contest.update(acceptable_params)
      redirect_to @contest
    else
      render 'edit'
    end
  end

  def show
    @per_page = 10
    @contest = Contest.friendly.find(params[:id])
    @tournaments = @contest.tournaments
                       .search(params[:tournament_search])
                       .paginate(per_page: @per_page, page: params[:tournament_page])
    @players = @contest.players
                   .search(params[:player_search])
                   .paginate(per_page: @per_page, page: params[:player_page])
  end

  def destroy
    @contest.tournaments.each{|t|t.destroy}
    @contest.matches.each{|m|m.destroy}
    @contest.players.each{|p|p.destroy}
    @contest.destroy
    redirect_to contests_path
  end

  private

  def acceptable_params
    params.require(:contest).permit(:deadline, :description, :name,  :referee_id)
  end

  def ensure_contest_owner
    @contest = Contest.friendly.find(params[:id])
    ensure_correct_user(@contest.user_id)
  end
end
