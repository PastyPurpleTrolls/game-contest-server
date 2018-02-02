class RemoveMatchLimitFromUsers < ActiveRecord::Migration[5.1]
  def change
    remove_column :users, :match_limit, :int
  end
end
