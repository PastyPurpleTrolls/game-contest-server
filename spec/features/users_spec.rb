require 'rails_helper'

describe "UsersPages" do
  subject {page}

  describe "Sign Up" do
    let(:submit) {'Create new account'}

    before {visit signup_path}

    it {should have_selector("h2", text: "Sign Up")}

    describe "passwords are not visible when typing" do
      it {should have_field 'user_password', type: 'password'}
      it {should have_field 'user_password_confirmation', type: 'password'}
    end

    describe "with invalid information" do
      it "does not add the user to the system" do
        expect {click_button submit}.not_to change(User, :count)
      end

      it "produces an error message" do
        click_button submit
        should have_alert(:danger)
      end
    end

    describe "with valid information" do
      before do
        fill_in 'Username', with: 'User Name'
        fill_in 'Email', with: 'user@example.com'
        fill_in 'Password', with: 'password'
        fill_in 'Confirmation', with: 'password'
      end

      it "allows the user to fill in user fields" do
        click_button submit
      end

      describe "redirects properly", type: :request do
        before do
          post users_path, params: {user: {username: 'User Name',
                                           email: 'user@example.com',
                                           password: 'password',
                                           password_confirmation: 'password'}}
        end

        specify {expect(response).to redirect_to(root_path)}
      end

      it "adds a new user to the system" do
        expect {click_button submit}.to change(User, :count).by(1)
      end

      describe "after creating the user" do
        before {click_button submit}

        it {should have_link('Log Out')}
        it {should_not have_link('Log In')}
        it {should have_alert(:success, text: 'Welcome')}
      end
    end
  end

  describe "Display Users" do
    describe "individually (not contest creator)" do
      let(:user) {FactoryBot.create(:user)}

      before do
        FactoryBot.create_list(:player, 5, user: user)
        visit user_path(user)
      end

      it {should have_selector("h2", text: "User")}

      it "displays all user information" do
        should have_content(user.username)
        should have_content(user.email)
        should_not have_content(user.password)
        should_not have_content(user.password_digest)
      end

      it {should have_header(text: 'My Players')}

      it "lists all the players for the user" do
        Player.all.each do |player|
          should have_selector('div', text: player.name)
          should have_link(player.name, href: player_path(player))
        end
      end

      it {should_not have_header(text: 'My Referees')}
      it {should_not have_header(text: 'My Contests')}
    end

    describe "individually (contest creator)" do
      let(:user) {FactoryBot.create(:contest_creator)}

      before do
        FactoryBot.create_list(:player, 5, user: user)
        FactoryBot.create_list(:referee, 5, user: user)
        FactoryBot.create_list(:contest, 5, user: user)
        visit user_path(user)
      end

      it {should have_selector("h2", text: "User")}

      it "displays all user information" do
        should have_content(user.username)
        should have_content(user.email)
        should_not have_content(user.password)
        should_not have_content(user.password_digest)
      end

      it {should have_header(text: 'My Players')}

      it "lists all the players for the user" do
        user.players.each do |player|
          should have_selector('div', text: player.name)
          should have_link(player.name, href: player_path(player))
        end
      end

      it {should have_header(text: 'My Referees')}

      it "lists all the referees for the user" do
        user.referees.each do |ref|
          should have_selector('div', text: ref.name)
        end
      end

      it {should have_header(text: 'My Contests')}

      it "lists all the contests for the user" do
        user.contests.each do |contest|
          should have_selector('div', text: contest.name)
        end
      end
    end

    describe "all" do
      before do
        FactoryBot.create_list(:user, 10)
        visit users_path
      end

      it {should have_header(text: 'Users')}

      User.all.each do |user|
        it {should have_selector('li', text: user.username)}
      end
    end
  end

  describe "pagination" do
    before do
      FactoryBot.create_list(:user, 25)
      visit users_path
    end

    it {should have_content("#{User.count} found (displaying 1-10)")}

    it 'displays properly' do
      should have_selector('div.pagination')
      should_not have_link('← Previous')
      should_not have_link('1')
      should have_link('2', href: "/users?page=2")
      should have_link('3', href: "/users?page=3")
      should_not have_link('4')
      should have_link('Next →', href: "/users?page=2")
    end

    describe "last page" do
      before { click_link('3', href: "/users?page=3") }

      it 'displays properly' do
        should have_selector('div.pagination')
        should have_link('← Previous', href: "/users?page=2")
        should have_link('1', href: "/users?page=1")
        should have_link('2', href: "/users?page=2")
        should_not have_link('3')
        should_not have_link('4')
        should_not have_link('Next →')
      end

      it 'properly shows records displaying' do
        should have_content("#{User.count} found (displaying 21-25)")
      end
    end
  end

  describe 'search error' do
    let(:submit) {"Search"}

    before do
      FactoryBot.create(:user)
      visit users_path
      fill_in 'search', with: 'junk input'
      click_button submit
    end

    it {should have_content('No users found')}
    it {should_not have_link('2')}
  end

  describe 'search with pagination' do
    let(:submit) {"Search"}

    before do
      FactoryBot.create_list(:user, 11)
      visit users_path
      fill_in 'search', with: 'User'
      click_button submit
    end

    it {should have_content("#{User.count} found (displaying 1-10)")}

    it 'paginates properly' do
      within '#user_pagination' do
        should have_link('2')
        should_not have_link('3')
      end
    end
  end

  describe 'search without pagination' do
    let(:submit) {"Search"}

    before do
      FactoryBot.create(:user, username: "searchtest")
      visit users_path
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

  describe "Edit users" do
    describe "as User" do
      let (:user) {FactoryBot.create(:user)}
      let!(:orig_username) {user.username}
      let (:submit) {'Update Account'}

      before do
        login user
        visit edit_user_path(user)
      end

      it {should have_selector("h2", text: "Edit Account")}

      it "has the proper fields" do
        should have_field('Username', with: user.username)
        should have_field('Email', with: user.email)
        should_not have_field('Password', with: user.password)
      end

      describe "with invalid information" do
        before do
          fill_in 'Username', with: ''
          fill_in 'Email', with: user.email
          fill_in 'Password', with: user.password
          fill_in 'Confirmation', with: user.password
        end

        describe "does not change data" do
          before {click_button submit}

          specify {expect(user.reload.username).not_to eq('')}
          specify {expect(user.reload.username).to eq(orig_username)}
        end

        it "does not add a new user to the system" do
          expect {click_button submit}.not_to change(User, :count)
        end

        it "produces an error message" do
          click_button submit
          should have_alert(:danger)
        end
      end

      describe "with forbidden attributes", type: :request do
        describe 'admin' do
          before do
            login user, avoid_capybara: true
            patch user_path(user), params: {user: {admin: true,
                                                   password: user.password,
                                                   password_confirmation: user.password}}
          end

          specify {expect(user.reload).not_to be_admin}
        end

        describe 'contest_creator' do
          before do
            login user, avoid_capybara: true
            patch user_path(user), params: {user: {contest_creator: true,
                                                   password: user.password,
                                                   password_confirmation: user.password}}
          end

          specify {expect(user.reload).not_to be_contest_creator}
        end
      end

      describe "with valid information" do
        before do
          fill_in 'Username', with: 'Changed name'
          fill_in 'Email', with: 'new@example.com'
          fill_in 'Password', with: user.password
          fill_in 'Confirmation', with: user.password
        end

        describe "changes the data" do
          before {click_button submit}

          specify {expect(user.reload.username).to eq('Changed name')}
          specify {expect(user.reload.email).to eq('new@example.com')}
        end

        describe "redirects properly", type: :request do
          before do
            login user, avoid_capybara: true
            patch user_path(user), params: {user: {username: 'Changed name',
                                                   email: user.email,
                                                   password: user.password,
                                                   password_confirmation: user.password}}
          end

          specify {expect(response).to redirect_to(user_path(user))}
        end

        it "produces an update message" do
          click_button submit
          should have_alert(:success)
        end

        it "does not add a new user to the system" do
          expect {click_button submit}.not_to change(User, :count)
        end
      end
    end

    describe "as admin" do
      let (:admin) {FactoryBot.create(:admin)}
      let (:user) {FactoryBot.create(:user)}
      let!(:orig_username) {user.username}
      let (:submit) {'Update Account'}

      before do
        login admin
        visit edit_user_path(user)
      end

      it "has the proper fields" do
        should have_field('Username', with: user.username)
        should have_field('Email', with: user.email)
        should_not have_field('Password', with: user.password)
      end

      describe "with invalid information" do
        before do
          fill_in 'Username', with: ''
          fill_in 'Email', with: user.email
          fill_in 'Password', with: user.password
          fill_in 'Confirmation', with: user.password
        end

        describe "does not change data" do
          before {click_button submit}

          specify {expect(user.reload.username).not_to eq('')}
          specify {expect(user.reload.username).to eq(orig_username)}
        end

        it "does not add a new user to the system" do
          expect {click_button submit}.not_to change(User, :count)
        end

        it "produces an error message" do
          click_button submit
          should have_alert(:danger)
        end
      end

      describe "with permission attributes", type: :request do
        describe 'admin' do
          before do
            login admin, avoid_capybara: true
            patch user_path(user), params: {user: {admin: true}}
          end

          specify {expect(user.reload).to be_admin}
        end

        describe 'contest_creator' do
          before do
            login admin, avoid_capybara: true
            patch user_path(user), params: {user: {contest_creator: true}}
          end

          specify {expect(user.reload).to be_contest_creator}
        end
      end

      describe "with valid information" do
        before do
          fill_in 'Username', with: 'Changed name'
          fill_in 'Email', with: 'new@example.com'
          fill_in 'Password', with: user.password
          fill_in 'Confirmation', with: user.password
        end

        describe "redirects properly", type: :request do
          before do
            login admin, avoid_capybara: true
            patch user_path(user), params: {user: {username: 'Changed name',
                                                   email: user.email,
                                                   password: user.password,
                                                   password_confirmation: user.password}}
          end

          specify {expect(response).to redirect_to(user_path(user))}
        end

        it "produces an update message" do
          click_button submit
          should have_alert(:success)
        end

        it "does not add a new user to the system" do
          expect {click_button submit}.not_to change(User, :count)
        end
      end
    end

    describe "Delete users" do
      describe "as anonymous" do
        let!(:user) {FactoryBot.create(:user)}
        before {visit user_path(user)}

        it {should_not have_link('Delete')}
      end

      describe "as a user" do
        let (:user) {FactoryBot.create(:user)}

        before do
          login user
          visit user_path(user)
        end

        it {should_not have_link('Delete')}
      end

      describe "as admin" do
        let (:admin) {FactoryBot.create(:admin)}
        let!(:user) {FactoryBot.create(:user)}

        before do
          login admin
          visit user_path(user)
        end

        it {should have_link('Delete', href: user_path(user))}

        describe "redirects properly", type: :request do
          before do
            login admin, avoid_capybara: true
            delete user_path(user)
          end

          specify {expect(response).to redirect_to(users_path)}
        end

        it "produces a delete message" do
          click_link('Delete', match: :first)
          should have_alert(:success)
        end

        it "removes a user from the system" do
          expect {click_link('Delete', match: :first)}.to change(User, :count).by(-1)
        end
      end

      describe "as another admin" do
        let! (:admin1) {FactoryBot.create(:admin)}
        let! (:admin2) {FactoryBot.create(:admin)}

        before do
          login admin2
          visit user_path(admin1)
        end

        it {should have_link('Delete', href: user_path(admin1))}

        describe "redirects properly", type: :request do
          before do
            login admin2, avoid_capybara: true
            delete user_path(admin1)
          end

          specify {expect(response).to redirect_to(users_path)}
        end
      end

      describe "as admin deleting yourself" do
        let! (:admin) {FactoryBot.create(:admin)}

        before do
          login admin
          visit user_path(admin)
        end

        it {should_not have_link('Delete', href: user_path(admin))}
      end
    end
  end
end
