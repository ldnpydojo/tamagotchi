import bisect
import sys
import select
import time
import random


SPEED = 0.5
BASIC_STEP = 20


class SortedList(list):
    def append(self, item):
        self.insert(bisect.bisect(self, item), item)


class Tamagotchi(object):
    def __init__(self):
        self.events = SortedList()
        self.hunger = 0
        self.dirtiness = 0
        self.boredom = 0
        self.disease = 0
        self.anger = 0
        self.birth = time.time()
        self.add_event(SPEED, self.time_passes)

    def age(self):
        return int(time.time() - self.birth)

    def add_event(self, delay, event):
        self.events.append((time.time() + delay, event))

    def time_passes(self):
        self.hunger += 1
        self.dirtiness += 1
        self.boredom += 1
        if self.disease:
            self.disease += max(1, self.disease * 0.2)
        else:
            if random.randrange(10) == 1:
                self.disease = 1
        self.add_event(SPEED, self.time_passes)

    def poop(self):
        self.dirtiness += 20
        print "Tamagotchi poops!"

    def check_death(self):
        return max(self.hunger, self.dirtiness, self.boredom, self.disease, self.anger) >= 100

    def display(self):
        print "hunger:", self.hunger, " dirtiness:", self.dirtiness, " boredom:", self.boredom, " anger:", self.anger, " disease:", int(self.disease)

    def update(self):
        now = time.time()
        while self.events and now >= self.events[0][0]:
            self.events.pop(0)[1]()

    def next_event(self):
        if self.events:
            return self.events[0][0]
        return None

    def do_action(self, action):
        if not action.isalpha():
            return
        func = getattr(self, "action_" + action.lower(), None)
        if func:
            func()
            self.anger = max(self.anger - 20, 0)
        else:
            self.anger += 10

    def action_feed(self):
        self.hunger -= BASIC_STEP
        if self.hunger < 0:
            self.dirtiness -= self.hunger
            self.hunger = 0
        self.add_event(10, self.poop)

    def action_clean(self):
        self.dirtiness -= BASIC_STEP
        if self.dirtiness < 0:
            self.boredom -= self.dirtiness
            self.dirtiness = 0

    def action_play(self):
        self.boredom -= BASIC_STEP
        if self.boredom < 0:
            self.hunger -= self.boredom
            self.boredom = 0

    def action_heal(self):
        self.disease = 0
        self.boredom += 40


if __name__ == '__main__':
    pet = Tamagotchi()
    while not pet.check_death():
        pet.display()
        next_event_time = pet.next_event()
        if next_event_time:
            timeout = next_event_time - time.time()
        else:
            timeout = None
        r1, r2, r3 = select.select([sys.stdin], [], [], timeout)
        if r1:
            inp = sys.stdin.readline()
            print "received:", inp
            pet.do_action(inp.strip())

        pet.update()

    pet.display()
    print "Final age:", pet.age()
    if pet.anger >= 100:
        print "Tamagotchi has slain you in a murderous rage!"
    else:
        print "Alas poor tamagotchi! I knew him, Horatio."
