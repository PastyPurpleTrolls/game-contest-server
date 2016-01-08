class ChangeRoundsToNumRounds < ActiveRecord::Migration
  def change
      rename_column :matches, :rounds, :num_rounds
  end
end
