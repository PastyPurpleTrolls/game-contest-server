class AddRoundsCapableColumnToReferees < ActiveRecord::Migration[5.1]
  def change
    add_column :referees, :rounds_capable, :boolean
  end
end
