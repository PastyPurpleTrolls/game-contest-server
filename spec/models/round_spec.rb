require 'rails_helper'

describe Round do
  let (:round) { FactoryGirl.create(:round) }
  subject { round }

  # Tables
  it { should respond_to(:match) }

end
