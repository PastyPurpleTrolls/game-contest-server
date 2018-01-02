require 'rails_helper'

describe PlayerTournament do
  let (:player_tournament) { FactoryBot.create(:player_tournament) }
  subject { player_tournament }

  # Tables
  it { should respond_to(:player) }
  it { should respond_to(:tournament) }

  describe "validations" do
    it { should be_valid }
    specify { expect_required_attribute(:player) }
    specify { expect_required_attribute(:tournament) }
  end
end
