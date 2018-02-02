class AddMatchLimitToReferees < ActiveRecord::Migration[5.1]
  def change
    add_column :referees, :match_limit, :int
  end
end
