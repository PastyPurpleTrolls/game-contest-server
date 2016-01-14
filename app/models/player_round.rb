class PlayerRound < ActiveRecord::Base
  belongs_to :round, inverse_of: :player_rounds
  belongs_to :player
=begin
<<<<<<< HEAD

  validates :round,           presence: true
  validates :player,           presence: true
=======
=end
	
	validates :round_id, :presence => true
	validates :player_id, :presence => true
  validates :result,  	inclusion: [nil, 'error', 'Win', 'Loss', 'Tie', 'Crash', 'Time out', 'Unknown Round Result']
#	validates_uniqueness_of :round_id, scope: :player_id 
	
	validate :check_ids

	def check_ids 
		pr_count =  PlayerRound.where(round_id: self.round_id, player_id: self.player_id).count
		if pr_count > 1
			errors.add(:count, "you cannot have more than one player round with the same player and round id")
		end
	end
=begin
>>>>>>> 2042a496d8a3de42ef23b5007c647a47bb77bb47
=end
end
