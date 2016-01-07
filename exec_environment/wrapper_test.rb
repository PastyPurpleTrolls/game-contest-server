#! /usr/bin/env ruby
#
#Alex Sjoberg
#wrapper_test.rb
#Jan 2014
#Can be used test any players and referees without having to worry about tournaments/databases/etc

require_relative 'round_wrapper'

class MockPlayer
    attr_accessor :file_location , :name, :rounds_capable
    def initialize(file_location,name)
        self.file_location = file_location
        self.name = name
        @rounds_capable = true
    end
end

p1 = MockPlayer.new("../examples/checkers_player.py","first")
p2 = MockPlayer.new("../examples/checkers_player.py", "second")
ref = MockPlayer.new("../examples/checkers_ref.py", "ref")


#p1 = MockPlayer.new("../spec/exec_environment/test_player.py","first")
#p2 = MockPlayer.new("../spec/exec_environment/test_player.rb", "second")
#ref = MockPlayer.new("../spec/exec_environment/test_referee.rb", "ref")

round_wrapper = RoundWrapper.new(ref, 2, 5, [p1, p2], 3)
round_wrapper.run_match

puts(round_wrapper.results)


