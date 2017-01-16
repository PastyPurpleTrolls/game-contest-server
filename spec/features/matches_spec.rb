require 'rails_helper'

include ActionView::Helpers::DateHelper

describe "MatchesPages" do
  subject { page }

  let (:user) { FactoryGirl.create(:user) }
  let (:creator) { FactoryGirl.create(:contest_creator) }
  let (:contest) { FactoryGirl.create(:contest, user: creator) }
  let! (:player1) { FactoryGirl.create(:player, contest: contest, user: creator) }
  let! (:player2) { FactoryGirl.create(:player, contest: contest) }
  let! (:player3) { FactoryGirl.create(:player, contest: contest) }
  let! (:player4) { FactoryGirl.create(:player, contest: contest) }
  let! (:player5) { FactoryGirl.create(:player, contest: contest) }

  let (:now) { Time.current }
  let (:submit) { 'Challenge!' }
  let (:num_of_rounds) { 3 }
  let (:big_num_of_rounds) { 100 }

# CREATE MATCHES
  describe "create" do

    before do
      login creator
      visit new_contest_match_path(contest)
    end

    describe "invalid information" do
      describe "missing information" do
        it "should not create a match" do
          expect { click_button submit }.not_to change(Match, :count)
        end

        describe "after submission" do
          before { click_button submit }

          it { should have_alert(:danger) }
        end
      end # missing info

      illegal_dates = [{month: 'Feb', day: '30'},
        {month: 'Feb', day: '31'},
        {year: '2015', month: 'Feb', day: '29'},
        {month: 'Apr', day: '31'},
        {month: 'Jun', day: '31'},
        {month: 'Sep', day: '31'},
        {month: 'Nov', day: '31'}]
      illegal_dates.each do |date|
        describe "illegal date (#{date.to_s})" do
          before do
            select_illegal_datetime('Start', date)
	    check("#{player1.name} | #{player1.user.username}")
	    check("#{player2.name} | #{player2.user.username}")
	    check("#{player3.name} | #{player3.user.username}")
	    check("#{player4.name} | #{player4.user.username}")
	    select num_of_rounds, from: :match_num_rounds
            click_button submit
          end
          it { should have_alert(:danger) }
        end
      end # illegal date
      
      # Test that one of the current user's players are chosen.
      describe "didn't select a current user's player" do
        before do
	  select_datetime(now, 'Start')
          check("#{player2.name} | #{player2.user.username}")
          check("#{player3.name} | #{player3.user.username}")
          check("#{player4.name} | #{player4.user.username}")
          check("#{player5.name} | #{player5.user.username}")
	  select num_of_rounds, from: :match_num_rounds
	  click_button submit
	end
	
	it { should have_alert(:danger) }

      end # no current user's player	

      #Test that enough players are chosen.
      describe "didn't select enough players" do
        before do
          select_datetime(now, 'Start')
          check("#{player1.name} | #{player1.user.username}")
          check("#{player4.name} | #{player4.user.username}")
          select num_of_rounds, from: :match_num_rounds
	  click_button submit
        end

        it { should have_alert(:danger) }

      end # not enough players

      #Test that there aren't too many players chosen.
      describe "selected too many players" do
        before do
          select_datetime(now, 'Start')
          check("#{player1.name} | #{player1.user.username}")
          check("#{player2.name} | #{player2.user.username}")
          check("#{player3.name} | #{player3.user.username}")
          check("#{player4.name} | #{player4.user.username}")
          check("#{player5.name} | #{player5.user.username}")
          select num_of_rounds, from: :match_num_rounds
          click_button submit
        end

        it { should have_alert(:danger) }

      end # too many players

    end # invalid info

    describe "valid information" do

      describe "create a few matches" do
        before do
          select_datetime(now, 'Start')
          check("#{player1.name} | #{player1.user.username}")
          check("#{player2.name} | #{player2.user.username}")
          check("#{player3.name} | #{player3.user.username}")
          check("#{player4.name} | #{player4.user.username}")
	  select num_of_rounds, from: :match_num_rounds
        end

        it "should create 3 matches" do
	  #Change by count of 3 because num_of_rounds = 3.
	  pending("Shouldn't actually work in production.  Fundamentally flawed.")
          expect { click_button submit }.to change(Match, :count).by(3)
        end    
      end

      describe "create many matches" do
        before do
          select_datetime(now, 'Start')
          check("#{player1.name} | #{player1.user.username}")
          check("#{player2.name} | #{player2.user.username}")
          check("#{player3.name} | #{player3.user.username}")
          check("#{player4.name} | #{player4.user.username}")
          select big_num_of_rounds, from: :match_num_rounds
        end

        it "should create 100 matches" do
          #Change by count of 100 because big_num_of_rounds = 100.
	  pending("Fundamentally flawed test.  Should not actually work.")
          expect { click_button submit }.to change(Match, :count).by(100)
        end
      end

      describe 'redirects properly', type: :request do
        before do
          login creator, avoid_capybara: true
          post contest_matches_path(contest),
            match: { manager_id: 1, earliest_start: now.strftime("%F %T"),
            player_ids: {player1.id => "1", player2.id => "1", player3.id => "1", player4.id => "1"},
	          num_rounds: 3 }
        end
        specify { expect(response).to redirect_to(match_path( contest.matches.first.slug )) }
	      specify { expect(assigns(:match).manager).to eq(contest) }	

      end # redirects

      describe "after submission" do

	before do
          select_datetime(now, 'Start')
          check("#{player1.name} | #{player1.user.username}")
          check("#{player2.name} | #{player2.user.username}")
          check("#{player3.name} | #{player3.user.username}")
          check("#{player4.name} | #{player4.user.username}")
          select num_of_rounds, from: :match_num_rounds
	end

        before { click_button submit }

	      it { should have_content('Match Information') }
        it { should have_alert(:success, text: 'Match created.') }
        it { should have_content(contest.name) }

	#The following tests were removed when successful redirect was changed from
	#the newly created match page to the contest page.

	#it { should have_content('Match Information') }
        #it { should have_content(/less than a minute|1 minute/) }
        #it { should have_content('waiting') }
        #it { should have_link(contest.name,
        #                      href: contest_path(contest)) }
        #it { should have_content("4 Players") }
        #it { should have_link(player1.name,
        #                      href: player_path(player1)) }
        #it { should have_link(player2.name,
        #                      href: player_path(player2)) }
        #it { should have_link(player3.name,
        #                      href: player_path(player3)) }
        #it { should have_link(player4.name,
        #                      href: player_path(player4)) }
        #it { should_not have_link(player5.name,
        #                      href: player_path(player5)) }

      end

    end #valid

  end #create

