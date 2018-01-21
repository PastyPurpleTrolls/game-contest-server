require 'rails_helper'

describe "PlayersPages" do
  let (:user) {FactoryBot.create(:user)}
  let (:contest) {FactoryBot.create(:contest)}
  let (:player) {FactoryBot.create(:player, user: user, contest: contest)}
  let (:description) {'Test Player Description'}
  let (:name) {'Test Player'}
  let (:file_location) {Rails.root.join('spec', 'files', 'player.test')}
  let (:server_location) {Rails.root.join('code', 'players', 'test').to_s}

  subject {page}

  describe "create" do
    let (:submit) {'Create Player'}

    before do
      login user
      visit new_contest_player_path(contest)
      attach_file('Player File', file_location) # hack to get submit working!
    end

    it {should have_current_path(new_contest_player_path(contest))}

    describe "invalid information" do
      describe "missing information" do
        it "should not create a player" do
          expect {click_button submit}.not_to change(Player, :count)
        end

        describe "after submission" do
          before {click_button submit}

          it {should have_alert(:danger)}
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
        expect {click_button submit}.to change(Player, :count).by(1)
      end

      describe "redirects properly", type: :request do
        before do
          login user, avoid_capybara: true
          post contest_players_path(contest),
               params: {player: {name: name,
                                 description: description,
                                 downloadable: false,
                                 playable: true,
                                 upload: fixture_file_upload(file_location)}}
        end

        specify {expect(response).to redirect_to(player_path(assigns(:player)))}
      end

      describe "after submission" do
        let (:player) {Player.find_by(contest: contest, name: name)}

        before {click_button submit}

        specify {expect(player.user).to eq(user)}
        specify {expect(player.contest).to eq(contest)}

        it "shows all player information" do
          should have_content(name)
          should have_content(description)
          should have_content('can be challenged')
          should have_content('cannot be downloaded')
          should have_link(player.contest.name,
                               href: contest_path(player.contest))
          should have_link(player.user.username,
                               href: user_path(player.user))
        end
      end
    end
  end

  describe "edit" do
    let (:player) {FactoryBot.create(:player, user: user)}
    let!(:orig_name) {player.name}
    let (:submit) {'Update Player'}

    before do
      login user
      visit edit_player_path(player)
      attach_file('Player File', file_location) # hack to get submit working!
    end

    it "shows all fields" do
      should have_field('Name', with: player.name)
      should have_field('Description', with: player.description)
      should have_unchecked_field('download')
      should_not have_checked_field('download')
      should have_checked_field('compete')
      should_not have_unchecked_field('compete')
    end

    describe "with invalid information" do
      before do
        fill_in 'Name', with: ''
        fill_in 'Description', with: description
      end

      describe "does not change data" do
        before {click_button submit}

        specify {expect(player.reload.name).not_to eq('')}
        specify {expect(player.reload.name).to eq(orig_name)}
      end

      it "does not add a new player to the system" do
        expect {click_button submit}.not_to change(Player, :count)
      end

      it "produces an error message" do
        click_button submit
        should have_alert(:danger)
      end
    end

    describe "with forbidden attributes", type: :request do
      let (:bad_path) {Rails.root.join('code',
                                       'players',
                                       'test').to_s}
      before do
        login user, avoid_capybara: true
        patch player_path(player), params: {player: {file_location: bad_path}}
      end

      specify {expect(player.reload.file_location).not_to eq(bad_path)}
    end

    describe "with valid information" do
      before do
        fill_in 'Name', with: name
        fill_in 'Description', with: description
        attach_file('Player File', file_location)
      end

      describe "changes the data" do
        before {click_button submit}

        specify {expect(player.reload.name).to eq(name)}
        specify {expect(player.reload.description).to eq(description)}

        it "stores the contents of the file correctly" do
          expect_same_contents(player.reload.file_location, file_location)
        end
      end

      describe "redirects properly", type: :request do
        before do
          login user, avoid_capybara: true
          patch player_path(player), params: {player: {name: name,
                                                       description: description,
                                                       playable: true,
                                                       downloadable: false,
                                                       upload: fixture_file_upload(file_location)}}
        end

        specify {expect(response).to redirect_to(player_path(player))}
      end

      it "does not add a new player to the system" do
        expect {click_button submit}.not_to change(Player, :count)
      end
    end
  end

  describe "destroy", type: :request do
    let!(:player) {FactoryBot.create(:player, user: user)}
    let!(:player2) {FactoryBot.create(:player, user: user)}
    let!(:match) {FactoryBot.create(:match)}
    let!(:player_match) {FactoryBot.create(:player_match, player: player2, match: match)}

    before do
      login user, avoid_capybara: true
    end

    it "removes the player from the file system" do
      expect do
        delete player_path(player)
      end.to change {Dir.entries(server_location).size}.by(-1)

      expect(File.exists?(player.file_location)).to be_falsey
    end

    describe "redirects properly" do
      before {delete player_path(player)}

      specify {expect(response).to redirect_to(contest_path(player.contest))}
    end

    it "produces a delete message" do
      delete player_path(player)
      get response.location
      response.body.should have_alert(:success)
    end

    it "removes a player from the system" do
      expect {delete player_path(player)}.to change(Player, :count).by(-1)
    end

    it "does not remove a player from the system that is in a match" do
      expect {delete player_path(player2)}.to change(Player, :count).by(0)
    end

  end

  describe "show" do
    let (:player) {FactoryBot.create(:player)}

    before {visit player_path(player)}

    it "shows all player information" do
      should have_content(player.name)
      should have_content(player.description)
      should have_content('This player can be challenged')
      should_not have_content('This player can be downloaded')
      should have_content(player.contest.name)
      should have_link(player.contest.name, href: contest_path(player.contest))
      should have_content(player.user.username)
      should have_link(player.user.username, href: user_path(player.user))
    end

    describe "show match" do
      let!(:player_match) do
        match = FactoryBot.create(:tournament_match, player: player)
        PlayerMatch.where(match: match, player: player).first
      end

      before {visit player_path(player)}

      it {should have_header(text: 'Match')}
      it {should have_content(player_match.result)}
      it {should have_selector("form[action='#{match_path(player_match.match)}']")}
    end

    describe "more complete match history" do
      before do
        FactoryBot.create_list(:winning_match, 7, player: player)
        FactoryBot.create_list(:losing_match, 4, player: player)

        visit player_path(player)
      end

      it {should have_header(text: 'Matches')}

      it "shows all match information" do
        should have_content('Win', count: 6)
        #Should only have 3 losses displayed because the 4th is on the next page.
        should have_content('Loss', count: 4)
        should have_content('Record: 7-4')
      end
    end

    describe "undefeated history" do
      before do
        FactoryBot.create_list(:winning_match, 5, player: player)

        visit player_path(player)
      end

      it "shows all match information" do
        should have_content('Win', count: 5)
        should_not have_content('Loss')
        should have_content('Record: 5-0')
      end
    end

    describe "win-loss history" do
      before do
        FactoryBot.create_list(:losing_match, 8, player: player)

        visit player_path(player)
      end

      it "shows all match information" do
        should_not have_content('Win')
        should have_content('Loss', count: 8)
        should have_content('Record: 0-8')
      end
    end
  end

  describe "pagination" do
    before do
      FactoryBot.create_list(:player, 25, contest: contest)
      visit contest_path(contest)
    end

    it {should have_content("#{contest.players.count} found (displaying 1-10)")}

    it 'displays properly' do
      should have_selector('div.pagination')
      within '#player_pagination' do
        should_not have_link('← Previous')
        should_not have_link('1')
        should have_link('2')
        should have_link('3')
        should_not have_link('4')
        should have_link('Next →')
      end
    end

    describe "last page" do
      before { click_link('3') }

      it 'displays properly' do
        should have_selector('div.pagination')
        within '#player_pagination' do
          should have_link('← Previous')
          should have_link('1')
          should have_link('2')
          should_not have_link('3')
          should_not have_link('4')
          should_not have_link('Next →')
        end
      end

      it 'properly shows records displaying' do
        should have_content("#{contest.players.count} found (displaying 21-25)")
      end
    end

    describe "changing pages" do
      before do
        FactoryBot.create_list(:tournament, 11, contest: contest)
        within '#player_pagination' do
          click_link('2')
        end
      end

      it "does not change tournaments page" do
        within '#tournament_pagination' do
          should have_link('2')
        end
      end
    end
  end

  describe 'search with pagination' do
    let(:submit) {'Search'}

    before do
      FactoryBot.create_list(:player, 20, contest: contest)
      visit contest_path(contest)
      fill_in 'player_search', with: 'Player'
      within '#player_form' do
        click_button submit
      end
    end

    it {should have_content("#{contest.players.count} found (displaying 1-10)")}

    it "paginates properly" do
      within '#player_pagination' do
        should have_link('2')
        should_not have_link('3')
      end
    end
  end

  describe 'search without pagination' do
    let(:submit) {'Search'}

    before do
      FactoryBot.create(:player, contest: contest, name: "searchtest")
      visit contest_path(contest)
      fill_in 'player_search', with: 'searchtest'
      within '#player_form' do
        click_button submit
      end
    end

    it 'should return results' do
      should have_link('searchtest')
      should have_content('1 found')
      should_not have_content('displaying')
      should_not have_css('#player_pagination')
    end
  end

  describe 'search error' do
    let(:submit) {'Search'}

    before do
      visit contest_path(contest)
      fill_in 'player_search', with: 'junk input'
      within '#player_form' do
        click_button submit
      end
    end

    it "paginates properly" do
      should_not have_css('#player_pagination')
    end

    it {should have_content('No players found')}
  end

  describe "show all" do
    before do
      FactoryBot.create_list(:player, 5, contest: contest)

      visit contest_path(contest)
    end

    it "lists all the players for a contest in the system" do
      Player.where(contest: contest).each do |p|
        should have_link(p.name, href: player_path(p))
      end
    end
  end
end
