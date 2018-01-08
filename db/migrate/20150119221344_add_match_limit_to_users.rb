class AddMatchLimitToUsers < ActiveRecord::Migration[5.1]
  def change
    add_column :users, :match_limit, :int
  end
end