# DESTROY MATCHES
  describe "destroy", type: :request do
    let!(:challenge_match) { FactoryGirl.create(:challenge_match) }
    let!(:tournament_match) { FactoryGirl.create(:tournament_match) }

    describe "logged in as normal user" do
      before do
        login user, avoid_capybara: true
      end

      it "should not let normal user destroy a challenge match" do
        expect { delete match_path(challenge_match) }.not_to change(Match, :count)
      end

      it "should not let normal user destroy a tournament match" do
        expect { delete match_path(tournament_match) }.not_to change(Match, :count)
      end

    end # logged in as normal user

    describe "logged in as contest creator" do
      before do
        login creator, avoid_capybara: true
      end

      describe "challenge match redirects properly" do
        before { delete match_path(challenge_match) }
        specify { expect(response).to redirect_to(contest_path(challenge_match.manager)) }
      end

      describe "tournament match redirects properly" do
        before { delete match_path(tournament_match) }
        specify { expect(response).to redirect_to(tournament_path(tournament_match.manager)) }
      end

      it "produces a delete message" do
        delete match_path(challenge_match)
        get response.location
        response.body.should have_alert(:success)
      end

      it "removes a match from the system (challenge match)" do
        expect { delete match_path(challenge_match) }.to change(Match, :count).by(-1)
      end

			it "removes all rounds associated with the match from the system (challenge round)" do
				expect { delete match_path(challenge_match) }.to change(Round, :count).by(-4)
			end

      it "removes a match from the system (tournament match)" do
        expect { delete match_path(tournament_match) }.to change(Match, :count).by(-1)
      end
			
			it "removes all player matches associated with the match from the system" do
				expect { delete match_path(tournament_match) }.to change(PlayerMatch, :count).by(-4)
			end

			it "removes all rounds associated with the match from the system (tournament round)" do
				expect { delete match_path(tournament_match) }.to change(Round, :count).by(-4)
			end

			it "removes all player rounds associated with the match from the system" do
				expect { delete match_path(tournament_match) }.to change(PlayerRound, :count).by(-16)
			end

    end # logged in as contest creator

  end # destroy

