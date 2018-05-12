require 'rails_helper'

include ActionView::Helpers::DateHelper

describe 'TournamentsPages' do
  let (:creator) {FactoryBot.create(:contest_creator)}
  let!(:referee) {FactoryBot.create(:referee)}
  let (:contest) {FactoryBot.create(:contest, user: creator)}
  let!(:player1) {FactoryBot.create(:player, contest: contest)}
  let!(:player2) {FactoryBot.create(:player, contest: contest)}

  let (:name) {'Test Tournament'}
  let (:now) {mins_multiple_of_5(1.hour.from_now)}
  let (:tournament_type) {'Round Robin'}

  let (:edit_name) {'Some random edited name'}
  let (:edit_time) {now + 1.day}
  let (:edit_tournament_type) {'Single Elimination'}

  subject {page}

  describe 'create' do
    let(:submit) {'Create Tournament'}

    before do
      login creator
      visit new_contest_tournament_path(contest)
    end

    it {should have_current_path(new_contest_tournament_path(contest))}

    describe 'invalid information' do
      describe 'missing information' do
        it 'should not create a tournament' do
          expect {click_button submit}.not_to change(Tournament, :count)
        end

        describe "after submission" do
          before {click_button submit}

          it {should have_alert(:danger)}
        end
      end

      # illegal_dates.each do |date|
      #   describe "illegal date (#{date.to_s})" do
      #     before do
      #       fill_in 'Name', with: name
      #       select_illegal_datetime('Start', date)
      #       select tournament_type, from: 'Tournament Type'
      #       click_button submit
      #     end
      #
      #     it {should have_alert(:danger)}
      #   end
      # end
    end

    describe 'valid information', js: true do
      before do
        fill_in 'Name', with: name
        select_datetime(now, 'Start')
        select tournament_type, from: 'Tournament Type'
        select("#{player1.name} (#{player1.user.username})")
        click_button("btnRight")
        fill_in 'Rounds per Match', with: '1'
      end

      it "should create a tournament" do
        expect do
          click_button submit
          page.find('.alert')
        end.to change(Tournament, :count).by(1)
      end

      describe 'redirects properly', type: :request, js: false do
        before do
          login creator, avoid_capybara: true
          post contest_tournaments_path(contest),
               params: {tournament: {name: name,
                                     start: now.strftime("%F %T"),
                                     tournament_type: tournament_type.downcase,
                                     players: [player1],
                                     rounds_per_match: 1
               }}
        end

        specify {expect(response).to redirect_to(tournament_path(assigns(:tournament)))}
      end

      describe "after submission" do
        let (:tournament) {Tournament.find_by(name: name)}

        before do
          click_button submit
          page.find('.alert')
        end

        specify {expect(tournament.contest.user).to eq(creator)}

        it {should have_alert(:success, text: 'Tournament created')}

        it "shows all tournament information" do
          should have_content(/About 1 Hour/)
          should have_content(tournament.name)
          should have_content(tournament.status.capitalize)
          should have_link(tournament.contest.name,
                           href: contest_path(tournament.contest))
          should have_content("Player")
          should have_link(player1.name,
                           href: player_path(player1))
          should_not have_link(player2.name,
                               href: player_path(player2))
        end
      end
    end
  end

  describe "edit" do
    let (:tournament) {FactoryBot.create(:tournament, contest: contest, start: now)}
    let!(:orig_name) {tournament.name}
    let (:submit) {'Update Tournament'}

    before do
      tournament.players << player1
      tournament.save
      login creator
      visit edit_tournament_path(tournament)
    end

    it "shows the proper fields" do
      should have_field("Name", with: tournament.name)
      expect_datetime_select(tournament.start, 'Start')
      # should have_select('Tournament Type',
      #                    options: %w[ Round\ Robin Single\ Elimination Multiplayer\ Game King\ of\ the\ Hill ],
      #                    selected: tournament_type)

      should have_select("rightValues", options: ["#{player1.name} (#{player1.user.username})"])
      should have_select("leftValues", options: ["#{player2.name} (#{player2.user.username})"])
    end

    describe "with invalid information" do
      before do
        select_datetime(now, 'Start')
        fill_in 'Name', with: ''
        select tournament_type, from: 'Tournament Type'
      end

      describe "does not change data" do
        before {click_button submit}

        specify {expect(tournament.reload.name).not_to eq('')}
        specify {expect(tournament.reload.name).to eq(orig_name)}
      end

      it "does not add a new tournament to the system" do
        expect {click_button submit}.not_to change(Tournament, :count)
      end

      it "produces an error message" do
        click_button submit
        should have_alert(:danger)
      end
    end

    # Users should NOT be able to change the status of a
    # tournament. This is done by the backend and it uses it
    # to determine when to run tournaments.
    # The tournament model needs to be changed to reflect this.
    describe "with forbidden attributes", type: :request do
      %w[ waiting completed ].each do |new_status|
        describe "change status to #{new_status}" do
          before do
            tournament.status = 'started'
            tournament.save
            login creator, avoid_capybara: true
            patch tournament_path(tournament), params: {tournament: {status: new_status}}
          end

          specify {expect(tournament.reload.status).not_to eq(new_status)}
        end
      end
    end

    describe "with valid information", js: true do
      before do
        fill_in 'Name', with: edit_name
        select_datetime(edit_time, 'Start')
        select edit_tournament_type, from: 'Tournament Type'
        select("#{player1.name} (#{player1.user.username})")
        click_button("btnLeft")
        unselect("#{player1.name} (#{player1.user.username})")
        select("#{player2.name} (#{player2.user.username})")
        click_button("btnRight")
      end

      describe "changes the data" do
        before do
          click_button submit
          page.find('.alert')
        end

        it {should have_alert(:success)}
        specify {expect(tournament.reload.name).to eq(edit_name)}
        specify {expect_same_minute(tournament.reload.start, edit_time)}
        specify {expect(tournament.reload.tournament_type).to eq(edit_tournament_type.downcase)}

        it "shows the proper players" do
          should_not have_link(player1.name,
                               href: player_path(player1))
          should have_link(player2.name,
                           href: player_path(player2))
        end
      end

      describe "redirects properly", type: :request, js: false do
        before do
          login creator, avoid_capybara: true
          patch tournament_path(tournament), params: {tournament: {start: now.strftime("%F %T"),
                                                                   name: edit_name,
                                                                   tournament_type: edit_tournament_type.downcase
          }}
        end

        specify {expect(response).to redirect_to(tournament_path(tournament))}
      end

      it "does not add a new tournament to the system" do
        expect do
          click_button submit
          page.find('.alert')
        end.not_to change(Tournament, :count)
      end
    end
  end

  describe "destroy", type: :request do
    let!(:tournament) {FactoryBot.create(:tournament, contest: contest)}

    before do
      login creator, avoid_capybara: true
    end

    describe "redirects properly" do
      before {delete tournament_path(tournament)}

      specify {expect(response).to redirect_to(contest_path(tournament.contest))}
    end

    it "removes a tournament from the system" do
      expect {delete tournament_path(tournament)}.to change(Tournament, :count).by(-1)
    end
  end

  describe 'show' do
    let!(:tournament) {FactoryBot.create(:tournament)}

    before {visit tournament_path(tournament)}

    it "shows all tournament information" do
      should have_content(tournament.name)
      should have_content(tournament.status.capitalize)
      should have_content(distance_of_time_in_words_to_now(tournament.start).split.map {|i| i.capitalize}.join(' '))
      should have_content(tournament.tournament_type.split.map {|i| i.capitalize}.join(' '))
      should have_link(tournament.contest.user.username, href: user_path(tournament.contest.user))
      should have_link(tournament.contest.name, href: contest_path(tournament.contest))
    end

    it "lists all the players in the tournament" do
      PlayerTournament.where(tournament: tournament).each do |pt|
        p = pt.player
        should have_selector('li', text: p.name)
        should have_link(t.name, href: player_path(p))
      end
    end
  end

  describe "pagination" do
    before do
      FactoryBot.create_list(:tournament, 25, contest: contest)
      visit contest_path(contest)
    end

    it {should have_content("#{contest.tournaments.count} found (displaying 1-10)")}

    it 'displays properly' do
      should have_selector('div.pagination')
      within '#tournament_pagination' do
        should_not have_link('<')
        should_not have_link('1')
        should have_link('2')
        should have_link('3')
        should_not have_link('4')
        should have_link('>')
      end
    end

    describe "last page" do
      before {click_link('3', href: "/contests/#{contest.slug}?tournament_page=3")}

      it 'displays properly' do
        should have_selector('div.pagination')
        within '#tournament_pagination' do
          should have_link('<')
          should have_link('1')
          should have_link('2')
          should_not have_link('3')
          should_not have_link('4')
          should_not have_link('>')
        end
      end

      it 'properly shows records displaying' do
        should have_content("#{contest.tournaments.count} found (displaying 21-25)")
      end
    end

    describe "changing pages" do
      before do
        FactoryBot.create_list(:player, 11, contest: contest)
        within '#tournament_pagination' do
          click_link('2')
        end
      end

      it "does not change players page" do
        within '#player_pagination' do
          should have_link('2')
        end
      end
    end
  end

  describe 'search with pagination' do
    let(:submit) {'Search'}

    before do
      FactoryBot.create_list(:tournament, 20, contest: contest)
      visit contest_path(contest)
      fill_in 'tournament_search', with: 'Tournament'
      within '#tournament_form' do
        click_button submit
      end
    end

    it {should have_content("#{contest.tournaments.count} found (displaying 1-10)")}

    it "paginates properly" do
      within '#tournament_pagination' do
        should have_link('2')
        should_not have_link('3')
      end
    end
  end

  describe 'search without pagination' do
    let(:submit) {'Search'}

    before do
      FactoryBot.create(:tournament, contest: contest, name: "searchtest")
      visit contest_path(contest)
      fill_in 'tournament_search', with: 'searchtest'
      within '#tournament_form' do
        click_button submit
      end
    end

    it 'should return results' do
      should have_link('searchtest')
      should have_content('1 found')
      should_not have_content('displaying')
      should_not have_css('#tournament_pagination')
    end
  end

  describe 'search error' do
    let(:submit) {'Search'}

    before do
      visit contest_path(contest)
      fill_in 'tournament_search', with: 'junk input'
      within '#tournament_form' do
        click_button submit
      end
    end

    it "paginates properly" do
      should_not have_css('#tournament_pagination')
    end

    it {should have_content('No tournaments found')}
  end

  describe "show all" do
    before do
      FactoryBot.create_list(:tournament, 5, contest: contest)

      visit contest_path(contest)
    end

    it "lists all the tournaments for a contest in the system" do
      Tournament.where(contest: contest).each do |tournament|
        should have_link(tournament.name, href: tournament_path(tournament))
      end
    end
  end
end
