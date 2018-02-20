class AddSlugToRounds < ActiveRecord::Migration[5.1]
  def change
    add_column :rounds, :slug, :string
  end
end
