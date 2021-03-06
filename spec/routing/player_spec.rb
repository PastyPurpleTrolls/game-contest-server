require 'rails_helper'

describe Player do
    describe "available routes" do
        describe "within contest" do
            specify { expect(post(contest_players_path(1))).to be_routable }
            specify { expect(get(new_contest_player_path(1))).to be_routable }
        end

        describe "within tournament" do
            specify { expect(post(tournament_players_path(1))).to be_routable }
            specify { expect(get(new_tournament_player_path(1))).to be_routable }
        end

        describe "shallow routes" do
            specify { expect(get(edit_player_path(1))).to be_routable }
            specify { expect(get(player_path(1))).to be_routable }
            specify { expect(patch(player_path(1))).to be_routable }
            specify { expect(delete(player_path(1))).to be_routable }
        end

        describe "unavailable routes" do
            specify { expect(get('/players')).not_to be_routable }
            specify { expect(post('/players')).not_to be_routable }
            specify { expect(get('/players/new')).not_to route_to(action: 'new') }
        end
    end
end
