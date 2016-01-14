class PlayerRound < ActiveRecord::Base
  belongs_to :round, inverse_of: :player_rounds
  belongs_to :player

	validates :round_id, :presence => true
	validates :player_id, :presence => true
  validates :result,  	inclusion: [nil, 'Win', 'Loss', 'Tie', 'Crash', 'Time out', 'Unknown Round Result']
	
	validate :check_ids

	def check_ids 
		pr_count =  PlayerRound.where(round_id: self.round_id, player_id: self.player_id).count
		if pr_count > 1
			errors.add(:count, "you cannot have more than one player round with the same player and round id")
		end
	end
end
