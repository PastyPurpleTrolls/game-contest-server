class UseRefereeIdInTables < ActiveRecord::Migration[5.1]
  def change
    rename_column :contests, :contest_manager_id, :referee_id
  end
end
