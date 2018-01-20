# encoding: utf-8

require 'rails_helper'

describe "RefereePages" do
  let (:creator) {FactoryBot.create(:contest_creator)}
  let (:name) {'Test Referee'}
  let (:rules) {'http://example.com/path/to/rules'}
  let (:num_players) {'2'}
  let (:time_per_game) {'10'}
  let (:file_location) {Rails.root.join('spec', 'files', 'referee.test')}
  let (:server_location) {Rails.root.join('code', 'referees', 'test').to_s}
  let (:round_limit) {'5'}
  let (:round_limit_word) {'DEVIN'}
  let (:round_limit_negative) {'-5'}
  let (:round_limit_zero) {'0'}

  subject {page}

  describe "create" do
    let (:submit) {'Create Referee'}

    before do
      login creator
      visit new_referee_path
# hack to get submit to work with empty files!
      attach_file('Referee File', file_location)
      attach_file('Player-Include Files', file_location)
      attach_file('Replay Plugin', file_location)
      attach_file('Test Player', file_location)
    end

    it {should have_current_path(new_referee_path)}

    describe "invalid information" do
      describe "missing information" do
        it "should not create a referee" do
          expect {click_button submit}.not_to change(Referee, :count)
        end
      end

      describe "match limit must be a number" do
        before do
          fill_in 'Name', with: name
          fill_in 'Rules', with: rules
          fill_in 'Round Limit (Inclusive)', with: round_limit_word
          select num_players, from: 'Players'
          select time_per_game, from: 'Time per Game'
          attach_file('Referee File', file_location)
          attach_file('Player-Include Files', file_location)
          attach_file('Replay Plugin', file_location)
          click_button submit
        end

        it {should have_alert(:danger)}
      end

      describe "match limit must be positive" do
        before do
          fill_in 'Name', with: name
          fill_in 'Rules', with: rules
          fill_in 'Round Limit (Inclusive)', with: round_limit_negative
          select num_players, from: 'Players'
          select time_per_game, from: 'Time per Game'
          attach_file('Referee File', file_location)
          attach_file('Player-Include Files', file_location)
          attach_file('Replay Plugin', file_location)
          click_button submit
        end

        it {should have_alert(:danger)}
      end

      describe "match limit must be nonzero" do
        before do
          fill_in 'Name', with: name
          fill_in 'Rules', with: rules
          fill_in 'Round Limit (Inclusive)', with: round_limit_zero
          select num_players, from: 'Players'
          select time_per_game, from: 'Time per Game'
          attach_file('Referee File', file_location)
          attach_file('Player-Include Files', file_location)
          attach_file('Replay Plugin', file_location)
          click_button submit
        end

        it {should have_alert(:danger)}
      end

      describe "after submission" do
        before {click_button submit}

        it {should have_alert(:danger)}
      end
    end

    describe "valid information" do
      before do
        fill_in 'Name', with: name
        fill_in 'Rules', with: rules
        fill_in 'Round Limit (Inclusive)', with: round_limit
        select num_players, from: 'Players'
        select time_per_game, from: 'Time per Game'
        check 'referee_rounds_capable'
        attach_file('Referee File', file_location)
        attach_file('Player-Include Files', file_location)
        attach_file('Replay Plugin', file_location)
      end

      it "should create a referee" do
        expect {click_button submit}.to change(Referee, :count).by(1)
      end

      it "should add the code to the right directory" do
        expect do
          click_button submit
        end.to change {Dir.entries(server_location).size}.by(1)
      end

      describe "redirects properly", type: :request do
        before do
          login creator, avoid_capybara: true
          post referees_path, params: {referee: {name: name,
                                                 rules_url: rules,
                                                 round_limit: round_limit,
                                                 players_per_game: num_players,
                                                 time_per_game: time_per_game,
                                                 rounds_capable: true,
                                                 upload: fixture_file_upload(file_location)}}
        end

        specify {expect(response).to redirect_to(referee_path(assigns(:referee)))}
      end

      describe "after submission" do
        let (:referee) {Referee.find_by(name: name)}

        before {click_button submit}

        specify {expect(referee.user).to eq(creator)}

        it "shows all referee information" do
          should have_content(name)
          should have_content(round_limit)
          should have_link(rules)
          should have_content("This referee is capable of handling rounds")
          should have_content(num_players)
          should have_content(time_per_game)
        end

        it "stores the contents of the file correctly" do
          expect_same_contents(referee.file_location, file_location)
        end
      end
    end
  end

  describe "edit" do
    let (:referee) {FactoryBot.create(:referee, user: creator)}
    let!(:orig_name) {referee.name}
    let (:submit) {'Update Referee'}

    before do
      login creator
      visit edit_referee_path(referee)
