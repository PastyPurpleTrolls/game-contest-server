class CreatePlayerRounds < ActiveRecord::Migration
  def change
    create_table :player_rounds do |t|
      t.references :round, index: true, foreign_key: true
      t.references :player, index: true, foreign_key: true
      t.string :result
      t.float :score

      t.timestamps null: false
    end
  end
end
