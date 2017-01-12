require 'rails_helper'

feature "HomePage" do
  before { visit root_path }

  subject { page }

  describe "the navigation bar" do
    it { should have_selector('.navbar') }
    
    let (:admin) { FactoryGirl.create(:admin) }
    let (:creator) { FactoryGirl.create(:contest_creator) }
    let (:user) { FactoryGirl.create(:user) }    
    
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
      before do
        login user
      end
      it "has the proper links" do
        within ".navbar" do
          should have_link('Game Contest Server', href: root_path)
          should have_link('Contests', href: contests_path)
          should have_content('Account')          
        end
      end
    end

    describe "as contest_creator" do
      before do
        login creator
      end
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
      before do
        login admin
      end
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
end
