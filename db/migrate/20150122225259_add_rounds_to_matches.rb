class AddRoundsToMatches < ActiveRecord::Migration[5.1]
  def change
    add_column :matches, :rounds, :integer
  end
end
