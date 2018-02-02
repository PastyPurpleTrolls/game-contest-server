class AddRoundsPerMatchToTournaments < ActiveRecord::Migration[5.1]
  def change
    add_column :tournaments, :rounds_per_match, :integer
  end
end
