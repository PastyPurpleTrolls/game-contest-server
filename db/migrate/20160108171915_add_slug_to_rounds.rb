class AddSlugToRounds < ActiveRecord::Migration
  def change
    add_column :rounds, :slug, :string
  end
end
