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
from random import randint

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



class Tamagotchi:

    def __init__(self):
        self.hunger = randint(2,5)
        self.fatness = 0
        self.health = randint(10, 20)
        self.dead = False

    def age(self):
        self.health -= randint(1, 4)
        self.hunger += 1


    def kill(self):
        self.dead = True

    def feed(self):
        self.hunger -= 1
        self.fatness += 1

    def inject(self):
        self.health += randint(4, 8)

    def face(self):
        eye = 'o'
        if self.health < 10:
            eye = '~'
        if self.dead:
            return self.add_size('xvx')
        face = '{0}v{0}'.format(eye)
        return self.add_size(face)

    def add_size(self,inner_face):
        return self.sizeness('(', self.fatness) + inner_face +  self.sizeness(')', self.fatness)

    @staticmethod
    def sizeness(c, size):
        return c*size


def feed(t):
    t.feed()
    return t

def inject(t):
    t.inject()
    return t

def check(t):
    if t.fatness > 2:
        t.kill()
    return t

def tamagotchi(t):
    universe_width = 30
    x = universe_width/2
    direction = 1
    speed = 1
    snake_width = 1
    kgen = getch(0.1)
    key_map = {'f': feed, 'i': inject}
    rand_x = random.randint(0, universe_width-1)
    food_waiting = False
    i = 0
    while 1:
        c = kgen.next()
        action = key_map.get(c, None)

        if action:
            action(t)
            check(t)
            i += 1

        t.age()

        if x not in range(universe_width):
            print 'Game Over'
            print 'You scored {}!'.format(speed)
            sys.exit()
        os.system('clear')
        print
        print ('Score: ' + str(i)).center(universe_width)
        print
        print t.face().center(universe_width)
        if t.dead:
            print 'GAME OVER!'
            break

if __name__ == '__main__':
    tamagotchi(Tamagotchi())