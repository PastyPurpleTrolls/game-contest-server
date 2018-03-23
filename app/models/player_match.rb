class PlayerMatch < ActiveRecord::Base
  belongs_to :player
  belongs_to :match , inverse_of: :player_matches
  has_one :match_log_info, as: :match_source 

  validates :player,    presence: true
  validates :match,     presence: true
  validates :result,  	inclusion: [nil,'Pending', 'Error', 'Win', 'Loss', 'Tie', 'Unknown Result']

  default_scope -> { order("player_matches.result DESC") }
  scope :wins, -> { where(result: 'Win') }
  scope :losses, -> { where(result: 'Loss') }
  scope :ties, -> { where(result: 'Tie') }

  def self.search(player, search)
    if search.blank?
      player.player_matches
    else
      find_by_sql("SELECT pm1.* FROM players AS p1 INNER JOIN player_matches AS pm1 ON pm1.player_id = p1.id INNER JOIN matches ON matches.id = pm1.match_id INNER JOIN player_matches AS pm2 ON pm2.match_id = matches.id INNER JOIN players AS p2 ON pm2.player_id = p2.id WHERE p1.id = #{player.id} AND #{sanitize_sql ["p2.name = '%s'", search]}")
    end
  end

  def self.win_percentage
    if self.count == 0
      0.0
    else
      (self.wins.count.to_f / self.count * 100).round(2)
    end
  end
end
