class Round < ActiveRecord::Base
  belongs_to :match
  
  has_many :player_rounds, dependent: :destroy
  has_many :players, through: :player_rounds
  
end
