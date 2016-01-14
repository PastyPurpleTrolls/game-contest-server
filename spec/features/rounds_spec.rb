require 'rails_helper'

describe "RoundsPages" do

        subject { page }

	describe "show all rounds of a tournament match" do 
    let (:tournament) { FactoryGirl.create(:tournament) }
    let! (:tournament_match) { FactoryGirl.create(:tournament_match, manager: tournament) }
    let (:tournament_match_2) { FactoryGirl.create(:tournament_match, manager: tournament) }
    let (:contest) { FactoryGirl.create(:contest) }
		let (:challenge_match) { FactoryGirl.create(:challenge_match, manager: contest) }

    before do
			FactoryGirl.create_list(:round, 5, match: tournament_match)
			FactoryGirl.create_list(:round, 5, match: tournament_match_2)
			FactoryGirl.create_list(:round, 5, match: challenge_match)
			visit match_path(tournament_match)
		end

		it "lists all the rounds for the match" do
			Round.where(match: tournament_match).each do |r|
			should have_selector('li', text: /Round #{r.id}$/)	
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
    let (:tournament) { FactoryGirl.create(:tournament) }
    let (:tournament_match) { FactoryGirl.create(:tournament_match, manager: tournament) }
    let (:contest) { FactoryGirl.create(:contest) }
		let (:challenge_match) { FactoryGirl.create(:challenge_match, manager: contest) }
		let (:challenge_match_2) { FactoryGirl.create(:challenge_match, manager: contest) }

    before do
			FactoryGirl.create_list(:round, 5, match: tournament_match)
			FactoryGirl.create_list(:round, 5, match: challenge_match)
			FactoryGirl.create_list(:round, 5, match: challenge_match_2)
			visit match_path(challenge_match)
		end

		it "lists all the rounds for the match" do
				Round.where(match: challenge_match).each do |r|
				#should have_selector('li', text: 'Round '+ r.id.to_s)	
				should have_selector('li', text: /Round #{r.id}$/)	
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
