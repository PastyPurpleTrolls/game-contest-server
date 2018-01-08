require 'rails_helper'

include ActionView::Helpers::DateHelper

describe "MatchesPages" do

  subject {page}

  let (:user) {FactoryBot.create(:user)}
  let (:creator) {FactoryBot.create(:contest_creator)}
  let (:contest) {FactoryBot.create(:contest, user: creator)}
  let (:contest2) {FactoryBot.create(:contest, user: creator)}
  let (:contest3) {FactoryBot.create(:contest, user: creator)}
  let! (:player1) {FactoryBot.create(:player, contest: contest, user: creator)}
  let! (:player2) {FactoryBot.create(:player, contest: contest)}
  let! (:player3) {FactoryBot.create(:player, contest: contest)}
  let! (:player4) {FactoryBot.create(:player, contest: contest)}
  let! (:player5) {FactoryBot.create(:player, contest: contest)}
  let! (:player6) {FactoryBot.create(:player, contest: contest2, user: creator)}
  let! (:player7) {FactoryBot.create(:player, contest: contest2)}
  let! (:player8) {FactoryBot.create(:unplayable_player, contest: contest, user: creator)}
  let! (:player9) {FactoryBot.create(:unplayable_player, contest: contest)}
  let! (:player10) {FactoryBot.create(:unplayable_player, contest: contest2, user: creator)}
  let! (:player11) {FactoryBot.create(:unplayable_player, contest: contest2)}

  let (:now) {1.hour.from_now}
  let (:submit) {'Challenge!'}
  let (:num_of_rounds) {3}
  let (:big_num_of_rounds) {100}

  describe "create" do
    before do
      login creator
      visit new_contest_match_path(contest)
    end

    it {should have_selector("h2", text: "Challenge Match")}

    describe "list of available players" do
      it "should list all playable players in contest" do
        should have_selector("option", text: "#{player1.name} (#{player1.user.username})")
        should have_selector("option", text: "#{player2.name} (#{player2.user.username})")
        should have_selector("option", text: "#{player3.name} (#{player3.user.username})")
        should have_selector("option", text: "#{player4.name} (#{player4.user.username})")
        should have_selector("option", text: "#{player5.name} (#{player5.user.username})")
      end

      it "should not list any players in another contest" do
        should_not have_selector("option", text: "#{player6.name} (#{player6.user.username})")
        should_not have_selector("option", text: "#{player7.name} (#{player7.user.username})")
        should_not have_selector("option", text: "#{player10.name} (#{player10.user.username})")
        should_not have_selector("option", text: "#{player11.name} (#{player11.user.username})")
      end

      it "should not list other users' unplayable players" do
        should_not have_selector("option", text: "#{player9.name} (#{player10.user.username})")
        should_not have_selector("option", text: "#{player11.name} (#{player11.user.username})")
      end

      it "should list all current user's players in contest" do
        should have_selector("option", text: "#{player1.name} (#{player1.user.username})")
        should have_selector("option", text: "#{player8.name} (#{player8.user.username})")
      end

      describe "should show message if no available players" do
        before do
          visit new_contest_match_path(contest3)
        end

        it {should have_selector("p", text: "No challenge-able players yet.")}
      end
    end

    describe "invalid information" do
      describe "missing information" do
        it "should not create a match" do
          expect {click_button submit}.not_to change(Match, :count)
        end

        describe "after submission" do
          before {click_button submit}

          it {should have_alert(:danger)}
        end
      end

      illegal_dates.each do |date|
        describe "illegal date (#{date.to_s})", js: true do
          before do
            select_illegal_datetime('Start', date)
            select("#{player1.name} (#{player1.user.username})")
            select("#{player2.name} (#{player2.user.username})")
            select("#{player3.name} (#{player3.user.username})")
            select("#{player4.name} (#{player4.user.username})")
            click_button("btnRight")
            select num_of_rounds, from: :match_num_rounds
            click_button submit
          end

          it {should have_alert(:danger)}
        end
      end

      describe "didn't select a current user's player", js: true do
        before do
          select_datetime(now, 'Start')
          select("#{player2.name} (#{player2.user.username})")
          select("#{player3.name} (#{player3.user.username})")
          select("#{player4.name} (#{player4.user.username})")
          select("#{player5.name} (#{player5.user.username})")
          click_button("btnRight")
          select num_of_rounds, from: :match_num_rounds
          click_button submit
        end

        it {should have_alert(:danger)}
      end

      describe "didn't select enough players", js: true do
        before do
          select_datetime(now, 'Start')
          select("#{player1.name} (#{player1.user.username})")
          select("#{player4.name} (#{player4.user.username})")
          click_button("btnRight")
          select num_of_rounds, from: :match_num_rounds
          click_button submit
        end

        it {should have_alert(:danger)}
      end

      describe "selected too many players", js: true do
        before do
          select_datetime(now, 'Start')
          select("#{player1.name} (#{player1.user.username})")
          select("#{player2.name} (#{player2.user.username})")
          select("#{player3.name} (#{player3.user.username})")
          select("#{player4.name} (#{player4.user.username})")
          select("#{player5.name} (#{player5.user.username})")
          click_button("btnRight")
          select num_of_rounds, from: :match_num_rounds
          click_button submit
        end

        it {should have_alert(:danger)}
      end
    end

    describe "valid information" do
      describe 'redirects properly', type: :request do
        before do
          login creator, avoid_capybara: true
          post contest_matches_path(contest),
               params: {match: {earliest_start: now.strftime("%F %T"),
                                player_ids: [player1.id, player2.id, player3.id, player4.id],
                                num_rounds: 3}}
        end

        specify {expect(response).to redirect_to(match_path(contest.matches.first.slug))}
        specify {expect(assigns(:match).manager).to eq(contest)}
      end

      describe "after submission", js: true do

        before do
          select_datetime(now, 'Start')
          select("#{player1.name} (#{player1.user.username})")
          select("#{player2.name} (#{player2.user.username})")
          select("#{player3.name} (#{player3.user.username})")
          select("#{player4.name} (#{player4.user.username})")
          click_button("btnRight")
          select num_of_rounds, from: :match_num_rounds
          click_button(submit)
          page.find('.alert')
        end

        it {should have_content('Match')}
        it {should have_alert(:success, text: 'Match created.')}
        it {should have_content(contest.name)}
      end
    end
  end

  describe "destroy", type: :request do
    let!(:challenge_match) {FactoryBot.create(:challenge_match)}
    let!(:tournament_match) {FactoryBot.create(:tournament_match)}

    describe "logged in as normal user" do
      before do
        login user, avoid_capybara: true
      end

      it "should not let normal user destroy a challenge match" do
        expect {delete match_path(challenge_match)}.not_to change(Match, :count)
      end

      it "should not let normal user destroy a tournament match" do
        expect {delete match_path(tournament_match)}.not_to change(Match, :count)
      end
    end

    describe "logged in as contest creator" do
      before do
        login creator, avoid_capybara: true
      end

      describe "challenge match redirects properly" do
        before {delete match_path(challenge_match)}
        specify {expect(response).to redirect_to(contest_path(challenge_match.manager))}
      end

      describe "tournament match redirects properly" do
        before {delete match_path(tournament_match)}
        specify {expect(response).to redirect_to(tournament_path(tournament_match.manager))}
      end

      it "produces a delete message" do
        delete match_path(challenge_match)
        get response.location
        response.body.should have_alert(:success)
      end

      it "removes a match from the system (challenge match)" do
        expect {delete match_path(challenge_match)}.to change(Match, :count).by(-1)
      end

      it "removes all rounds associated with the match from the system (challenge round)" do
        expect {delete match_path(challenge_match)}.to change(Round, :count).by(-4)
      end

      it "removes a match from the system (tournament match)" do
        expect {delete match_path(tournament_match)}.to change(Match, :count).by(-1)
      end

      it "removes all player matches associated with the match from the system" do
        expect {delete match_path(tournament_match)}.to change(PlayerMatch, :count).by(-4)
      end

      it "removes all rounds associated with the match from the system (tournament round)" do
        expect {delete match_path(tournament_match)}.to change(Round, :count).by(-4)
      end

      it "removes all player rounds associated with the match from the system" do
        expect {delete match_path(tournament_match)}.to change(PlayerRound, :count).by(-16)
      end

    end
  end

  describe "show (tournament match)" do
    let (:match) {FactoryBot.create(:tournament_match)}

    before {visit match_path(match)}

    it {should have_selector("h2", text: "Match")}

    it "shows all match information" do
      should have_content(match.status.capitalize)
      should have_content(distance_of_time_in_words_to_now(match.earliest_start).split.map {|i| i.capitalize}.join(' '))
      should have_content(match.manager.name)
      should have_content(match.manager.referee.players_per_game)
    end

    describe "completed" do
      before do
        match.status = 'completed'
        match.completion = 1.day.ago
        match.save
        visit match_path(match)
      end

      it {should have_content(distance_of_time_in_words_to_now(match.completion).split.map {|i| i.capitalize}.join(' '))}
    end

    describe "associated players (descending scores)" do
      let!(:players) {[]}

      before do
        match.player_matches.each_with_index do |pm, i|
          pm.save
        end

        visit match_path(match)
      end

      it "should link to all players" do
        match.players.each_with_index do |p, i|
          should have_link(p.name, href: player_path(p))
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
          should have_link(p.name, href: player_path(p))
        end
      end
    end
  end

  describe "show (challenge match)" do
    let (:match) {FactoryBot.create(:challenge_match)}
    let (:user) {match.players.first.user}

    before do
      user.password = "password"
      login user
      visit match_path(match)
    end

    it {should have_selector("h2", text: "Match")}

    it "shows all match information" do
      should have_content(match.status.capitalize)
      should have_content(distance_of_time_in_words_to_now(match.earliest_start).split.map {|i| i.capitalize}.join(' '))
      should have_content(match.manager.name)
      should have_content(match.manager.referee.players_per_game)
    end
  end

  describe "show all tournament matches" do
    let (:tournament) {FactoryBot.create(:tournament)}
    let! (:t2) {FactoryBot.create(:tournament)}

    before do
      FactoryBot.create_list(:tournament_match, 5, manager: tournament)
      FactoryBot.create_list(:tournament_match, 5, manager: t2)

      visit tournament_matches_path(tournament)
    end

    it {should have_selector("h2", text: "Tournament")}

    it "lists all the tournament matches for a single tournament in the system" do
      Match.where(manager: tournament).each do |m|
        should have_selector('li', text: m.id)
        should have_link(m.id, href: match_path(m))
      end
    end

    it "should not list matches of other tournaments" do
      Match.where(manager: t2).each do |m|
        should_not have_selector('li', text: m.id)
        should_not have_link(m.id, href: match_path(m))
      end
    end
  end

  describe "show all contest matches" do
    let! (:challenge_matches_player1_is_in) {FactoryBot.create_list(:challenge_match, 5, manager: contest, player: player1)}
    let! (:challenge_matches_player1_is_not_in) {FactoryBot.create_list(:challenge_match, 5, manager: contest, player: player2)}

    before do
      login creator
      visit contest_matches_path(contest)
    end

    it {should have_selector("h2", text: "Tournament")}

    it "should list all the challenge matches for a contest in which the user has a player participating" do
      challenge_matches_player1_is_in.each do |m|
        should have_selector('li', text: m.id)
        should have_link(m.id, href: match_path(m))
      end
    end

    it "should not list challenge matches (within the same contest) in which the user doesn\'t have a player participating" do
      challenge_matches_player1_is_not_in.each do |m|
        should_not have_selector('li', text: m.id)
        should_not have_link(m.id, href: match_path(m))
      end
    end
  end
end


