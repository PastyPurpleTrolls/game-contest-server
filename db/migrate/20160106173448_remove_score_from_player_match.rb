class RemoveScoreFromPlayerMatch < ActiveRecord::Migration
  def change
    remove_column :player_matches, :score, :float
  end
end
