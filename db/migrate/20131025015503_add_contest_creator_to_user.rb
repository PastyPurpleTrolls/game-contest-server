class AddContestCreatorToUser < ActiveRecord::Migration[5.1]
  def change
    add_column :users, :contest_creator, :boolean, default: false
  end
end
