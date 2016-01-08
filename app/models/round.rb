class Round < ActiveRecord::Base
  belongs_to :match
<<<<<<< HEAD
  
  has_many :player_rounds, dependent: :destroy
  has_many :players, through: :player_rounds
  
  validates :player_rounds, presence: true
  validates :players, presence: true
  validates :match, presence: true

  def name
    return SecureRandom.hex(5)
  end
      
  extend FriendlyId
  friendly_id :name, use: :slugged
end
