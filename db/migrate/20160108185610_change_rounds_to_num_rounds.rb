class ChangeRoundsToNumRounds < ActiveRecord::Migration[5.1]
  def change
      rename_column :matches, :rounds, :num_rounds
  end
end
