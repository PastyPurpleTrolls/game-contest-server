require 'rails_helper'

describe "RoundsPages" do

  subject {page}

  describe "show all rounds of a tournament match" do
    let (:tournament) {FactoryBot.create(:tournament)}
    let! (:tournament_match) {FactoryBot.create(:tournament_match, manager: tournament)}
    let (:tournament_match_2) {FactoryBot.create(:tournament_match, manager: tournament)}
    let (:contest) {FactoryBot.create(:contest)}
    let (:challenge_match) {FactoryBot.create(:challenge_match, manager: contest)}

    before do
      FactoryBot.create_list(:round, 5, match: tournament_match)
      FactoryBot.create_list(:round, 5, match: tournament_match_2)
      FactoryBot.create_list(:round, 5, match: challenge_match)
      visit match_path(tournament_match)
    end

    it {should have_selector("h2", text: "Match")}

    it "lists all the rounds for the match" do
      Round.where(match: tournament_match).each do |r|
        should have_selector('div', text: /Round #{r.id}$/)
        should have_link(r.id, href: round_path(r))
      end
    end

    it "should not list rounds of a different match" do
      Round.where(match: tournament_match_2).each do |r|
        should_not have_selector('li', text: /Round #{r.id}$/)
        should_not have_link(r.id, href: round_path(r))
      end
      Round.where(match: challenge_match).each do |r|
        should_not have_selector('li', text: /Round #{r.id}$/)
        should_not have_link(r.id, href: round_path(r))
      end
    end
  end

  describe "show all rounds of a contest match" do
    let (:tournament) {FactoryBot.create(:tournament)}
    let (:tournament_match) {FactoryBot.create(:tournament_match, manager: tournament)}
    let (:contest) {FactoryBot.create(:contest)}
    let (:challenge_match) {FactoryBot.create(:challenge_match, manager: contest)}
    let (:challenge_match_2) {FactoryBot.create(:challenge_match, manager: contest)}

    before do
      FactoryBot.create_list(:round, 5, match: tournament_match)
      FactoryBot.create_list(:round, 5, match: challenge_match)
      FactoryBot.create_list(:round, 5, match: challenge_match_2)
      challenge_match.players.first.user.password = "password"
      login challenge_match.players.first.user
      visit match_path(challenge_match)
    end

    it {should have_selector("h2", text: "Match")}

    it "lists all the rounds for the match" do
      Round.where(match: challenge_match).each do |r|
        #should have_selector('li', text: 'Round '+ r.id.to_s)
        should have_selector('div', text: /Round #{r.id}$/)
        should have_link(r.id, href: round_path(r))
      end
    end

    it "should not list rounds of a different match" do
      Round.where(match: challenge_match_2).each do |r|
        should_not have_selector('li', text: /Round #{r.id}$/)
        should_not have_link(r.id, href: round_path(r))
      end
      Round.where(match: tournament_match).each do |r|
        should_not have_selector('li', text: /Round #{r.id}$/)
        should_not have_link(r.id, href: round_path(r))
      end
    end
  end
end
