require 'uri'

class Referee < ActiveRecord::Base
    #  belongs_to :programming_language
    belongs_to :user
    has_many :contests

    validates :user,              presence: true
  	validates :round_limit,       presence: true, numericality: { only_integer: true, greater_than: 0 }
    validates :name,              presence: true, uniqueness: true
    validates :rules_url,		format: { with: /\A((http|https):\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,6}(:[0-9]{1,5})?(([\/][a-z0-9]*)*(([\/][a-z0-9]+([\-]{1}[a-z0-9]+)?)*\.[a-z]{2,6})?)?([\?]([a-z0-9]+[\=][a-z0-9]+[\&]?)*)?\z/ }
#    validate :valid_url
    validates :players_per_game,  numericality: { only_integer: true, greater_than: 0, less_than: 11 }
    validates :time_per_game,     numericality: { only_integer: true, greater_than: 0, less_than: 16 }
    validates :file_location,              presence: true
  	validates :rounds_capable,	inclusion: { in: [true, false] }	
    #  validates :programming_language, presence: true

    default_scope -> { order("created_at DESC") }

    include Uploadable


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

      def deletable?(u)
        u == user && contests.size == 0
    end

  def update_log_locations(new_location)
    new_dir = File.dirname(new_location)
    self.contests.each do |contest|
      contest.matches.each do |match|
        log_info = match.match_log_info
        unless log_info.nil?
          log_info.log_stdout = new_dir+"/logs/"+File.basename(log_info.log_stdout)
          log_info.log_stderr = new_dir+"/logs/"+File.basename(log_info.log_stderr)
          log_info.save!
	end
      end
      contest.tournaments.each do |tourney|
        contest.matches.each do |match|
          log_info = match.match_log_info
          unless log_info.nil?
            log_info.log_stdout = new_dir+"/logs/"+File.basename(log_info.log_stdout)
            log_info.log_stderr = new_dir+"/logs/"+File.basename(log_info.log_stderr)
	    log_info.save!
          end
        end
      end
    end
  end

    private

    def valid_url
	unless self.rules_url.blank?
	    uri = URI.parse(self.rules_url)
	    if uri.kind_of?(URI::HTTP) || uri.scheme.nil?
		self.errors.add(:rules_url, "is invalid")
	    end
	end
    rescue URI::InvalidURIError
	self.errors.add(:rules_url, "is invalid")
    end
end
