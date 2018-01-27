class CreateUsers < ActiveRecord::Migration[5.1]
  def change
    create_table :users do |t|
      t.string :username, index: true
      t.string :slug

      t.timestamps
    end
    add_index :users, :slug, unique: true
  end
end
