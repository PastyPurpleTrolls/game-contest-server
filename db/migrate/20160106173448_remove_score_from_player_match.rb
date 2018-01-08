class RemoveScoreFromPlayerMatch < ActiveRecord::Migration[5.1]
  def change
    remove_column :player_matches, :score, :float
  end
end
