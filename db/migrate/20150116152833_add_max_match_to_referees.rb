class AddMaxMatchToReferees < ActiveRecord::Migration[5.1]
  def change
    add_column :referees, :max_match, :int
  end
end
