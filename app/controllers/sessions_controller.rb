class SessionsController < ApplicationController
  before_action :ensure_user_logged_out, only: [:new, :create]
  before_action :ensure_user_logged_in, only: [:destroy]

  def new
  end

  def create
    if session[:redirect_to] != nil then
      redirect_back_to_previous user
    end

    user = User.find_by(username: params[:username])
    if user && user.authenticate(params[:password])
      login user
      redirect_to root_path
    else
      flash.now[:danger] = 'Invalid username or password'
      render 'new'
    end
  end

  def destroy
    logout
    flash[:info] = 'Logged out.'
    redirect_to root_path
  end
end
