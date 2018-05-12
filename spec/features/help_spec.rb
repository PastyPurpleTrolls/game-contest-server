require 'rails_helper'

describe 'HelpPages' do
  let (:student) {FactoryBot.create(:user)}
  let (:creator) {FactoryBot.create(:contest_creator)}
  let (:admin) {FactoryBot.create(:admin, contest_creator: true)}

  subject {page}

  describe 'students' do
    before do
      login student
      visit help_path
    end

    it 'can see general help pages' do
      should have_content 'General'
      should have_link('Terminology', href: help_terminology_path)
    end

    it 'have access to the terminology help page' do
      visit help_terminology_path
      should have_content 'Terminology'
    end

    it 'cannot see administrator help pages' do
      should_not have_content 'Administrator Role'
      should_not have_link('Capabilities', href: help_admin_capabilities_path)
      should_not have_link('Changing User Roles', href: help_changing_user_roles_path)
      should_not have_link('Deleting Users', href: help_deleting_users_path)
      should_not have_link('Manually Running a Match', href: help_manually_running_match_path)
      should_not have_link('Entity Relationship Diagram', href: help_erd_path)
    end

    it 'do not have access to the administrator capabilities help page' do
      visit help_admin_capabilities_path
      should have_content 'You must be an administrator'
      should have_current_path help_path
    end

    it 'do not have access to the changing user roles help page' do
      visit help_changing_user_roles_path
      should have_content 'You must be an administrator'
      should have_current_path help_path
    end

    it 'do not have access to the deleting users help page' do
      visit help_deleting_users_path
      should have_content 'You must be an administrator'
      should have_current_path help_path
    end

    it 'do not have access to the manually running a match help page' do
      visit help_manually_running_match_path
      should have_content 'You must be an administrator'
      should have_current_path help_path
    end

    it 'do not have access to the ERD help page' do
      visit help_erd_path
      should have_content 'You must be an administrator'
      should have_current_path help_path
    end

    it 'cannot see contest creator help pages' do
      should_not have_content 'Contest Creator Role'
      should_not have_link('Capabilities', href: help_contest_creator_capabilities_path)
      should_not have_link('Creating and Running a Contest', href: help_creating_contest_path)
      should_not have_link('Writing a Referee', href: help_writing_referee_path)
      should_not have_link('Writing a Replay Plugin', href: help_writing_replay_plugin_path)
    end

    it 'do not have access to the contest creator capabilities help page' do
      visit help_contest_creator_capabilities_path
      should have_content 'You must be a contest creator'
      should have_current_path help_path
    end

    it 'do not have access to the creating and running a contest help page' do
      visit help_creating_contest_path
      should have_content 'You must be a contest creator'
      should have_current_path help_path
    end

    it 'do not have access to the writing a referee help page' do
      visit help_writing_referee_path
      should have_content 'You must be a contest creator'
      should have_current_path help_path
    end

    it 'do not have access to the writing a replay plugin help page' do
      visit help_writing_replay_plugin_path
      should have_content 'You must be a contest creator'
      should have_current_path help_path
    end

    it 'can see student help pages' do
      should have_content 'Student Role'
      should have_link('Capabilities', href: help_student_capabilities_path)
      should have_link('Upload Players to a Contest', href: help_upload_players_to_contest_path)
      should have_link('Challenge Other Players', href: help_challenge_other_players_path)
      should have_link('View Tournament Results', href: help_view_tournament_results_path)
      should have_link('View Challenge Match Results', href: help_view_challenge_match_results_path)
    end

    it 'have access to the student capabilities help page' do
      visit help_student_capabilities_path
      should have_current_path help_student_capabilities_path
    end

    it 'have access to the upload players to a contest help page' do
      visit help_upload_players_to_contest_path
      should have_current_path help_upload_players_to_contest_path
    end

    it 'have access to the challenge other players help page' do
      visit help_challenge_other_players_path
      should have_current_path help_challenge_other_players_path
    end

    it 'have access to the view tournament results help page' do
      visit help_view_tournament_results_path
      should have_current_path help_view_tournament_results_path
    end

    it 'have access to the view challenge match results help page' do
      visit help_view_challenge_match_results_path
      should have_current_path help_view_challenge_match_results_path
    end
  end

  describe 'contest creators' do
    before do
      login creator
      visit help_path
    end

    it 'can see general help pages' do
      should have_content 'General'
      should have_link('Terminology', href: help_terminology_path)
    end

    it 'have access to the terminology help page' do
      visit help_terminology_path
      should have_content 'Terminology'
    end

    it 'cannot see administrator help pages' do
      should_not have_content 'Administrator Role'
      should_not have_link('Changing User Roles', href: help_changing_user_roles_path)
      should_not have_link('Deleting Users', href: help_deleting_users_path)
      should_not have_link('Manually Running a Match', href: help_manually_running_match_path)
      should_not have_link('Entity Relationship Diagram', href: help_erd_path)
    end

    it 'do not have access to the administrator capabilities help page' do
      visit help_admin_capabilities_path
      should have_content 'You must be an administrator'
      should have_current_path help_path
    end

    it 'do not have access to the changing user roles help page' do
      visit help_changing_user_roles_path
      should have_content 'You must be an administrator'
      should have_current_path help_path
    end

    it 'do not have access to the deleting users help page' do
      visit help_deleting_users_path
      should have_content 'You must be an administrator'
      should have_current_path help_path
    end

    it 'do not have access to the manually running a match help page' do
      visit help_manually_running_match_path
      should have_content 'You must be an administrator'
      should have_current_path help_path
    end

    it 'do not have access to the ERD help page' do
      visit help_erd_path
      should have_content 'You must be an administrator'
      should have_current_path help_path
    end

    it 'can see contest creator help pages' do
      should have_content 'Contest Creator Role'
      should have_link('Capabilities', href: help_contest_creator_capabilities_path)
      should have_link('Creating and Running a Contest', href: help_creating_contest_path)
      should have_link('Writing a Referee', href: help_writing_referee_path)
      should have_link('Writing a Replay Plugin', href: help_writing_replay_plugin_path)
    end

    it 'have access to the contest creator capabilities help page' do
      visit help_contest_creator_capabilities_path
      should have_current_path help_contest_creator_capabilities_path
    end

    it 'have access to the creating and running a contest help page' do
      visit help_creating_contest_path
      should have_current_path help_creating_contest_path
    end

    it 'have access to the writing a referee help page' do
      visit help_writing_referee_path
      should have_current_path help_writing_referee_path
    end

    it 'have access to the writing a replay plugin help page' do
      visit help_writing_replay_plugin_path
      should have_current_path help_writing_replay_plugin_path
    end

    it 'can see student help pages' do
      should have_content 'Student Role'
      should have_link('Capabilities', href: help_student_capabilities_path)
      should have_link('Upload Players to a Contest', href: help_upload_players_to_contest_path)
      should have_link('Challenge Other Players', href: help_challenge_other_players_path)
      should have_link('View Tournament Results', href: help_view_tournament_results_path)
      should have_link('View Challenge Match Results', href: help_view_challenge_match_results_path)
    end

    it 'have access to the student capabilities help page' do
      visit help_student_capabilities_path
      should have_current_path help_student_capabilities_path
    end

    it 'have access to the upload players to a contest help page' do
      visit help_upload_players_to_contest_path
      should have_current_path help_upload_players_to_contest_path
    end

    it 'have access to the challenge other players help page' do
      visit help_challenge_other_players_path
      should have_current_path help_challenge_other_players_path
    end

    it 'have access to the view tournament results help page' do
      visit help_view_tournament_results_path
      should have_current_path help_view_tournament_results_path
    end

    it 'have access to the view challenge match results help page' do
      visit help_view_challenge_match_results_path
      should have_current_path help_view_challenge_match_results_path
    end
  end

  describe 'administrators' do
    before do
      login admin
      visit help_path
    end

    it 'can see general help pages' do
      should have_content 'General'
      should have_link('Terminology', href: help_terminology_path)
    end

    it 'have access to the terminology help page' do
      visit help_terminology_path
      should have_content 'Terminology'
    end

    it 'can see administrator help pages' do
      should have_content 'Administrator Role'
      should have_link('Capabilities', href: help_admin_capabilities_path)
      should have_link('Changing User Roles', href: help_changing_user_roles_path)
      should have_link('Deleting Users', href: help_deleting_users_path)
      should have_link('Manually Running a Match', href: help_manually_running_match_path)
      should have_link('Entity Relationship Diagram', href: help_erd_path)
    end

    it 'have access to the administrator capabilities help page' do
      visit help_admin_capabilities_path
      should have_current_path help_admin_capabilities_path
    end

    it 'have access to the changing user roles help page' do
      visit help_changing_user_roles_path
      should have_current_path help_changing_user_roles_path
    end

    it 'have access to the deleting users help page' do
      visit help_deleting_users_path
      should have_current_path help_deleting_users_path
    end

    it 'have access to the manually running a match help page' do
      visit help_manually_running_match_path
      should have_current_path help_manually_running_match_path
    end

    it 'have access to the ERD help page' do
      visit help_erd_path
      should have_current_path help_erd_path
    end

    it 'can see contest creator help pages' do
      should have_content 'Contest Creator Role'
      should have_link('Capabilities', href: help_contest_creator_capabilities_path)
      should have_link('Creating and Running a Contest', href: help_creating_contest_path)
      should have_link('Writing a Referee', href: help_writing_referee_path)
      should have_link('Writing a Replay Plugin', href: help_writing_replay_plugin_path)
    end

    it 'have access to the contest creator capabilities help page' do
      visit help_contest_creator_capabilities_path
      should have_current_path help_contest_creator_capabilities_path
    end

    it 'have access to the creating and running a contest help page' do
      visit help_creating_contest_path
      should have_current_path help_creating_contest_path
    end

    it 'have access to the writing a referee help page' do
      visit help_writing_referee_path
      should have_current_path help_writing_referee_path
    end

    it 'have access to the writing a replay plugin help page' do
      visit help_writing_replay_plugin_path
      should have_current_path help_writing_replay_plugin_path
    end

    it 'can see student help pages' do
      should have_content 'Student Role'
      should have_link('Capabilities', href: help_student_capabilities_path)
      should have_link('Upload Players to a Contest', href: help_upload_players_to_contest_path)
      should have_link('Challenge Other Players', href: help_challenge_other_players_path)
      should have_link('View Tournament Results', href: help_view_tournament_results_path)
      should have_link('View Challenge Match Results', href: help_view_challenge_match_results_path)
    end

    it 'have access to the student capabilities help page' do
      visit help_student_capabilities_path
      should have_current_path help_student_capabilities_path
    end

    it 'have access to the upload players to a contest help page' do
      visit help_upload_players_to_contest_path
      should have_current_path help_upload_players_to_contest_path
    end

    it 'have access to the challenge other players help page' do
      visit help_challenge_other_players_path
      should have_current_path help_challenge_other_players_path
    end

    it 'have access to the view tournament results help page' do
      visit help_view_tournament_results_path
      should have_current_path help_view_tournament_results_path
    end

    it 'have access to the view challenge match results help page' do
      visit help_view_challenge_match_results_path
      should have_current_path help_view_challenge_match_results_path
    end
  end
end