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
      flash[:success] = "Welcome to the site: #{@user.username}"
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
    @user = User.friendly.find(params[:id])
  end

  def edit
  end

  def update
		if current_user.admin? && @user.update(admin_acceptable_params)
      flash[:success] = @user.username + "'s profile has been modified"
      redirect_to @user
    elsif @user.update(acceptable_params)
      flash[:success] = "Your profile has been modified"
      redirect_to @user
    else
      render 'edit'
    end
  end

  def destroy
    @user.destroy
    flash[:success] = "#{@user.username} removed from the site"
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
    unless !current_user?(@user)
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
