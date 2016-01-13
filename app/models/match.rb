class Match < ActiveRecord::Base

  attr_accessor :match_limit

  belongs_to :manager, polymorphic: true
  has_many :player_matches , inverse_of: :match , dependent: :destroy
  has_many :players, through: :player_matches
  has_many :rounds, dependent: :destroy

  accepts_nested_attributes_for :player_matches
  has_many :parent_matches, class_name: 'MatchPath', foreign_key: 'child_match_id', dependent: :destroy
  has_many :child_matches, class_name: 'MatchPath', foreign_key: 'parent_match_id', dependent: :destroy

  validates :manager,           presence: true
  validates :status,            presence: true, inclusion: %w[unassigned waiting started completed]
  validates :earliest_start,    presence: true, timeliness: { type: :datetime, allow_nil: false }, unless: :started?
  validates :completion,
    timeliness: { type: :datetime, on_or_before: :now },
    if: :completed?
	validates :num_rounds,				presence: true

#	validate :correct_number_of_rounds
  validate :correct_number_of_players, unless: :unassigned?
  validate :players_allowed_to_play, if: :tournament_match?

	validates_numericality_of :num_rounds, allow_nil: false
	validates_numericality_of :num_rounds, greater_than: 0

  def unassigned?
    status == 'unassigned'
  end

  def waiting?
    status == 'waiting'
  end

  def started?
    %w(started completed).include? status
  end

  def completed?
    status == 'completed'
  end

  def player_ids=(ids)
    ids.each do |p, use|
      self.player_matches.build(player: Player.find(p))
    end
  end


  def correct_number_of_players
    return if self.player_matches.nil? || self.manager.nil?
      errors.add(:players, "number of players must equal " +
                 self.manager.referee.players_per_game.to_s +
                 " you have " + self.player_matches.length.to_s +
                 " players") unless self.player_matches.length ==
                                    self.manager.referee.players_per_game
  end

#	def correct_number_of_rounds
#		puts self.num_rounds
#		puts Round.all.count
#		return if (self.num_rounds >= Round.where(match_id: self.id).count)
#	end

  def tournament_match?
    return if self.manager.nil?

    self.manager_type == "Tournament"
  end

  # Makes sure players are in the tournament the match is in
  def players_allowed_to_play
    return if self.manager.nil? || self.players.nil?

    self.players.each do |p|
      unless p.tournaments.include? self.manager
        errors.add(:match, "players must be in same tournament as match")
      end
    end
  end

  def name
    self.players.map(&:name).join("-")
  end

  extend FriendlyId
  friendly_id :name, use: :slugged

end
