class UpdateIndexToPlayersName < ActiveRecord::Migration[5.1]
  def change
     remove_index :players, :name
     add_index :players, [:name, :contest_id], unique: true
  end
end
