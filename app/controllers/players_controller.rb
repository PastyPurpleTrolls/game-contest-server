class PlayersController < ApplicationController
  include ApplicationHelper
  before_action :ensure_user_logged_in, except: :show
  before_action :ensure_player_owner, only: [:edit, :update, :destroy]

  require 'will_paginate/array'

  def new
    @contests = Contest.all
    if params[:contest_id] != 'not-specified'
      @contest = Contest.friendly.find(params[:contest_id])
      @player = @contest.players.build
    end
  end

  def create
    @contest = Contest.friendly.find(params[:contest_id])
    @player = @contest.players.build(acceptable_create_params)
    @player.upload = params[:player][:upload]
    @player.user = current_user
    if @player.save
      startTestMatch(@player.id, @contest)
      redirect_to @player
    else
      @contests = Contest.all
      render 'new'
    end
  end

  def show
    @per_page = 10
    @player = Player.friendly.find(params[:id])
    @playermatch = PlayerMatch.search(@player, params[:search])
    @matches = PlayerMatch.search(@player, params[:search]).paginate(:per_page =>10, :page => params[:page])
  end

  def edit
  end

  def update
    if @player.update(acceptable_update_params)
      redirect_to @player
    else
      render 'edit'
    end
  end

  def destroy
    @player.destroy
    redirect_to contest_path(@player.contest)
  end

  private

  def acceptable_update_params
     params.require(:player).permit(:name, :description, :downloadable, :playable, :upload)
  end

  def acceptable_create_params
     params.require(:player).permit(:name, :description, :downloadable, :playable)
  end

  def ensure_player_owner
    @player = Player.friendly.find(params[:id])
    ensure_correct_user(@player.user_id)
  end
end
