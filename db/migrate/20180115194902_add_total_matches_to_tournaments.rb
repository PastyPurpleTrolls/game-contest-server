class AddTotalMatchesToTournaments < ActiveRecord::Migration[5.1]
  def change
    add_column :tournaments, :total_matches, :integer
  end
end
