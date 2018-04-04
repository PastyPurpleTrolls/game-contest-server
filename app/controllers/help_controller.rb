class HelpController < ApplicationController
  include ApplicationHelper

  before_action :ensure_user_logged_in

  before_action :check_contest_creator,
                only: [:contest_creator_capabilities, :creating_contest, :writing_referee, :writing_replay_plugin]

  before_action :check_admin,
                only: [:admin_capabilities, :deleting_users, :changing_user_roles, :erd, :manually_running_match]

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

  def check_contest_creator
    unless current_user.contest_creator
      flash[:danger] = 'You must be a contest creator to view this page'
      redirect_to help_path
    end
  end

  def check_admin
    unless current_user.admin
      flash[:danger] = 'You must be an administrator to view this page'
      redirect_to help_path
    end
  end
end
