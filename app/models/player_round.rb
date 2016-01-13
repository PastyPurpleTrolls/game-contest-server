class PlayerRound < ActiveRecord::Base
  belongs_to :round
  belongs_to :player

  validates :round,           presence: true
  validates :player,           presence: true
end
