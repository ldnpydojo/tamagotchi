"""
Based on: https://docs.python.org/2/faq/library.html#how-do-i-get-a-single-keypress-at-a-time
"""

import os
import sys
import time
from contextlib import contextmanager

import fcntl
import termios

import os
import random
import string
import sys
import time

@contextmanager
def stdin_setup():
    fd = sys.stdin.fileno()
    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

    try:
        yield
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

def getch(timeout=0):
    while True:
        c = None
        start = time.time()
        with stdin_setup():
            while True:
                duration = time.time() - start
                if timeout and timeout < duration:
                    break
                try:
                    c = sys.stdin.read(1)
                except IOError:
                    pass
                if c:
                    break
        yield c




def tamagotchi():
    universe_width = 100
    x = universe_width/2
    direction = 1
    speed = 1
    snake_width = 1
    kgen = getch(0.1)
    key_map = {'D': -1, 'C': 1}
    rand_x = random.randint(0, universe_width-1)
    food_waiting = False
    while 1:
        c = kgen.next()
        direction = key_map.get(c, direction)
        x += direction * speed
        if x in range(rand_x, rand_x+speed):
            speed += 1
            food_waiting = False
        if x not in range(universe_width):
            print 'Game Over'
            print 'You scored {}!'.format(speed)
            sys.exit()
        os.system('clear')
        print '\n'*10
        print ('Score: ' + str(speed)).center(universe_width)
        print
        print '(oVo)'

if __name__ == '__main__':
    tamagotchi()