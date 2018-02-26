# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rake db:seed (or created alongside the db with db:setup).
#
# Examples:
#
#   cities = City.create([{ name: 'Chicago' }, { name: 'Copenhagen' }])
#   Mayor.create(name: 'Emanuel', city: cities.first)
%w(C C++ Java Python Ruby).each do |lang|
  ProgrammingLanguage.create(name: lang)
end

User.create!(
    username: "administrator",
    email: "admin@test.com",
    password: "password",
    password_confirmation: "password",
    admin: true,
    contest_creator: true,
    chat_url: "www.google.com"
)

creator = User.create!(
  username: "contestcreator",
  email: "creator@test.com",
  password: "password",
  password_confirmation: "password",
  admin: false,
  contest_creator: true,
  chat_url: "www.google.com"
)

student = User.create!(
  username: "student",
  email: "student@test.com",
  password: "password",
  password_confirmation: "password",
  admin: false,
  contest_creator: false,
  chat_url: "www.google.com"
)
(2..11).each do |user_num|
  User.create!(
    username: "student#{user_num}",
    email: "student#{user_num}@test.com",
    password: "password",
    password_confirmation: "password",
    admin: false,
    contest_creator: false,
    chat_url: "www.google.com"
  )
end

referee = Referee.create!(
  user: creator,
  name: "Guess W!",
  rules_url: "http://www.google.com",
  players_per_game: 2,
  file_location: Rails.root.join("examples", "guess-w", "python", "guess_w_referee.py").to_s,
  time_per_game: 2,
  round_limit: 100,
	rounds_capable: false
)
(2..11).each do |referee_num|
  Referee.create!(
    user: creator,
    name: "Guess W #{referee_num}",
    rules_url: "http://www.google.com",
    players_per_game: 2,
    file_location: Rails.root.join("examples", "guess-w", "python", "guess_w_referee.py").to_s,
    time_per_game: 2,
    round_limit: 100,
    rounds_capable: false
  )
end

contest = Contest.create!(
  user: creator,
  referee: referee,
  deadline: DateTime.now + 5.minutes,
  description: "test",
  name: "Contest 1"
)
(2..11).each do |contest_num|
  Contest.create!(
    user: creator,
    referee: referee,
    deadline: DateTime.now + 5.minutes,
    description: "test",
    name: "Contest #{contest_num}"
  )
end

player1 = Player.create!(
  user: student,
  contest: contest,
  description: "test",
  name: "Phil",
  downloadable: false,
  playable: false,
  file_location: Rails.root.join("examples", "guess-w", "python", "sometimes_win_player.py").to_s
)
player2 = Player.create!(
  user: student,
  contest: contest,
  description: "test",
  name: "Justin",
  downloadable: false,
  playable: false,
  file_location: Rails.root.join("examples", "guess-w", "python", "sometimes_win_player.py").to_s
)
player3 = Player.create!(
  user: student,
  contest: contest,
  description: "test",
  name: "Alex",
  downloadable: false,
  playable: false,
  file_location: Rails.root.join("examples", "guess-w", "python", "sometimes_win_player.py").to_s
)
player4 = Player.create!(
  user: student,
  contest: contest,
  description: "test",
  name: "Doug",
  downloadable: false,
  playable: false,
  file_location: Rails.root.join("examples", "guess-w", "python", "sometimes_win_player.py").to_s
)
player5 = Player.create!(
  user: student,
  contest: contest,
  description: "test",
  name: "David",
  downloadable: false,
  playable: false,
  file_location: Rails.root.join("examples", "guess-w", "python", "sometimes_win_player.py").to_s
)
player6 = Player.create!(
  user: student,
  contest: contest,
  description: "test",
  name: "Nathan",
  downloadable: false,
  playable: false,
  file_location: Rails.root.join("examples", "guess-w", "python", "sometimes_win_player.py").to_s
)
player7 = Player.create!(
  user: student,
  contest: contest,
  description: "test",
  name: "Juan",
  downloadable: false,
  playable: true,
  file_location: Rails.root.join("examples", "guess-w", "python", "sometimes_win_player.py").to_s
)
(8..11).each do |player_num|
  Player.create!(
    user: student,
    contest: contest,
    description: "test",
    name: "Player #{player_num}",
    downloadable: false,
    playable: false,
    file_location: Rails.root.join("examples", "guess-w", "python", "sometimes_win_player.py").to_s
  )
end

tournament = Tournament.create!(
  contest: contest,
  name: "Round Robin Test Tournament",
  start: Time.now + 10.seconds,
  tournament_type: "round robin",
  status: "waiting",
  rounds_per_match: 1
)
PlayerTournament.create!(player: player1, tournament: tournament)
PlayerTournament.create!(player: player2, tournament: tournament)
PlayerTournament.create!(player: player3, tournament: tournament)

tournament2 = Tournament.create!(
  contest: contest,
  name: "Single Elimination Test Tournament",
  start: Time.now + 10.seconds,
  tournament_type: "single elimination",
  status: "waiting",
  rounds_per_match: 1
)
PlayerTournament.create!(player: player1, tournament: tournament2)
PlayerTournament.create!(player: player2, tournament: tournament2)
PlayerTournament.create!(player: player3, tournament: tournament2)
PlayerTournament.create!(player: player4, tournament: tournament2)
PlayerTournament.create!(player: player5, tournament: tournament2)
PlayerTournament.create!(player: player6, tournament: tournament2)
PlayerTournament.create!(player: player7, tournament: tournament2)

(3..11).each do |tournament_num|
  Tournament.create!(
    contest: contest,
    name: "Tournament #{tournament_num}",
    start: Time.now + 10.seconds,
    tournament_type: "single elimination",
    status: "waiting",
    rounds_per_match: 1
  )
end