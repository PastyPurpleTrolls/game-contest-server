class Round < ActiveRecord::Base
  belongs_to :match

  
  has_many :player_rounds, dependent: :destroy
  has_many :players, through: :player_rounds
  
  validates :match, presence: true

  def name
    return SecureRandom.hex(5)
  end
      
  extend FriendlyId
  friendly_id :name, use: :slugged


	validate :same_players_as_match 

	def same_players_as_match
		if match.present? && match.players != players
			errors.add(:players, "must be the same as the match's players")
		end
	end
end
