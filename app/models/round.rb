class Round < ActiveRecord::Base
  belongs_to :match

  def name
    return SecureRandom.hex(5)
  end
      
  extend FriendlyId
  friendly_id :name, use: :slugged
end
