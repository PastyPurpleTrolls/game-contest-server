class Round < ActiveRecord::Base
  belongs_to :match

  has_many :player_rounds, dependent: :destroy
  has_many :players, through: :player_rounds

  validates :match, presence: true
  validate :check_num_rounds, on: :create
  validate :same_players_as_match

  extend FriendlyId
  friendly_id :name, use: :slugged

  def name
    SecureRandom.hex(5)
  end

  def check_num_rounds
    unless self.match.nil?
      rounds = Round.where(match_id: self.match_id).count
      num_rounds = Match.find(self.match_id).num_rounds
      if rounds > num_rounds
        errors.add(:count, "you have more rounds than this match allows")
      end
    end
  end

  def same_players_as_match
    if match.present? && players.present? && match.players != players
      errors.add(:players, "must be the same as the match's players")
    end
  end

  def winners
    player_rounds = self.player_rounds.where(result: 'Win').includes(:player)
    players = []
    player_rounds.each do |player_round|
      players << player_round.player.name
    end
    players.join(', ')
  end
end
