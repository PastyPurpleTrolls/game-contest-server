class RemoveMaxMatchFromReferees < ActiveRecord::Migration[5.1]
  def change
    remove_column :referees, :max_match, :int
  end
end
