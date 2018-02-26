#! /usr/bin/env python3

import random
import talk_to_referee

asciiVal = random.choice(range(97, 123))
move = chr(asciiVal)

talk_to_referee.init(move)