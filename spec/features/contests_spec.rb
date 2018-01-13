require 'rails_helper'

include ActionView::Helpers::DateHelper

describe "ContestsPages" do
  let (:creator) {FactoryBot.create(:contest_creator)}
  let!(:referee) {FactoryBot.create(:referee)}
  let (:now) {mins_multiple_of_5(1.hour.from_now)}
  let (:name) {'Test Contest'}
  let (:description) {'Contest description'}

  subject {page}

  describe "create" do
    let (:submit) {'Create Contest'}

    before do
      login creator
      visit new_contest_path
    end

    it {should have_selector("h2", text: "Add Contest")}

    describe "invalid information" do
      describe "missing information" do
        it "should not create a contest" do
          expect {click_button submit}.not_to change(Contest, :count)
        end

        describe "after submission" do
          before {click_button submit}
          it {should have_alert(:danger)}
        end
      end

      illegal_dates.each do |date|
        describe "illegal date (#{date.to_s})" do
          before do
            select_illegal_datetime('Deadline', date)
            fill_in 'Description', with: description
            fill_in 'Name', with: name
            select referee.name, from: 'Referee'
            click_button submit
          end

          it {pending; should have_alert(:danger)}
        end
      end
    end

    describe "valid information" do
      before do
        select_datetime(now, 'Deadline')
        fill_in 'Description', with: description
        fill_in 'Name', with: name
        select referee.name, from: 'Referee'
      end

      it "should create a contest" do
        expect {click_button submit}.to change(Contest, :count).by(1)
      end

      describe "redirects properly", type: :request do
        before do
          login creator, avoid_capybara: true
          post contests_path, params: {contest: {deadline: now.strftime("%F %T"),
                                                 description: description, name: name, referee_id: referee.id}}
        end

        specify {expect(response).to redirect_to(contest_path(assigns(:contest)))}
      end

      describe "after submission" do
        let (:contest) {Contest.find_by(name: name)}

        before {click_button submit}

        specify {expect(contest.user).to eq(creator)}

        it {should have_alert(:success, text: 'Contest created')}

        it "shows all contest information" do
          should have_content(/About 1 Hour/)
          should have_content(description)
          should have_content(name)
          should have_content(contest.referee.name)
          should have_link('', href: new_contest_player_path(contest))
        end
      end
    end
  end

  describe "edit" do
    let (:contest) {FactoryBot.create(:contest, user: creator, deadline: now)}
    let!(:orig_name) {contest.name}
    let (:submit) {'Update Contest'}

    before do
      login creator
      visit edit_contest_path(contest)
    end

    it {should have_selector("h2", text: "Edit Contest")}

    it "has the proper fields" do
      should have_content(contest.referee.name)
      should have_field('Name', with: contest.name)
      should have_field('Description', with: contest.description)
      expect_datetime_select(contest.deadline, 'Deadline')
    end

    describe "with invalid information" do
      before do
        select_datetime(now, 'Deadline')
        fill_in 'Name', with: ''
        fill_in 'Description', with: description
      end

      describe "does not change data" do
        before {click_button submit}

        specify {expect(contest.reload.name).not_to eq('')}
        specify {expect(contest.reload.name).to eq(orig_name)}
      end

      it "does not add a new contest to the system" do
        expect {click_button submit}.not_to change(Contest, :count)
      end

      it "produces an error message" do
        click_button submit
        should have_alert(:danger)
      end
    end

    describe "with valid information" do
      before do
        select_datetime(now, 'Deadline')
        fill_in 'Name', with: name
        fill_in 'Description', with: description
      end

      describe "changes the data" do
        before {click_button submit}

        it {should have_alert(:success)}
        specify {expect_same_minute(contest.reload.deadline, now)}
        specify {expect(contest.reload.name).to eq(name)}
        specify {expect(contest.reload.description).to eq(description)}
        it {should have_link('', href: new_contest_player_path(contest))}
      end

      describe "redirects properly", type: :request do
        before do
          login creator, avoid_capybara: true
          patch contest_path(contest), params: {contest: {deadline: now.strftime("%F %T"),
                                                          description: description,
                                                          name: name,
                                                          referee_id: referee.id}}
        end

        specify {expect(response).to redirect_to(contest_path(contest))}
      end

      it "does not add a new contest to the system" do
        expect {click_button submit}.not_to change(Contest, :count)
      end
    end
  end

  describe "destroy", type: :request do
    let!(:contest) {FactoryBot.create(:contest, user: creator)}

    before do
      login creator, avoid_capybara: true
    end

    describe "redirects properly" do
      before {delete contest_path(contest)}
      specify {expect(response).to redirect_to(contests_path)}
    end

    it "produces a delete message" do
      delete contest_path(contest)
      get response.location
      response.body.should have_alert(:success)
    end

    it "removes a contest from the system" do
      expect {delete contest_path(contest)}.to change(Contest, :count).by(-1)
    end
  end

  describe "pagination" do
    before do
      FactoryBot.create_list(:contest, 25)
      visit contests_path
    end

    it {should have_content("#{Contest.count} found (displaying 1-10)")}

    it 'displays properly' do
      should have_selector('div.pagination')
      should_not have_link('← Previous')
      should_not have_link('1')
      should have_link('2', href: "/contests?page=2")
      should have_link('3', href: "/contests?page=3")
      should_not have_link('4')
      should have_link('Next →', href: "/contests?page=2")
    end

    describe "last page" do
      before { click_link('3', href: "/contests?page=3") }

      it 'displays properly' do
        should have_selector('div.pagination')
        should have_link('← Previous', href: "/contests?page=2")
        should have_link('1', href: "/contests?page=1")
        should have_link('2', href: "/contests?page=2")
        should_not have_link('3')
        should_not have_link('4')
        should_not have_link('Next →')
      end

      it 'properly shows records displaying' do
        should have_content("#{Contest.count} found (displaying 21-25)")
      end
    end
  end

  describe 'search error' do
    let(:submit) {"Search"}

    before do
      visit contests_path
      fill_in 'search', with: 'junk input'
      click_button submit
    end

    it {should have_content("No contests found")}
    it {should_not have_link('2')}
  end

  describe 'search partial' do
    let(:submit) {"Search"}

    before do
      FactoryBot.create_list(:contest, 11)
      visit contests_path
      fill_in 'search', with: 'Contest'
      click_button submit
    end

    it {should have_content("#{Contest.count} found (displaying 1-10)")}

    it 'paginates properly' do
      should have_link('2')
      should_not have_link('3')
    end
  end

  describe 'search' do
    let(:submit) {"Search"}

    before do
      FactoryBot.create(:contest, name: "searchtest")
      visit contests_path
      fill_in 'search', with: 'searchtest'
      click_button submit
    end

    it 'should return results' do
      should have_button('searchtest')
      should have_content('1 found')
    end
  end

  describe "show" do
    let (:contest) {FactoryBot.create(:contest, user: creator)}

    describe "as any user" do
      before {visit contest_path(contest)}

      it "shows all contest information" do
        should have_selector("h2", text: "Contest")
        should have_content(contest.name)
        should have_content(contest.description)
        should have_content(distance_of_time_in_words_to_now(contest.deadline)
                              .split.map {|i| i.capitalize}.join(' '))
        should have_content(contest.user.username)
        should have_link(contest.user.username, href: user_path(contest.user))
        should have_content(contest.referee.name)
        should have_link(contest.referee.name, href: referee_path(contest.referee))
      end

      it "lists all the players in the contest" do
        Player.where(contest: contest).each do |player|
          should have_selector('li', text: player.name)
          should have_link(t.name, href: player_path(player))
        end
      end

      it {should_not have_link('', href: new_contest_player_path(contest))}
      it {should have_link('', href: new_contest_match_path(contest))}
    end

    describe "as contest_creator" do
      before do
        login creator
        visit contest_path(contest)
      end

      it "shows all contest information" do
        should have_selector("h2", text: "Contest")
        should have_content(contest.name)
        should have_content(contest.description)
        should have_content(distance_of_time_in_words_to_now(contest.deadline)
                              .split.map {|i| i.capitalize}.join(' '))
        should have_content(contest.user.username)
        should have_link(contest.user.username, href: user_path(contest.user))
        should have_content(contest.referee.name)
        should have_link(contest.referee.name, href: referee_path(contest.referee))
      end

      it "lists all the players in the contest" do
        Player.where(contest: contest).each do |player|
          should have_selector('li', text: player.name)
          should have_link(t.name, href: player_path(player))
        end
      end

      it {should have_link('', href: new_contest_player_path(contest))}
      it {should have_link('', href: new_contest_match_path(contest))}
    end

  end

  describe "show all as any user" do
    before do
      FactoryBot.create_list(:contest, 5)
      visit contests_path
    end

    it "does not have adding option" do
      should_not have_link('', href: new_contest_path)
    end

    it {should have_selector("h2", text: "Contest")}

    it "lists all the contests in the system" do
      Contest.all.each do |c|
        should have_selector("form[action='#{contest_path(c)}']")
        within "form[action='#{contest_path(c)}']" do
          should have_selector('input.results-container')
          should have_button(c.name)
        end
      end
    end
  end

  describe "show all as contest_creator" do
    before do
      login creator
      visit contests_path
    end

    it "has adding option" do
      should have_link('', href: new_contest_path)
    end

    it {should have_selector("h2", text: "Contest")}
  end
end
