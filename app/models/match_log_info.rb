class MatchLogInfo < ActiveRecord::Base
  belongs_to :match_source, polymorphic: true
end