# hack to get submit to work with empty files!
      attach_file('Referee File', file_location)
      attach_file('Player-Include Files', file_location)
      attach_file('Replay Plugin', file_location)
      attach_file('Test Player', file_location)
    end

    it "has the proper fields" do
      should have_field('Name', with: referee.name)
      should have_field('Rules', with: referee.rules_url)
      should have_select('Players', selected: referee.players_per_game.to_s)
    end

    describe "with invalid information" do
      before do
        fill_in 'Name', with: ''
        fill_in 'Rules', with: "#{rules}/updated"
        fill_in 'Round Limit (Inclusive)', with: round_limit
        select num_players, from: 'Players'
        select time_per_game, from: 'Time per Game'
        attach_file('Referee File', file_location)
        attach_file('Player-Include Files', file_location)
        attach_file('Replay Plugin', file_location)
      end

      describe "does not change data" do
        before {click_button submit}

        specify {expect(referee.reload.name).not_to eq('')}
        specify {expect(referee.reload.name).to eq(orig_name)}
      end

      it "does not add a new referee to the system" do
        expect {click_button submit}.not_to change(Referee, :count)
      end

      it "produces an error message" do
        click_button submit
        should have_alert(:danger)
      end
    end

    describe "with forbidden attributes", type: :request do
      let (:bad_path) {'/path/to/file'}

      before do
        login creator, avoid_capybara: true
        patch referee_path(referee), params: {referee: {file_location: bad_path}}
      end

      specify {expect(referee.reload.file_location).not_to eq(bad_path)}
    end

    describe "with valid information" do
      before do
        fill_in 'Name', with: name
        fill_in 'Rules', with: "#{rules}/updated"
        fill_in 'Round Limit (Inclusive)', with: round_limit
        select num_players, from: 'Players'
        select time_per_game, from: 'Time per Game'
        check 'referee_rounds_capable'
        attach_file('Referee File', file_location)
        attach_file('Player-Include Files', file_location)
        attach_file('Replay Plugin', file_location)
      end

      describe "changes the data" do
        before {click_button submit}

        specify {expect(referee.reload.name).to eq(name)}
        specify {expect(referee.reload.rules_url).to eq("#{rules}/updated")}
        specify {expect(referee.reload.round_limit.to_s).to eq(round_limit)}
        specify {expect(referee.reload.rounds_capable).to eq(true)}
        specify {expect(referee.reload.players_per_game).to eq(num_players.to_i)}
        specify {expect(referee.reload.time_per_game).to eq(time_per_game.to_i)}

        it "stores the contents of the file correctly" do
          expect_same_contents(referee.reload.file_location, file_location)
        end
      end

      describe "redirects properly", type: :request do
        before do
          login creator, avoid_capybara: true
          patch referee_path(referee), params: {referee: {name: name,
                                                          rules_url: "#{rules}/updated",
                                                          round_limit: round_limit,
                                                          players_per_game: num_players,
                                                          time_per_game: time_per_game,
                                                          referee_rounds_capable: true,
                                                          upload: fixture_file_upload(file_location)}}
        end

        specify {expect(response).to redirect_to(referee_path(referee))}
      end

      it "does not add a new referee to the system" do
        expect {click_button submit}.not_to change(Referee, :count)
      end

      it "should modify an existing referee" do
        expect do
          click_button submit
        end.not_to change {Dir.entries(server_location).size}
      end
    end
  end

  describe "destroy", type: :request do
    let!(:referee) {FactoryBot.create(:referee, user: creator)}

    before do
      login creator, avoid_capybara: true
    end

    it "removes the referee from the file system" do
      expect do
        delete referee_path(referee)
      end.to change {Dir.entries(server_location).size}.by(-1)

      expect(File.exists?(referee.file_location)).to be_falsey
    end

    describe "redirects properly" do
      before {delete referee_path(referee)}

      specify {expect(response).to redirect_to(referees_path)}
    end

    it "removes a referee from the system" do
      expect {delete referee_path(referee)}.to change(Referee, :count).by(-1)
    end
  end

  describe "pagination" do
    before do
      FactoryBot.create_list(:referee, 25)
      visit referees_path
    end

    it {should have_content("#{Referee.count} found (displaying 1-10)")}

    it 'displays properly' do
      should have_selector('div.pagination')
      should_not have_link('← Previous')
      should_not have_link('1')
      should have_link('2', href: "/referees?page=2")
      should have_link('3', href: "/referees?page=3")
      should_not have_link('4')
      should have_link('Next →', href: "/referees?page=2")
    end

    describe "last page" do
      before { click_link('3', href: "/referees?page=3") }

      it 'displays properly' do
        should have_selector('div.pagination')
        should have_link('← Previous', href: "/referees?page=2")
        should have_link('1', href: "/referees?page=1")
        should have_link('2', href: "/referees?page=2")
        should_not have_link('3')
        should_not have_link('4')
        should_not have_link('Next →')
      end

      it 'properly shows records displaying' do
        should have_content("#{Referee.count} found (displaying 21-25)")
      end
    end
  end

  describe 'search error' do
    let(:submit) {"Search"}

    before do
      visit referees_path
      fill_in 'search', with: 'junk input'
      click_button submit
    end

    it {should have_content("No referees found")}
    it {should_not have_link('2')}
  end


  describe 'search with pagination' do
    let(:submit) {"Search"}

    before do
      FactoryBot.create_list(:referee, 11)
      visit referees_path
      fill_in 'search', with: 'Referee'
      click_button submit
    end

    it {should have_content("#{Referee.count} found (displaying 1-10)")}

    it "paginates properly" do
      within '#referee_pagination' do
        should have_link('2')
        should_not have_link('3')
      end
    end
  end

  describe 'search without pagination' do
    let(:submit) {"Search"}

    before do
      FactoryBot.create(:referee, name: "searchtest")
      visit referees_path
      fill_in 'search', with: 'searchtest'
      click_button submit
    end

    it 'should return results' do
      should have_button('searchtest')
      should have_content('1 found')
      should_not have_content('displaying')
      should_not have_link('2')
    end
  end

  describe "show" do
    let (:referee) {FactoryBot.create(:referee)}

    before do
      FactoryBot.create_list(:contest, 5, referee: referee)
      visit referee_path(referee)
    end

    it "shows all referee information" do
      should have_content(referee.name)
      should have_link(referee.rules_url)
      should have_content(referee.round_limit)
      should have_content(referee.players_per_game.to_s)
      should have_content("This referee is not capable of handling rounds")
      should_not have_content(referee.file_location)
      should have_content(referee.user.username)
    end

    it "lists all the contests that use this referee" do
      Contest.all.each do |contest|
        should have_selector('div', text: contest.name)
        should have_link(contest.name, href: contest_path(contest))
      end
    end
  end

  describe "show all as any user" do
    before do
      FactoryBot.create_list(:referee, 5)
      visit referees_path
    end

    it {should have_current_path(referees_path)}

    it "does not have adding option" do
      should_not have_link('', href: new_referee_path)
    end

    it "lists all the referees in the system" do
      Referee.all.each do |ref|
        should have_selector('input.results-container')
        should have_selector("form[action='#{referee_path(ref)}']")

        within "form[action='#{referee_path(ref)}']" do
          should have_button(ref.name)
        end
      end
    end
  end

  describe "show all as contest_creator" do
    before do
      login creator
      visit referees_path
    end

    it {should have_current_path(referees_path)}

    it "has adding option" do
      should have_link('', href: new_referee_path)
    end
  end
end
