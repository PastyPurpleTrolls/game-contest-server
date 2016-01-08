require 'rails_helper'

describe Round do
  let (:round) { FactoryGirl.create(:round) }
  subject { round }

  # Tables
  it { should respond_to(:match) }
	it { should respond_to(:player_rounds) }
	it { should respond_to(:players) }

	# Attributes there are none currently
end
