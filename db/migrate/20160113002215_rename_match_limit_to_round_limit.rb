class RenameMatchLimitToRoundLimit < ActiveRecord::Migration[5.1]
  def change
		change_table :referees do |t|
			t.rename :match_limit, :round_limit
		end
  end
end
