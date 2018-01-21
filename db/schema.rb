# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20180115194902) do

  create_table "contests", force: :cascade do |t|
    t.integer "user_id"
    t.integer "referee_id"
    t.text "description"
    t.string "slug", limit: 255
    t.datetime "created_at"
    t.datetime "updated_at"
    t.datetime "deadline"
    t.string "name", limit: 255
    t.index ["name"], name: "index_contests_on_name", unique: true
    t.index ["referee_id"], name: "index_contests_on_referee_id"
    t.index ["slug"], name: "index_contests_on_slug", unique: true
    t.index ["user_id"], name: "index_contests_on_user_id"
  end

  create_table "friendly_id_slugs", force: :cascade do |t|
    t.string "slug", limit: 255, null: false
    t.integer "sluggable_id", null: false
    t.string "sluggable_type", limit: 50
    t.string "scope", limit: 255
    t.datetime "created_at"
    t.index ["slug", "sluggable_type", "scope"], name: "index_friendly_id_slugs_on_slug_and_sluggable_type_and_scope", unique: true
    t.index ["slug", "sluggable_type"], name: "index_friendly_id_slugs_on_slug_and_sluggable_type"
    t.index ["sluggable_id"], name: "index_friendly_id_slugs_on_sluggable_id"
    t.index ["sluggable_type"], name: "index_friendly_id_slugs_on_sluggable_type"
  end

  create_table "match_log_infos", force: :cascade do |t|
    t.string "log_stdout"
    t.string "log_stderr"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.integer "match_source_id"
    t.string "match_source_type"
    t.index ["match_source_type", "match_source_id"], name: "index_match_log_infos_on_match_source_type_and_match_source_id"
  end

  create_table "match_paths", force: :cascade do |t|
    t.integer "parent_match_id"
    t.integer "child_match_id"
    t.string "result", limit: 255
    t.datetime "created_at"
    t.datetime "updated_at"
    t.index ["child_match_id"], name: "index_match_paths_on_child_match_id"
    t.index ["parent_match_id"], name: "index_match_paths_on_parent_match_id"
  end

  create_table "matches", force: :cascade do |t|
    t.integer "manager_id"
    t.datetime "completion"
    t.datetime "created_at"
    t.datetime "updated_at"
    t.string "status", limit: 255
    t.datetime "earliest_start"
    t.string "manager_type", limit: 255
    t.string "slug"
    t.integer "num_rounds"
    t.string "match_name"
    t.index ["manager_id", "manager_type"], name: "index_matches_on_manager_id_and_manager_type"
    t.index ["manager_id"], name: "index_matches_on_manager_id"
    t.index ["slug"], name: "index_matches_on_slug", unique: true
  end

  create_table "player_matches", force: :cascade do |t|
    t.integer "player_id"
    t.integer "match_id"
    t.datetime "created_at"
    t.datetime "updated_at"
    t.string "result", limit: 255
    t.string "log_out"
    t.string "log_err"
    t.index ["match_id"], name: "index_player_matches_on_match_id"
    t.index ["player_id"], name: "index_player_matches_on_player_id"
  end

  create_table "player_rounds", force: :cascade do |t|
    t.integer "round_id"
    t.integer "player_id"
    t.string "result"
    t.float "score"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["player_id"], name: "index_player_rounds_on_player_id"
    t.index ["round_id"], name: "index_player_rounds_on_round_id"
  end

  create_table "player_tournaments", force: :cascade do |t|
    t.integer "tournament_id"
    t.integer "player_id"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "players", force: :cascade do |t|
    t.integer "user_id"
    t.integer "contest_id"
    t.string "file_location", limit: 255
    t.integer "programming_language_id"
    t.string "slug", limit: 255
    t.datetime "created_at"
    t.datetime "updated_at"
    t.text "description"
    t.string "name", limit: 255
    t.boolean "downloadable", default: false
    t.boolean "playable", default: true
    t.index ["contest_id"], name: "index_players_on_contest_id"
    t.index ["name", "contest_id"], name: "index_players_on_name_and_contest_id", unique: true
    t.index ["programming_language_id"], name: "index_players_on_programming_language_id"
    t.index ["slug"], name: "index_players_on_slug", unique: true
    t.index ["user_id"], name: "index_players_on_user_id"
  end

  create_table "programming_languages", force: :cascade do |t|
    t.string "name", limit: 255
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "referees", force: :cascade do |t|
    t.string "file_location", limit: 255
    t.integer "programming_language_id"
    t.string "slug", limit: 255
    t.datetime "created_at"
    t.datetime "updated_at"
    t.string "name", limit: 255
    t.string "rules_url", limit: 255
    t.integer "players_per_game"
    t.integer "user_id"
    t.string "compressed_file_location"
    t.integer "round_limit"
    t.integer "time_per_game"
    t.boolean "rounds_capable"
    t.string "replay_assets_location", limit: 255
    t.index ["name"], name: "index_referees_on_name", unique: true
    t.index ["programming_language_id"], name: "index_referees_on_programming_language_id"
    t.index ["slug"], name: "index_referees_on_slug", unique: true
    t.index ["user_id"], name: "index_referees_on_user_id"
  end

  create_table "rounds", force: :cascade do |t|
    t.integer "match_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.string "slug"
    t.string "round_name"
    t.index ["match_id"], name: "index_rounds_on_match_id"
  end

  create_table "testings", force: :cascade do |t|
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "tournaments", force: :cascade do |t|
    t.string "tournament_type", limit: 255
    t.integer "contest_id"
    t.datetime "start"
    t.string "name", limit: 255
    t.string "status", limit: 255
    t.string "slug", limit: 255
    t.datetime "created_at"
    t.datetime "updated_at"
    t.integer "rounds_per_match"
    t.integer "total_matches"
    t.index ["slug"], name: "index_tournaments_on_slug", unique: true
  end

  create_table "users", force: :cascade do |t|
    t.string "username", limit: 255
    t.string "slug", limit: 255
    t.datetime "created_at"
    t.datetime "updated_at"
    t.string "email", limit: 255
    t.string "password_digest", limit: 255
    t.boolean "admin", default: false
    t.boolean "contest_creator", default: false
    t.boolean "banned", default: false
    t.string "chat_url", limit: 255
    t.index ["slug"], name: "index_users_on_slug", unique: true
    t.index ["username"], name: "index_users_on_username", unique: true
  end

end
