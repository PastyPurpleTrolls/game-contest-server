class AddIndexToPlayersName < ActiveRecord::Migration[5.1]
  def change
    add_index :players, :name, unique: true
  end
end
