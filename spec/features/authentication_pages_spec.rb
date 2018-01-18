require 'rails_helper'

describe "AuthenticationPages" do
  subject {page}
  describe "login page" do
    before {visit login_path}

    it {should have_selector("h2", text: "Login")}

    describe "with invalid account" do
      before {click_button 'Log In'}

      it {should have_alert(:danger, text: 'Invalid')}

      describe "visiting another page" do
        before {click_link 'Contests'}

        it {should_not have_alert(:danger)}
      end
    end

    describe "with valid account" do
      let(:user) {FactoryBot.create(:user)}

      before do
        fill_in 'Username', with: user.username
        fill_in 'Password', with: user.password
        click_button 'Log In'
      end

      it "has the correct content on the navbar" do
        should have_selector(:xpath, "//li/a", text: 'Account')
        should have_link('Profile', href: user_path(user))
        should have_link('Settings', href: edit_user_path(user))
        should have_link('Log Out', href: logout_path)
        should_not have_button('Log In')
        should_not have_button('Sign Up')
      end

      describe "followed by logout" do
        before {click_link 'Log Out'}

        it "has the correct content on the navbar" do
          should have_button('Log In')
          should have_button('Sign Up')
          should_not have_selector(:xpath, "//li/a", text: 'Account')
          should_not have_link('Log Out', href: logout_path)
          should_not have_link('Settings')
          should_not have_link('Profile')
        end
      end
    end
  end
end

