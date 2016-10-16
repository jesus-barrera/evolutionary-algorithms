import random
from collections import namedtuple

Interval = namedtuple('Interval', ['min', 'max'])

class RandomSelector:
    Item = namedtuple('Item', ['data', 'weight'])

    def __init__(self):
        self.items = []
        self.total_weight = 0

    def add(self, data, weight):
        self.items.append(self.Item(data, weight))

        self.total_weight += weight

    def pick(self):
        accumulated = 0
        rand = random.uniform(0, self.total_weight)

        picked = None

        for item in self.items:
            accumulated += item.weight

            if accumulated >= rand:
                picked = item.data
                break

        return picked
