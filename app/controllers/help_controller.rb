class HelpController < ApplicationController
  include ApplicationHelper

  before_action :ensure_user_logged_in

  def index
  end


  # General

  def terminology
  end


  # Administrator Role

  def admin_capabilities
  end

  def deleting_users
  end

  def changing_user_roles
  end

  def erd
  end

  def manually_running_match
  end


  # Contest Creator Role

  def contest_creator_capabilities
  end

  def creating_contest
  end

  def writing_referee
  end

  def writing_replay_plugin
  end


  # Student Role

  def student_capabilities
  end

  def upload_players_to_contest
  end

  def challenge_other_players
  end

  def view_tournament_results
  end

  def view_challenge_match_results
  end


  private


  def ensure_admin
    unless current_user.admin
      flash[:danger] = 'Not an administrator.'
      redirect_to root_path
    end
  end
end
