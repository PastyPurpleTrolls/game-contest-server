class Tournament < ActiveRecord::Base

  belongs_to :contest
  has_many :player_tournaments, inverse_of: :tournament #, dependent: :destroy
  has_many :players, through: :player_tournaments
  has_many :matches, as: :manager #, dependent: :destroy

  validates :rounds_per_match,    presence: true, numericality: { only_integer: true, greater_than: 0 }
  validates :contest,             presence: true
  validates :name,                presence: true, uniqueness: { scope: :contest }
  #validates :start,               presence: true, timeliness: { type: :datetime, allow_nil: false }
  validates :start,               presence: true
  validates :tournament_type,     presence: true, inclusion: ['round robin', 'single elimination', 'multiplayer game', 'king of the hill']
  # Validate that the status is one of the required statuses
  validates :status,              presence: true, inclusion: %w[waiting started completed]

  def referee
    contest.referee
  end
  
  def expected_disparity
  end
  
  def total_time
  end

  def RMSE
  end

  def self.search(search)
    if search
      where('name LIKE ?', "%#{search}%")
    else
      all
    end
  end

  def player_ids=(ids)
    ids.each do |p, use|
      self.player_tournaments.build(player: Player.find(p))
    end
  end
  

  extend FriendlyId
  friendly_id :name, use: :slugged
  after_validation :move_friendly_id_error_to_name

  def move_friendly_id_error_to_name
    errors.add :name, *errors.delete(:friendly_id) if errors[:friendly_id].present?
  end

  def started?
    self.status == 'started'
  end

  def completed?
    self.status == 'completed'
  end

  def available_players
    self.contest.players.select{ |p| !p.tournaments.include?(self) }.each
  end

  def percent_complete
    if self.matches.count == 0
      return 0
    end
    (self.matches.completed_matches.count.to_f / self.matches.count * 100).to_i
  end

  def human_readable_time(time)
    time = time.to_i
    seconds_in_year = 31536000
    seconds_in_week = 604800
    seconds_in_day = 86400
    seconds_in_hour = 3600
    seconds_in_minute = 60
    years = time / seconds_in_year
    weeks = time / seconds_in_week
    days = time / seconds_in_day
    hours = time / seconds_in_hour
    minutes = time / seconds_in_minute
    if time > seconds_in_year
      format("%s %s", years, 'year'.pluralize(years))
    elsif time > seconds_in_week
      format("%s %s", weeks, 'week'.pluralize(weeks))
    elsif time > seconds_in_day
      format("%s %s", days, 'day'.pluralize(days))
    elsif time > seconds_in_hour
      format("%s %s", hours, 'hour'.pluralize(hours))
    elsif time > seconds_in_minute
      format("%s %s", minutes, 'minute'.pluralize(minutes))
    else
      format("%s %s", time, 'second'.pluralize(time))
    end
  end

  def time_remaining
    completed_matches = self.matches.completed_matches
    num_completed_matches = completed_matches.count

    if num_completed_matches < 2
      return nil
    end

    completion_times = completed_matches.pluck(:completion).sort
    times_between_completion = []

    (1...num_completed_matches).each do |i|
      times_between_completion << completion_times[i] - completion_times[i-1]
    end

    average_times = times_between_completion.sum / num_completed_matches
    time_remaining = average_times * self.matches.uncompleted_matches.count
    human_readable_time(time_remaining)
  end

end
