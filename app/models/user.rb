class User < ActiveRecord::Base
  has_secure_password

  has_many :referees
  has_many :players
  has_many :contests

  validates :username, presence: true, length: { maximum: 25 }, uniqueness: true

  #
  # Note that the email regex is from Michael Hartl's Rails tutorial
  # and does a "good enough" job.  It misses some addresses that are
  # officially acceptable, but silly to check for.  He even has a more
  # robust email regex in his homework section at the end of Chapter 6.
  #
  validates :email, presence: true,
    format: { with: /\A[\w+\-.]+@[a-z\d\-.]+\.[a-z]+\z/i }

  default_scope -> { order("created_at DESC") }

  def self.search(search)
    if search
      where('username LIKE ?', "%#{search}%")
    else
      all
    end
  end

  extend FriendlyId
  friendly_id :username, use: :slugged
  after_validation :move_friendly_id_error_to_username

  def move_friendly_id_error_to_username
    errors.add :username, *errors.delete(:friendly_id) if errors[:friendly_id].present?
  end

  def can_edit_contest?(contest)
    (self == contest.user and self.contest_creator) or self.admin
  end

  def can_edit_player?(player)
    self == player.user or self.admin
  end

  def can_delete_player?(player)
    (self == player.user or self.can_edit_contest?(player.contest)) and player.matches.size == 0
  end

  def can_delete_player_with_warning?(player)
    self.can_edit_contest?(player.contest)
  end

  def can_edit_referee?(referee)
    (self == referee.user and self.contest_creator) or self.admin
  end

  def can_edit_tournament?(tournament)
    (self == tournament.contest.user and self.contest_creator) or self.admin
  end
end
