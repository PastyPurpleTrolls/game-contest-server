#! /usr/bin/env python3

import random
import talk_to_referee

def move():
    asciiVal = random.choice(range(97, 123))
    return chr(asciiVal)

talk_to_referee.init(move)