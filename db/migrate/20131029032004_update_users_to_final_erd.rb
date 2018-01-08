class UpdateUsersToFinalErd < ActiveRecord::Migration[5.1]
  def change
    add_column :users, :banned, :boolean, default: false
    add_column :users, :chat_url, :string
  end
end
