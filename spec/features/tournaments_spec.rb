require 'rails_helper'

include ActionView::Helpers::DateHelper

describe 'TournamentsPages' do
  let (:creator) { FactoryBot.create(:contest_creator) }
  let!(:referee) { FactoryBot.create(:referee) }
  let (:contest) { FactoryBot.create(:contest, user: creator) }
  let!(:player1) { FactoryBot.create(:player, contest: contest) }
  let!(:player2) { FactoryBot.create(:player, contest: contest) }

  let (:name) { 'Test Tournament' }
  let (:now) { mins_multiple_of_5(1.hour.from_now) }
  let (:tournament_type) { 'Round Robin' }

  let (:edit_name) { 'Some random edited name' }
  let (:edit_time) { now + 1.day }
  let (:edit_tournament_type) { 'Single Elimination' }

  subject { page }

  describe 'create' do
    let(:submit) {'Create Tournament'}

    before do
      login creator
      visit new_contest_tournament_path(contest)
    end

    it { should have_selector("h2", text: "Add Tournament") }             

    describe 'invalid information' do
      describe 'missing information' do
        it 'should not create a tournament' do
          expect { click_button submit }.not_to change(Tournament, :count)
        end

        describe "after submission" do
          before { click_button submit }

          it { should have_alert(:danger) }
        end
      end # missing info

      illegal_dates.each do |date|
        describe "illegal date (#{date.to_s})" do
          before do
            fill_in 'Name', with: name
            select_illegal_datetime('Start', date)
            select tournament_type, from: 'Tournament Type'
            click_button submit
          end

          it { pending; should have_alert(:danger) }
        end
      end # illegal date

    end # invalid info

    describe 'valid information', js: true do

      before do
        fill_in 'Name', with: name
        select_datetime(now, 'Start')
        select tournament_type, from: 'Tournament Type'
        select("#{player1.name} (#{player1.user.username})")
        click_button("btnRight")
	      select 1, from: 'Rounds per Match'

      end

      it "should create a tournament" do
        #pending "concurrent access by database"
        expect do 
          click_button submit 
          page.find('.alert')
        end.to change(Tournament, :count).by(1)
      end

      describe 'redirects properly', type: :request, js: false do
        before do
          login creator, avoid_capybara: true
          post contest_tournaments_path(contest),
            params: { tournament: { name: name,
              start: now.strftime("%F %T"),
              tournament_type: tournament_type.downcase,
              players: [player1],
	      rounds_per_match: 1
          } }
        end

        specify { expect(response).to redirect_to(tournament_path(assigns(:tournament))) }
      end # redirects

      describe "after submission" do
        let (:tournament) { Tournament.find_by(name: name) }

        before do 
          click_button submit
          page.find('.alert')
        end

        specify { expect(tournament.contest.user).to eq(creator) }

        it { should have_alert(:success, text: 'Tournament created') }
        it { should have_content(/About 1 Hour/) }
        it { should have_content(tournament.name) }
        it { should have_content(tournament.status.capitalize) }
        it { should have_link(tournament.contest.name,
                              href: contest_path(tournament.contest)) }
        it { should have_content("Player") }
        it { should have_link(player1.name,
                              href: player_path(player1)) }
        it { should_not have_link(player2.name,
                              href: player_path(player2)) }

      end
    end # valid info
  end # create

  describe "edit" do
    #let (:tournament) { FactoryBot.create(:tournament, contest: contest, tournament_type: tournament_type.downcase) }
    let (:tournament) { FactoryBot.create(:tournament, contest: contest, start: now) }
    let!(:orig_name) { tournament.name }
    let (:submit) { 'Update Tournament' }

    before do
      tournament.players << player1
      tournament.save
      login creator
      visit edit_tournament_path(tournament)
    end

    it { should have_selector("h2", text: "Edit Tournament") }
    it { should have_field("Name", with: tournament.name) }    
    it { expect_datetime_select(tournament.start, 'Start') }
    it { should have_select('Tournament Type',
                            options: %w[ Round\ Robin   Single\ Elimination  Multiplayer\ Game  King\ Of\ The\ Hill ],
                            selected: tournament_type) }

    it { should have_select("rightValues", options: ["#{player1.name} (#{player1.user.username})"]) } 
    it { should have_select("leftValues", options: ["#{player2.name} (#{player2.user.username})"]) }     

    describe "with invalid information" do
      before do
        select_datetime(now, 'Start')
        fill_in 'Name', with: ''
        select tournament_type, from: 'Tournament Type'
      end

      describe "does not change data" do
        before { click_button submit }

        specify { expect(tournament.reload.name).not_to eq('') }
        specify { expect(tournament.reload.name).to eq(orig_name) }
      end

      it "does not add a new tournament to the system" do
        expect { click_button submit }.not_to change(Tournament, :count)
      end

      it "produces an error message" do
        click_button submit
        should have_alert(:danger)
      end
    end # invalid info

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
            patch tournament_path(tournament), params: { tournament: { status: new_status  } }
          end

          specify { expect(tournament.reload.status).not_to eq(new_status) }
        end # change status to #{new_status}
      end # do loop


    end # forbidden attributes

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

        it { should have_alert(:success) }
        specify { expect(tournament.reload.name).to eq(edit_name) }
        specify { expect_same_minute(tournament.reload.start, edit_time) }
        specify { expect(tournament.reload.tournament_type).to eq(edit_tournament_type.downcase) }

        it { should_not have_link(player1.name,
                                  href: player_path(player1)) }
        it { should have_link(player2.name,
                              href: player_path(player2)) }
      end # changes the data

      describe "redirects properly", type: :request, js: false do
        before do
          login creator, avoid_capybara: true
          patch tournament_path(tournament), params: { tournament: { start: now.strftime("%F %T"),
            name: edit_name,
            tournament_type: edit_tournament_type.downcase
          } }
        end

        specify { expect(response).to redirect_to(tournament_path(tournament)) }
      end # redirects properly

      it "does not add a new tournament to the system" do
        expect do 
          click_button submit
          page.find('.alert')          
        end.not_to change(Tournament, :count)
      end

    end # valid information
  end # edit

  describe "destroy", type: :request do
    let!(:tournament) { FactoryBot.create(:tournament, contest: contest) }

    before do
      login creator, avoid_capybara: true
    end

    describe "redirects properly" do
      before { delete tournament_path(tournament) }

      specify { expect(response).to redirect_to(contest_path(tournament.contest)) }
    end

    it "produces a delete message" do
      delete tournament_path(tournament)
      get response.location
      response.body.should have_alert(:success)
    end

    it "removes a tournament from the system" do
      expect { delete tournament_path(tournament) }.to change(Tournament, :count).by(-1)
    end
  end # destroy

  describe 'show' do
    let!(:tournament) { FactoryBot.create(:tournament) }

    before { visit tournament_path(tournament) }

    # Tournament attributes
    it { should have_selector("h2", text: "Tournament") }                       
    it { should have_content(tournament.name) }
    it { should have_content(tournament.status.capitalize) }
    it { should have_content(distance_of_time_in_words_to_now(tournament.start).split.map { |i| i.capitalize }.join(' ')) }
    it { should have_content(tournament.tournament_type.split.map { |i| i.capitalize }.join(' ')) }

