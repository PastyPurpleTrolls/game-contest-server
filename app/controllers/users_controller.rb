class UsersController < ApplicationController
  include ApplicationHelper

  before_action :ensure_user_logged_out, only: [:new, :create]
  before_action :ensure_user_logged_in, only: [:edit, :update, :destroy]
  before_action :ensure_correct_user, only: [:edit, :update]
  before_action :ensure_admin, only: [:destroy]

  def new
    @user = User.new
  end

  def create
    @user = User.new(acceptable_params)
    if @user.save
      login @user
      redirect_to root_path
    else
      render 'new'
    end
  end

  def index
    @per_page = 10
    @users = User.search(params[:search]).paginate(per_page: @per_page, :page => params[:page])
  end

  def show
    @per_page = 10
    @user = User.friendly.find(params[:id])
    @players = @user.players
                   .search(params[:player_search])
                   .paginate(per_page: @per_page, page: params[:player_page])
    if @user.contest_creator
      @referees = @user.referees
                      .search(params[:referee_search])
                      .paginate(per_page: @per_page, page: params[:referee_page])
      @contests = @user.contests
                      .search(params[:contest_search])
                      .paginate(per_page: @per_page, page: params[:contest_page])
    end
  end

  def edit
  end

  def update
		if current_user.admin? && @user.update(admin_acceptable_params)
      redirect_to @user
    elsif @user.update(acceptable_params)
      redirect_to @user
    else
      render 'edit'
    end
  end

  def destroy
    @user.destroy
    redirect_to users_path
  end

  private

  def acceptable_params
    params.require(:user).permit(:username, :password, :password_confirmation, :email)
  end

  def admin_acceptable_params
    params.require(:user).permit(:username, :password, :password_confirmation, :email, :admin, :contest_creator)
  end

  def ensure_admin
    @user = User.friendly.find(params[:id])
    request_okay = true
    if current_user?(@user)
      flash[:danger] = 'Users may not delete themselves.'
      request_okay = false
    end

    unless current_user.admin?
      flash[:danger] = 'Only administrators can delete users.'
      request_okay = false
    end
    redirect_to root_path unless request_okay
  end
end
