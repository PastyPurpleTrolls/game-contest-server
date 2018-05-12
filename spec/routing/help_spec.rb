require 'rails_helper'

describe 'Help' do
  describe 'available routes' do
    specify { expect(get(help_terminology_path)).to be_routable }
    specify { expect(get(help_admin_capabilities_path)).to be_routable }
    specify { expect(get(help_deleting_users_path)).to be_routable }
    specify { expect(get(help_changing_user_roles_path)).to be_routable }
    specify { expect(get(help_erd_path)).to be_routable }
    specify { expect(get(help_manually_running_match_path)).to be_routable }
    specify { expect(get(help_contest_creator_capabilities_path)).to be_routable }
    specify { expect(get(help_creating_contest_path)).to be_routable }
    specify { expect(get(help_writing_referee_path)).to be_routable }
    specify { expect(get(help_writing_replay_plugin_path)).to be_routable }
    specify { expect(get(help_student_capabilities_path)).to be_routable }
    specify { expect(get(help_upload_players_to_contest_path)).to be_routable }
    specify { expect(get(help_challenge_other_players_path)).to be_routable }
    specify { expect(get(help_view_tournament_results_path)).to be_routable }
    specify { expect(get(help_view_challenge_match_results_path)).to be_routable }
  end
end