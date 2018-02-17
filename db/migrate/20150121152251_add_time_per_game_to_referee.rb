class AddTimePerGameToReferee < ActiveRecord::Migration[5.1]
  def change
    add_column :referees, :time_per_game, :integer
  end
end
