require 'rails_helper'

describe "PlayersPages" do
  let (:user) { FactoryBot.create(:user) }
  let (:contest) { FactoryBot.create(:contest) }
  let (:player) { FactoryBot.create(:player, user: user, contest: contest) }
  let (:description) { 'Test Player Description' }
  let (:name) { 'Test Player' }
  let (:file_location) { Rails.root.join('spec', 'files', 'player.test') }
  let (:server_location) { Rails.root.join('code', 'players', 'test').to_s }

  subject { page }

  describe "create" do
    let (:submit) { 'Create Player' }

    before do
      login user
      visit new_contest_player_path(contest)
# hack to get submit working!
attach_file('Player File', file_location)
    end

    it { should have_selector("h2", text: "Add Player") }                 

    describe "invalid information" do
      describe "missing information" do
        it "should not create a player" do
          expect { click_button submit }.not_to change(Player, :count)
        end

        describe "after submission" do
          before { click_button submit }

          it { should have_alert(:danger) }
        end
      end
    end

    describe "valid information" do
      before do
        fill_in 'Name', with: name
        fill_in 'Description', with: description
        check('Allow others to compete against this player')
        uncheck('Allow others to download this player')
        attach_file('Player File', file_location)
      end

      it "should create a player" do
        expect { click_button submit }.to change(Player, :count).by(1)
      end

      describe "redirects properly", type: :request do
        before do
          login user, avoid_capybara: true
          post contest_players_path(contest),
            params: { player: { name: name,
              description: description,
              downloadable: false,
              playable: true,
              upload: fixture_file_upload(file_location) } }
        end

        specify { expect(response).to redirect_to(player_path(assigns(:player))) }
      end

      describe "after submission" do
        let (:player) { Player.find_by(contest: contest, name: name) }

        before { click_button submit }

        specify { expect(player.user).to eq(user) }
        specify { expect(player.contest).to eq(contest) }

        it { should have_alert(:success, text: 'Player created') }
        it { should have_content(name) }
        it { should have_content(description) }
        #it { should have_content(file_contents) }
        it { should have_content('can be challenged') }
        it { should have_content('cannot be downloaded') }
        it { should have_link(player.contest.name,
                              href: contest_path(player.contest) ) }
        it { should have_link(player.user.username,
                              href: user_path(player.user) ) }
      end
    end
  end

  describe "edit" do
    let (:player) { FactoryBot.create(:player, user: user) }
    let!(:orig_name) { player.name }
    let (:submit) { 'Update Player' }

    before do
      login user
      visit edit_player_path(player)
# hack to get submit working!
attach_file('Player File', file_location)
    end

    it { should have_selector("h2", text: "Edit Player") }                 
    it { should have_field('Name', with: player.name) }
    it { should have_field('Description', with: player.description) }
    it { should have_unchecked_field('download') }
    it { should_not have_checked_field('download') }
    it { should have_checked_field('compete') }
    it { should_not have_unchecked_field('compete') }

    describe "with invalid information" do
      before do
        fill_in 'Name', with: ''
        fill_in 'Description', with: description
      end

      describe "does not change data" do
        before { click_button submit }

        specify { expect(player.reload.name).not_to eq('') }
        specify { expect(player.reload.name).to eq(orig_name) }
      end

      it "does not add a new player to the system" do
        expect { click_button submit }.not_to change(Player, :count)
      end

      it "produces an error message" do
        click_button submit
        should have_alert(:danger)
      end
    end

    describe "with forbidden attributes", type: :request do
      let (:bad_path) { Rails.root.join('code',
                                        'players',
                                        'test').to_s }
      before do
        login user, avoid_capybara: true
        patch player_path(player), params: { player: { file_location: bad_path } }
      end

      specify { expect(player.reload.file_location).not_to eq(bad_path) }
    end

    describe "with valid information" do
      before do
        fill_in 'Name', with: name
        fill_in 'Description', with: description
        attach_file('Player File', file_location)
      end

      describe "changes the data" do
        before { click_button submit }

        it { should have_alert(:success) }
        specify { expect(player.reload.name).to eq(name) }
        specify { expect(player.reload.description).to eq(description) }

        it "stores the contents of the file correctly" do
          expect_same_contents(player.reload.file_location, file_location)
        end
      end

      describe "redirects properly", type: :request do
        before do
          login user, avoid_capybara: true
          patch player_path(player), params: { player: { name: name,
            description: description,
            playable: true,
            downloadable: false,
            upload: fixture_file_upload(file_location) } }
        end

        specify { expect(response).to redirect_to(player_path(player)) }
      end

      it "does not add a new player to the system" do
        expect { click_button submit }.not_to change(Player, :count)
      end
    end
  end

  describe "destroy", type: :request do
    let!(:player) { FactoryBot.create(:player, user: user) }
		let!(:player2) { FactoryBot.create(:player, user: user) }
		let!(:match) { FactoryBot.create(:match) }
		let!(:player_match) { FactoryBot.create(:player_match, player: player2, match: match) }

    before do
      login user, avoid_capybara: true
    end

    it "removes the player from the file system" do
      expect do
        delete player_path(player)
      end.to change{ Dir.entries(server_location).size }.by(-1)

      expect(File.exists?(player.file_location)).to be_falsey
    end

    describe "redirects properly" do
      before { delete player_path(player) }

      specify { expect(response).to redirect_to(contest_path(player.contest)) }
    end

    it "produces a delete message" do
      delete player_path(player)
      get response.location
      response.body.should have_alert(:success)
    end

    it "removes a player from the system" do
      expect { delete player_path(player) }.to change(Player, :count).by(-1)
    end