describe "AuthorizationPages" do
  subject {page}

  let(:user) {FactoryBot.create(:user)}

  describe "non-authenticated users" do
    describe "for Users controller" do
      describe "edit action" do
        it_behaves_like "redirects to a login" do
          let (:path) {edit_user_path(user)}
          let (:method) {:patch}
          let (:http_path) {user_path(user)}
        end
      end

      describe "delete action" do
        it_behaves_like "redirects to a login", skip_browser: true do
          let (:user) {FactoryBot.create(:user)}
          let (:method) {:delete}
          let (:http_path) {user_path(user)}
        end
      end
    end

    describe "for Referees controller" do
      describe "new action" do
        it_behaves_like "redirects to a login" do
          let (:path) {new_referee_path}
          let (:method) {:post}
          let (:http_path) {referees_path}
        end
      end

      describe "edit action" do
        it_behaves_like "redirects to a login" do
          let (:referee) {FactoryBot.create(:referee)}
          let (:path) {edit_referee_path(referee)}
          let (:method) {:patch}
          let (:http_path) {referee_path(referee)}
        end
      end

      describe "delete action" do
        it_behaves_like "redirects to a login", skip_browser: true do
          let (:referee) {FactoryBot.create(:referee)}
          let (:method) {:delete}
          let (:http_path) {referee_path(referee)}
        end
      end
    end

    describe "for Contests controller" do
      describe "new action" do
        it_behaves_like "redirects to a login" do
          let (:path) {new_contest_path}
          let (:method) {:post}
          let (:http_path) {contests_path}
        end
      end

      describe "edit action" do
        it_behaves_like "redirects to a login" do
          let (:contest) {FactoryBot.create(:contest)}
          let (:path) {edit_contest_path(contest)}
          let (:method) {:patch}
          let (:http_path) {contest_path(contest)}
        end
      end

      describe "delete action" do
        it_behaves_like "redirects to a login", skip_browser: true do
          let (:contest) {FactoryBot.create(:contest)}
          let (:method) {:delete}
          let (:http_path) {contest_path(contest)}
        end
      end
    end

    describe "for Players controller" do
      describe "new action" do
        it_behaves_like "redirects to a login" do
          let (:contest) {FactoryBot.create(:contest)}
          let (:path) {new_contest_player_path(contest)}
          let (:method) {:post}
          let (:http_path) {contest_players_path(contest)}
        end
      end

      describe "edit action" do
        it_behaves_like "redirects to a login" do
          let (:player) {FactoryBot.create(:player)}
          let (:path) {edit_player_path(player)}
          let (:method) {:patch}
          let (:http_path) {player_path(player)}
        end
      end

      describe "delete action" do
        it_behaves_like "redirects to a login", skip_browser: true do
          let (:player) {FactoryBot.create(:player)}
          let (:method) {:delete}
          let (:http_path) {player_path(player)}
        end
      end
    end

    describe "for Matches controller" do
      describe "index action (with path 'contest_matches')" do
        it_behaves_like "redirects to a login", browser_only: true do
          let (:contest) {FactoryBot.create(:contest)}
          let (:path) {contest_matches_path(contest)}
        end
      end

      describe "show action (with a challenge match)" do
        it_behaves_like "redirects to a login", browser_only: true do
          let (:challenge_match) {FactoryBot.create(:challenge_match)}
          let (:path) {match_path(challenge_match)}
        end
      end
    end

    describe "for Rounds controller show action" do # written with an educated guess of what the path will be for rounds (but that route has not been generated yet)
      describe "(Rounds are of a challange match)" do
        it_behaves_like "redirects to a login", browser_only: true do
          let (:challenge_round) {FactoryBot.create(:challenge_round)}
          let (:path) {round_path(challenge_round)}
        end
      end

      describe "(Rounds are of a tournament match)" do
        it_behaves_like "redirects to a login", browser_only: true do
          let (:tournament_round) {FactoryBot.create(:tournament_round)}
          let (:path) {round_path(tournament_round)}
        end
      end
    end
  end

  describe "authenticated users" do
    describe "for Users controller" do
      it_behaves_like "redirects to root" do
        let (:login_user) {user}
        let (:path) {new_user_path}
        let (:signature) {'Sign Up'}
        let (:error_type) {:warning}
        let (:method) {:post}
        let (:http_path) {users_path}
      end

      it_behaves_like "redirects to root" do
        let (:login_user) {user}
        let (:path) {login_path}
        let (:signature) {'Log In'}
        let (:error_type) {:warning}
        let (:method) {:post}
        let (:http_path) {users_path}
      end
    end
  end

  describe "authenticated, but wrong user" do
    describe "for Users controller" do
      it_behaves_like "redirects to root" do
        let (:other_user) {FactoryBot.create(:user)}
        let (:login_user) {user}
        let (:path) {edit_user_path(other_user)}
        let (:signature) {'Edit user'}
        let (:error_type) {:danger}
        let (:method) {:patch}
        let (:http_path) {user_path(other_user)}
      end
    end

    describe "for Referees controller" do
      it_behaves_like "redirects to root" do
        let (:login_user) {user}
        let (:path) {new_referee_path}
        let (:signature) {'Create Referee'}
        let (:error_type) {:danger}
        let (:method) {:post}
        let (:http_path) {referees_path}
      end

      it_behaves_like "redirects to root" do
        let (:referee) {FactoryBot.create(:referee)}
        let (:login_user) {user}
        let (:path) {edit_referee_path(referee)}
        let (:signature) {'Edit Referee'}
        let (:error_type) {:danger}
        let (:method) {:patch}
        let (:http_path) {referee_path(referee)}
      end

      it_behaves_like "redirects to root", skip_browser: true do
        let (:referee) {FactoryBot.create(:referee)}
        let (:login_user) {user}
        let (:error_type) {:danger}
        let (:method) {:delete}
        let (:http_path) {referee_path(referee)}
      end
    end

    describe "for Contests controller" do
      it_behaves_like "redirects to root" do
        let (:login_user) {user}
        let (:path) {new_contest_path}
        let (:signature) {'Create Contest'}
        let (:error_type) {:danger}
        let (:method) {:post}
        let (:http_path) {contests_path}
      end

      it_behaves_like "redirects to root" do
        let (:contest) {FactoryBot.create(:contest)}
        let (:login_user) {user}
        let (:path) {edit_contest_path(contest)}
        let (:signature) {'Edit Contest'}
        let (:error_type) {:danger}
        let (:method) {:patch}
        let (:http_path) {contest_path(contest)}
      end

      it_behaves_like "redirects to root", skip_browser: true do
        let (:contest) {FactoryBot.create(:contest)}
        let (:login_user) {user}
        let (:error_type) {:danger}
        let (:method) {:delete}
        let (:http_path) {contest_path(contest)}
      end
    end

    describe "for Players controller" do
      it_behaves_like "redirects to root" do
        let (:player) {FactoryBot.create(:player)}
        let (:login_user) {user}
        let (:path) {edit_player_path(player)}
        let (:signature) {'Edit Player'}
        let (:error_type) {:danger}
        let (:method) {:patch}
        let (:http_path) {player_path(player)}
      end

      it_behaves_like "redirects to root", skip_browser: true do
        let (:player) {FactoryBot.create(:player)}
        let (:login_user) {user}
        let (:error_type) {:danger}
        let (:method) {:delete}
        let (:http_path) {player_path(player)}
      end
    end

    describe "for Matches controller" do
      let (:challenge_match) {FactoryBot.create(:challenge_match)}
      let (:other_user) {FactoryBot.create(:user)}
      let (:login_user) {other_user}
      describe "index action (with a challenge match)" do
        it_behaves_like "redirects to root", browser_only: true do
          let (:signature) {'Matches for'}
          let (:error_type) {:danger}
          let (:path) {contest_matches_path(challenge_match.manager)}
        end
      end

      describe "show action (with a challenge match)" do
        it_behaves_like "redirects to root", browser_only: true do
          let (:signature) {'Match Information'}
          let (:error_type) {:danger}
          let (:path) {match_path(challenge_match)}
        end
      end
    end

    describe "for Rounds controller show action" do # written with an educated guess of what the path will be for rounds (but that route has not been generated yet)
      let! (:other_user) {FactoryBot.create(:user)}
      let (:login_user) {other_user}
      let (:signature) {'Round Information'}
      let (:error_type) {:danger}

      describe "(Rounds are of a challange match)" do
        it_behaves_like "redirects to root", browser_only: true do
          let (:challenge_round) {FactoryBot.create(:challenge_round)}
          let (:path) {round_path(challenge_round)}
        end
      end

      describe "(Rounds are of a tournament match)" do
        it_behaves_like "redirects to root", browser_only: true do
          let (:tournament_round) {FactoryBot.create(:tournament_round)}
          let (:path) {round_path(tournament_round)}
        end
      end
    end

  end

  describe "authenticated, but non-admin user" do
    describe "for Users controller" do
      it_behaves_like "redirects to root", skip_browser: true do
        let (:other_user) {FactoryBot.create(:user)}
        let (:login_user) {user}
        let (:error_type) {:danger}
        let (:method) {:delete}
        let (:http_path) {user_path(other_user)}
      end
    end
  end

  describe "authenticated admin user" do
    let(:admin) {FactoryBot.create(:admin)}

    describe "delete action (self)" do
      it_behaves_like "redirects to root", skip_browser: true do
        let (:login_user) {admin}
        let (:error_type) {:danger}
        let (:method) {:delete}
        let (:http_path) {user_path(admin)}
      end
    end
  end
end
