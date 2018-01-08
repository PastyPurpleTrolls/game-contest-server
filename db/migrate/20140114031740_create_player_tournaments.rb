class CreatePlayerTournaments < ActiveRecord::Migration[5.1]
  def change
    create_table :player_tournaments do |t|
      t.references :tournament
      t.references :player


      t.timestamps
    end
  end
end
