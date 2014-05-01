
class Tamagochi(object):
    def __init__(self):
        self.rate = 8
        self.attributes = {
            'hunger': 0.0,
            'fatigue': 0.0,
            'unhappiness': 0.0,
            'thirst': 0.0,
        }

        self.sleeping = False

    def _cap_attribute(self, attribute):
        if self.attributes[attribute] < 0.0:
            return 0.0
        elif self.attributes[attribute] > 100.0:
            return 100.0
        return self.attributes[attribute]

    def update(self, elapsed):
        self._update_thirst(elapsed)
        self._update_hunger(elapsed)
        self._update_fatigue(elapsed)
        self._update_unhappiness(elapsed)

        for attribute in self.attributes:
            self.attributes[attribute] = self._cap_attribute(attribute)

        if self.attributes['hunger'] >= 100.0:
            self.die('You forgot to feed him!')
        elif self.attributes['thirst'] >= 100.0:
            self.die('Great, he died of dehydration!')

    def _update_thirst(self, elapsed): 
        self.attributes['thirst'] += elapsed * self.rate

    def _update_hunger(self, elapsed):
        self.attributes['hunger'] += elapsed * self.rate


    def _update_fatigue(self, elapsed):
        if self.sleeping:
            self.attributes['fatigue'] -= elapsed * 4 * self.rate
        else:
            self.attributes['fatigue'] += elapsed * self.rate

    def _update_unhappiness(self, elapsed):
        if not self.sleeping:
            self.attributes['unhappiness'] += elapsed * self.rate

    def feed(self):
        if not self.sleeping:
            self.attributes['hunger'] -= 20.0
            self._cap_attribute('hunger')

    def drink(self):
        if not self.sleeping:
            self.attributes['thirst'] -= 20.0

    def play(self):
        if not self.sleeping:
            self.attributes['unhappiness'] -= 20

    def sleep(self):
        self.rate = 4
        self.sleeping = True

    def wake(self):
        self.rate = 8
        self.sleeping = False