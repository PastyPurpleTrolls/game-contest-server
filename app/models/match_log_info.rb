class MatchLogInfo < ActiveRecord::Base

  belongs_to :match_source, polymorphic: true

  def get_owner
    source = self.match_source
    if self.is_player_log? then
      return source.player.user
    end
    if self.is_referee_log? then
      return source.manager.referee.user
    end
    return nil
  end

  def is_player_log?
    return self.match_source_type.to_s == "PlayerMatch"
  end

  def is_referee_log?
    return self.match_source_type.to_s == "Match"
  end

  def has_match_source?
    return self.match_source != nil
  end

  def has_match_source_with_self?
    return self.match_source.match_log_info == self
  end

  def has_logs?
    if self.log_stdout == nil then return false end
    if self.log_stderr == nil then return false end
    if self.log_stdout.length == 0 then return false end
    if self.log_stderr.length == 0 then return false end
    return true
  end
end
