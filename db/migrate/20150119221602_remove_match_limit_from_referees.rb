class RemoveMatchLimitFromReferees < ActiveRecord::Migration[5.1]
  def change
    remove_column :referees, :match_limit, :int
  end
end
