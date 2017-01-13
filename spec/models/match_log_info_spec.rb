require 'rails_helper'

describe MatchLogInfo do
  let (:match_log_info_player) {FactoryGirl.create(:match_log_info_player) }
  subject { match_log_info_player }
  
  describe "validation" do 
    it { should respond_to(:has_match_source?) }
    it { should respond_to(:has_match_source_with_self?) }
    it { should respond_to(:has_logs?) }
  end
end

describe MatchLogInfo do
  let (:match_log_info_referee) {FactoryGirl.create(:match_log_info_referee) }
  subject { match_log_info_referee }
  
  describe "validation" do 
    it { should respond_to(:has_match_source?) }
    it { should respond_to(:has_match_source_with_self?) }
    it { should respond_to(:has_logs?) }
  end
end