#SHOW A TOURNAMENT MATCH
  describe "show (tournament match)" do
    let (:match) { FactoryGirl.create(:tournament_match) }

    before { visit match_path(match) }

    it { should have_content(match.status.capitalize) }
    it { should have_content(distance_of_time_in_words_to_now(match.earliest_start)) }
    it { should have_content(match.manager.name) }
    it { should have_content(match.manager.referee.players_per_game) }

    describe "completed" do
      before do
        match.status = 'completed'
        match.completion = 1.day.ago
        match.save

        visit match_path(match)
      end

      it { should have_content(distance_of_time_in_words_to_now(match.completion)) }
    end

    describe "associated players (descending scores)" do
      let!(:players) { [] }

      before do
        match.player_matches.each_with_index do |pm, i|
         # pm.score = 10 - i
          pm.save
        end

        visit match_path(match)
      end

     it "should link to all players" do
        match.players.each_with_index do |p, i|
          should have_link(p.name, player_path(p))
        end
      end
    end

    describe "associated players (ascending scores)" do
      before do
        match.player_matches.each_with_index do |pm, i|
          pm.save
        end

        visit match_path(match)
      end

     it "should link to all players" do
        match.players.each_with_index do |p, i|
          should have_link(p.name, player_path(p))
        end
      end
    end
  end

#SHOW A CHALLENGE MATCH
  describe "show (challenge match)" do
    let (:match) { FactoryGirl.create(:challenge_match) }
    let (:user ) { match.players.first.user }
    before do
       user.password = "password"
       login user
       visit match_path(match) 
       end
       

    it { should have_content(match.status.capitalize) }
    it { should have_content(distance_of_time_in_words_to_now(match.earliest_start)) }
    it { should have_content(match.manager.name) }
    it { should have_content(match.manager.referee.players_per_game) }
  end

# SHOW ALL TOURNAMENT MATCHES
  describe "show all tournament matches" do
    let (:tournament) { FactoryGirl.create(:tournament) }
		let! (:t2) { FactoryGirl.create(:tournament) } 

    before do
      5.times { FactoryGirl.create(:tournament_match, manager: tournament) }
      5.times { FactoryGirl.create(:tournament_match, manager: t2) }

      visit tournament_matches_path(tournament)
    end
    
    it "lists all the tournament matches for a single tournament in the system" do
      Match.where(manager: tournament).each do |m|
        should have_selector('li', text: m.id)
        should have_link(m.id, match_path(m))
      end
    end

		it "should not list matches of other tournaments" do 
      Match.where(manager: t2).each do |m|
        should_not have_selector('li', text: m.id)
        should_not have_link(m.id, match_path(m))
      end
		end
  end

# SHOW ALL CONTEST MATCHES
  describe "show all contest matches" do
=begin
    let (:contest) { FactoryGirl.create(:contest) }
    let (:user) { FactoryGirl.create(:user) }
    let (:player) { FactoryGirl.create(:player, user: user, contest: contest) }
    before do
      login user 
      FactoryGirl.create_list(:challenge_match, 5, manager: contest, player: player) 
      visit contest_matches_path(contest)
    end

    it "lists all the challenge matches for a contest in the system" do
      Match.where(manager: contest).each do |m|
        should have_selector('li', text: m.id)
        should have_link(m.id, match_path(m))
      end
		end
=end
		# 'let!' is necessary because, without it, the Match's index page is visited before the challenge matches are created
		let! (:challenge_matches_player1_is_in) { FactoryGirl.create_list(:challenge_match, 5, manager: contest, player: player1) }
    let! (:challenge_matches_player1_is_not_in) { FactoryGirl.create_list(:challenge_match, 5, manager: contest, player: player2) }
    before do
      login creator
      visit contest_matches_path(contest)
    end

    it "should list all the challenge matches for a contest in which the user has a player participating" do
      challenge_matches_player1_is_in.each do |m|
        should have_selector('li', text: m.id)
        should have_link(m.id, match_path(m))
      end
    end

		it "should not list challenge matches (within the same contest) in which the user doesn\'t have a player participating" do
      challenge_matches_player1_is_not_in.each do |m|
        should_not have_selector('li', text: m.id)
        should_not have_link(m.id, match_path(m))
      end

		end
  end

end


