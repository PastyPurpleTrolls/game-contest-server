class RenameContestManagerToReferee < ActiveRecord::Migration[5.1]
  def change
    rename_table :contest_managers, :referees
  end
end
