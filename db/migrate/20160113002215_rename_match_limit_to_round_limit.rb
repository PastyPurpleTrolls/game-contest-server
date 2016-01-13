class RenameMatchLimitToRoundLimit < ActiveRecord::Migration
  def change
		change_table :referees do |t|
			t.rename :match_limit, :round_limit
		end
  end
end
