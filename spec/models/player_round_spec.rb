require 'rails_helper'

describe PlayerRound do
  let (:player_round) { FactoryGirl.create(:player_round) }
  subject { player_round }

  # Tables
  it { should respond_to(:player) }
  it { should respond_to(:round) }

	# Attributes
  it { should respond_to(:result) }
  it { should respond_to(:score) }

	# Validations
	it { should be_valid }

end
