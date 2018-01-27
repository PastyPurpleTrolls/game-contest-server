class AddCompressedFileLocationToReferee < ActiveRecord::Migration[5.1]
  def change
    add_column :referees, :compressed_file_location, :string
  end
end
