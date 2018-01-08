class AddIndexToRefereesName < ActiveRecord::Migration[5.1]
  def change
    add_index :referees, :name, unique: true
  end
end
