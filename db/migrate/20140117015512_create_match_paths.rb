class CreateMatchPaths < ActiveRecord::Migration[5.1] 
    def change
      create_table :match_paths do |t|      
          t.references :parent_match, index: true
          t.references :child_match, index: true
          t.string :result
          t.timestamps
      end
    end
end
