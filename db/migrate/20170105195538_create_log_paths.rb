class CreateLogPaths < ActiveRecord::Migration
  def change
    dir_players = "#{Rails.root}/code/players/"
    dir_referees= "#{Rails.root}/code/referees/"

    Process.spawn("for dir in #{dir_players}*/*/; do mkdir -p ${dir}logs; done")
    Process.spawn("for dir in #{dir_referees}*/*/; do mkdir -p ${dir}logs; done")
  end
end
