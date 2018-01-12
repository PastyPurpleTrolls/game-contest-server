require 'rails_helper'

feature "HomePage" do

  subject {page}

  describe "the navigation bar" do
    let (:admin) {FactoryBot.create(:admin)}
    let (:creator) {FactoryBot.create(:contest_creator)}
    let (:user) {FactoryBot.create(:user)}

    before {visit root_path}

    it {should have_selector("h2", text: "Home")}
    it {should have_selector('.navbar')}

    describe "as anonymous" do
      it "has the proper links" do
        within ".navbar" do
          should have_link('Game Contest Server', href: root_path)
          should have_link('Contests', href: contests_path)
          should have_button('Log In')
          should have_button('Sign Up')
        end
      end
    end

    describe "as user" do
      before {login user}

      it "has the proper links" do
        within ".navbar" do
          should have_link('Game Contest Server', href: root_path)
          should have_link('Contests', href: contests_path)
          should have_content('Account')
        end
      end
    end

    describe "as contest_creator" do
      before {login creator}

      it "has the proper links" do
        within ".navbar" do
          should have_link('Game Contest Server', href: root_path)
          should have_link('Contests', href: contests_path)
          should have_link('Referees', href: referees_path)
          should have_content('Account')
        end
      end
    end

    describe "as admin" do
      before {login admin}

      it "has the proper links" do
        within ".navbar" do
          should have_link('Game Contest Server', href: root_path)
          should have_link('Users', href: users_path)
          should have_link('Contests', href: contests_path)
          should have_content('Account')
        end
      end
    end
  end

  describe "the home page" do
    describe "as anonymous" do
      before {visit root_path}

      it "has the correct content" do
        should have_content("Welcome to Taylor University's Game Contest Server!")

        should_not have_content("Add Player")
        should_not have_link('', href: new_contest_player_path("not-specified"))
        should_not have_content("Add Contest")
        should_not have_link('', href: new_contest_path)
        should_not have_content("Add Tournament")
        should_not have_link('', href: new_contest_tournament_path('not-specified'))
        should_not have_content("Challenge Players")
        should_not have_link('', href: new_contest_match_path("not-specified"))
        should_not have_content("View Contests")
        should_not have_content("View My Players")
      end
    end

    describe "as user" do
      let (:user) {FactoryBot.create(:user)}

      before do
        login user
        visit root_path
      end

      it "has the correct content" do
        should_not have_content("Welcome to Taylor University's Game Contest Server!")

        should have_content("Add Player")
        should have_link('', href: new_contest_player_path("not-specified"))
        should_not have_content("Add Contest")
        should_not have_link('', href: new_contest_path)
        should_not have_content("Add Tournament")
        should_not have_link('', href: new_contest_tournament_path('not-specified'))
        should have_content("Challenge Players")
        should have_link('', href: new_contest_match_path("not-specified"))
        should have_content("View Contests")
        should have_content("View My Players")
      end
    end

    describe "as creator" do
      let (:creator) {FactoryBot.create(:contest_creator)}

      before do
        login creator
        visit root_path
      end

      it "has the correct content" do
        should_not have_content("Welcome to Taylor University's Game Contest Server!")

        should have_content("Add Player")
        should have_link('', href: new_contest_player_path("not-specified"))
        should have_content("Add Contest")
        should have_link('', href: new_contest_path)
        should have_content("Add Tournament")
        should have_link('', href: new_contest_tournament_path('not-specified'))
        should have_content("Challenge Players")
        should have_link('', href: new_contest_match_path("not-specified"))
        should have_content("View Contests")
        should have_content("View My Players")
      end
    end
  end
end
