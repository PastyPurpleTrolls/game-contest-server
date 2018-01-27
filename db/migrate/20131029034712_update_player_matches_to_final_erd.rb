class UpdatePlayerMatchesToFinalErd < ActiveRecord::Migration[5.1]
  def change
    add_column :player_matches, :result, :string
  end
end
