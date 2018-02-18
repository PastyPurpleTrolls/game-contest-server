#! /usr/bin/env ruby
#
#wrapper_test.rb
#Can be used test any players and referees without having to worry about tournaments/databases/etc

require_relative 'round_wrapper'

class MockPlayer
  attr_accessor :file_location, :name, :rounds_capable

  def initialize(file_location, name)
    self.file_location = file_location
    self.name = name
    @rounds_capable = false
  end
end

#p1 = MockPlayer.new("../examples/test_player.py","first")
#p2 = MockPlayer.new("../examples/test_player.py", "second")
#ref = MockPlayer.new("../examples/guess_w_referee.py", "ref")

p1 = MockPlayer.new("../examples/checkers/checkers_players/player1.py", "first")
p2 = MockPlayer.new("../examples/checkers/checkers_players/player2.py", "second")
ref = MockPlayer.new("../examples/checkers/checkers_referee.py", "ref")

=begin
p1 = MockPlayer.new("../examples/risk/risk_player.py", "first")
p2 = MockPlayer.new("../examples/risk/risk_player.py", "second")
p3 = MockPlayer.new("../examples/risk/risk_player.py", "third")
p4 = MockPlayer.new("../examples/risk/risk_player.py", "fourth")
ref = MockPlayer.new("../examples/risk/risk_referee.py", "ref")
=end

round_wrapper = RoundWrapper.new(ref, 2, 10, [p1, p2], 1)
round_wrapper.run_match

puts(round_wrapper.status)
puts round_wrapper.rounds
