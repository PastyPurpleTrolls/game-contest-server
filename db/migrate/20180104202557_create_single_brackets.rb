class CreateSingleBrackets < ActiveRecord::Migration[5.1]
  def change
    create_table :single_brackets do |t|

      t.timestamps
    end
  end
end
