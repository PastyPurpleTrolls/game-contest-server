class HelpController < ApplicationController
  include ApplicationHelper

  before_action :ensure_user_logged_in

  def index
  end


  # General

  def terminology
  end


  # Administrator Role

  def erd
  end

  private

  def ensure_admin
    unless current_user.admin
      flash[:danger] = 'Not an administrator.'
      redirect_to root_path
    end
  end
end
