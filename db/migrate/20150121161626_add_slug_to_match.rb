class AddSlugToMatch < ActiveRecord::Migration[5.1]
  def change
    add_column :matches, :slug, :string
    add_index :matches, :slug, unique: true
  end
end