#		after do
#			puts player_match.player_id
#		end

		it "does not remove a player from the system that is in a match" do
			expect { delete player_path(player2) }.to change(Player, :count).by(0)
		end

  end

  describe "show" do
    let (:player) { FactoryBot.create(:player) }

    before { visit player_path(player) }

    it { should have_selector("h2", text: "Player") }                 
    it { should have_content(player.name) }
    it { should have_content(player.description) }
    it { should have_content('This player can be challenged') }
    it { should_not have_content('This player can be downloaded') }
    it { should have_content(player.contest.name) }
    it { should have_link(player.contest.name, href: contest_path(player.contest)) }
    it { should have_content(player.user.username) }
    it { should have_link(player.user.username, href: user_path(player.user)) }

    describe "show match" do
      let!(:player_match) do
	match = FactoryBot.create(:tournament_match, player: player)
	PlayerMatch.where(match: match, player: player).first
      end

      before { visit player_path(player) }

      it { should have_header(text: 'Match') }
      it { should have_content(player_match.result) }
      it { should have_selector("form[action='#{match_path(player_match.match)}']") }
    end

    describe "more complete match history" do
      before do
        7.times { FactoryBot.create(:winning_match, player: player) }
        4.times { FactoryBot.create(:losing_match, player: player) }

        visit player_path(player)
      end

      it { should have_header(text: 'Matches') }
      it { should have_content('Win', count: 7) }
      #Should only have 3 losses displayed because the 4th is on the next page.
      it { should have_content('Loss', count: 3) }
      it { should have_content('Record: 7-4') }
    end

    describe "undefeated history" do
      before do
        5.times { FactoryBot.create(:winning_match, player: player) }

        visit player_path(player)
      end

      it { should have_content('Win', count: 5) }
      it { should_not have_content('Loss') }
      it { should have_content('Record: 5-0') }
    end

    describe "win-loss history" do
      before do
        8.times { FactoryBot.create(:losing_match, player: player) }

        visit player_path(player)
      end

      it { should_not have_content('Win') }
      it { should have_content('Loss', count: 8) }
      it { should have_content('Record: 0-8') }
    end
  end

  describe 'search with pagination' do
    let(:submit) { 'Search' }

    before do
      20.times { FactoryBot.create(:player, contest: contest) }
      visit contest_path(contest)
      fill_in 'search', with: 'Player'
      click_button submit
    end

    it 'displays correct amount of players and paginates correctly' do
      should have_content("Players (1-10 of #{Player.count})")
      should have_link('2')
      should_not have_link('3')
    end
  end

  describe 'search without pagination' do
    let(:submit) { 'Search' }
    let!(:player2) { FactoryBot.create(:player, contest: contest) }

    before do
      visit contest_path(contest)
      fill_in 'player_search', with: 'Player'
      click_button submit
    end

    it 'should return results' do
      should have_content("Players (1-2 of #{Player.count})")
      should have_link(player.name, href: player_path(player))
      should have_link(player2.name, href: player_path(player2))
    end
  end

  describe 'search_error'do
    let(:submit) { 'Search' }

    before do
      visit contest_path(contest)
      fill_in 'search', with: 'junk input'
      click_button submit
    end

    it 'does not display any players' do
      should have_content("Players (0 of #{Player.count})")
      should_not have_link('2')
      should have_content('No players found')
    end
  end

  describe "show all" do
    before do
      5.times { FactoryBot.create(:player, contest: contest) }

      visit contest_path(contest)
    end

    it { should have_selector("h2", text: "Contest") }                 
    it "lists all the players for a contest in the system" do
      Player.where(contest: contest).each do |p|
        should have_link(p.name, href: player_path(p))
      end
    end
  end
end
