class MatchLogInfo < ActiveRecord::Base

  belongs_to :match_source, polymorphic: true

  def get_owner
    source = self.match_source
    if self.is_player_log?
      return source.player.user
    end
    if self.is_referee_log?
      return source.manager.referee.user
    end
    nil
  end

  def is_player_log?
    self.match_source_type.to_s == "PlayerMatch"
  end

  def is_referee_log?
    self.match_source_type.to_s == "Match"
  end

  def has_match_source?
    self.match_source != nil
  end

  def has_match_source_with_self?
    self.match_source.match_log_info == self
  end

  def valid_log?(log)
    !log.nil? && log.length > 0
  end

  def has_logs?
    valid_log?(self.log_stdout) && valid_log?(self.log_stderr)
  end
end
