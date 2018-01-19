class PlayerMatch < ActiveRecord::Base
  belongs_to :player
  belongs_to :match , inverse_of: :player_matches
  has_one :match_log_info, as: :match_source 

  validates :player,    presence: true
  validates :match,     presence: true

  validates :result,  	inclusion: [nil,'Pending', 'Error', 'Win', 'Loss', 'Tie', 'Unknown Result']

#	validate :check_ids

  #default_scope -> { order("player_matches.result DESC") }
  default_scope -> { order("player_matches.created_at DESC")}
  scope :wins, -> { where(result: 'Win') }
  scope :losses, -> { where(result: 'Loss') }

 	
  def check_ids
    pm_count =  PlayerMatch.where(match_id: self.match_id, player_id: self.player_id).where.not(id: self.id).count
#   puts pr_count
    if pm_count > 0
      errors.add(:match_id, "you cannot have more than one player match with the same player and match id")
    end
  end
 
 
  def self.search(player, search)
    if search.blank?
      player.player_matches
    else
      find_by_sql("SELECT pm1.* FROM players AS p1 INNER JOIN player_matches AS pm1 ON pm1.player_id = p1.id INNER JOIN matches ON matches.id = pm1.match_id INNER JOIN player_matches AS pm2 ON pm2.match_id = matches.id INNER JOIN players AS p2 ON pm2.player_id = p2.id WHERE p1.id = #{player.id} AND #{sanitize_sql ["p2.name = '%s'", search]}")
    end
  end
end
