class CreateMatches < ActiveRecord::Migration[5.1]
  def change
    create_table :matches do |t|
      t.references :contest, index: true
      t.datetime :occurance
      t.float :duration

      t.timestamps
    end
  end
end
