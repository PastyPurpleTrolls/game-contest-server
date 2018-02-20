class AddIndexToContestsName < ActiveRecord::Migration[5.1]
  def change
    add_index :contests, :name, unique: true
  end
end
