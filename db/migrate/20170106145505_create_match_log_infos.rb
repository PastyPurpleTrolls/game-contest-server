class CreateMatchLogInfos < ActiveRecord::Migration[5.1]
  def change
    create_table :match_log_infos do |t|
      t.string :log_stdout
      t.string :log_stderr

      t.timestamps null: false
    end
  end
end
