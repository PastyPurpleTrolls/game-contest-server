class PlayerRound < ActiveRecord::Base
  belongs_to :round, inverse_of: :player_rounds
  belongs_to :player

  validates :round, presence: true
  validates :player, presence: true
  validates :round_id, :presence => true
  validates :player_id, :presence => true
  validates :result, inclusion: [nil, 'error', 'Win', 'Loss', 'Tie', 'Crash', 'Time out', 'Unknown Round Result']

end
