class AddMatchSourceToMatchLogInfo < ActiveRecord::Migration
  def change
    add_reference :match_log_infos, :match_source, polymorphic: true, index: true
  end
end
