class Contest < ActiveRecord::Base
  belongs_to :user
  belongs_to :referee
  has_many :tournaments
  has_many :players
  has_many :matches, as: :manager
  accepts_nested_attributes_for :matches
  
  validates :referee,       presence: true
  validates :user,          presence: true

  validates :deadline,      timeliness: { type: :datetime, allow_nil: false, on_or_after: :now }
  validates :description,   presence: true
  validates :name,          presence: true, uniqueness: true

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

  extend FriendlyId
  friendly_id :name, use: :slugged
  after_validation :move_friendly_id_error_to_name

  def move_friendly_id_error_to_name
    errors.add :name, *errors.delete(:friendly_id) if errors[:friendly_id].present?
  end

end