=begin
    # Edit
    it { should have_link("Edit", edit_tournament_path(tournament)) }
=end

    # Contest stuff
    it { should have_content(tournament.contest.user.username) }
    it { should have_link(tournament.contest.user.username, href: user_path(tournament.contest.user)) }

    it { should have_content(tournament.contest.name) }
    it { should have_link(tournament.contest.name, href: contest_path(tournament.contest)) }

    it "lists all the players in the tournament" do
      PlayerTournament.where(tournament: tournament).each do |pt|
        p = pt.player
        should have_selector('li', text: p.name)
        should have_link(t.name, href: player_path(p))
      end
    end


  end # show

  describe 'search with pagination' do
    let(:submit) { 'Search' }

    before do
      20.times { FactoryBot.create(:tournament, contest: contest) }
      visit contest_path(contest)
      fill_in 'search', with: 'Tournament'
      click_button submit
    end

    it { should have_content("Tournaments (1-10 of #{Tournament.count})") }
    it { should have_link('2') }
    it { should_not have_link('3') }
  end

  describe 'search without pagination' do
    let(:submit) { 'Search' }
    let!(:tournament2) { FactoryBot.create(:tournament, contest: contest) }

    before do
      visit contest_path(contest)
      fill_in 'tournament_search', with: 'Player'
      click_button submit
    end

    it 'should return results' do
      should have_content("Tournaments (1-2 of #{Tournament.count})")
      should have_link(tournament.name, href: tournament_path(tournament))
      should have_link(tournament2.name, href: tournament_path(tournament2))
    end
  end

  describe 'search_error'do
    let(:submit) { 'Search' }

    before do
      visit contest_path(contest)
      fill_in 'search', with: 'junk input'
      click_button submit
    end

    it { should have_content("Tournaments (0 of #{Tournament.count})") }
    it { should_not have_link('2') }
    it { should have_content('No players found') }
  end

  describe "show all" do
    before do
      5.times { FactoryBot.create(:tournament, contest: contest) }

      visit contest_path(contest)
    end

    it { should have_selector("h2", text: "Contest") }

    it "lists all the tournaments for a contest in the system" do
      Tournament.where(contest: contest).each do |tournament|
        should have_link(tournament.name, href: tournament_path(tournament))
      end
    end
  end # show all
end
