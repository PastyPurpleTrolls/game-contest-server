class AddAssetsFileLocationToReferee < ActiveRecord::Migration[5.1]
  def change
      add_column :referees, :replay_assets_location, :string, :limit => 255
  end
end
