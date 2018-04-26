class Contest < ActiveRecord::Base
  belongs_to :user
  belongs_to :referee
  has_many :tournaments
  has_many :players
  has_many :matches, as: :manager
  accepts_nested_attributes_for :matches
  
  validates :referee,       presence: true
  validates :user,          presence: true

  #validates :deadline,      timeliness: { type: :datetime, allow_nil: false, on_or_after: :now }
  validates :deadline, presence: true
  validates :description,   presence: true
  validates :name,          presence: true, uniqueness: true

  before_save :remove_invalid_characters

  default_scope -> { order("created_at DESC") }

  def contest
      self
  end

  def self.search(search)
    if search
      where('name LIKE ?', "%#{search}%")
    else
      all
    end
  end

  def playable_players_by(user)
    playable_players = self.players.where(playable: true)
    user_unplayable_players = self.players.where(playable: false).where(user_id: user.id)
    playable_players.or(user_unplayable_players)
  end

  extend FriendlyId
  friendly_id :name, use: :slugged
  after_validation :move_friendly_id_error_to_name

  def move_friendly_id_error_to_name
    errors.add :name, *errors.delete(:friendly_id) if errors[:friendly_id].present?
  end

  def remove_invalid_characters
    self.name.gsub!("'", '')
    self.name.gsub!('"', '')
  end
end
