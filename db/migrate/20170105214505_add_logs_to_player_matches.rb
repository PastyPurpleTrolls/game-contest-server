class AddLogsToPlayerMatches < ActiveRecord::Migration
  def change
    add_column :player_matches, :log_out, :string
    add_column :player_matches, :log_err, :string
  end
end
