import random
from collections import namedtuple

Interval = namedtuple('Interval', ['min', 'max'])

class RandomSelector:
    Item = namedtuple('Item', ['data', 'weight'])

    def __init__(self):
        self.clear()

    def add(self, data, weight):
        self.items.append(self.Item(data, weight))
        self.total_weight += weight

    def assign(self, items):
        self.clear()

        for item in items: self.add(*item)

    def clear(self):
        self.items = []
        self.total_weight = 0

    def choose(self):
        picked = self.__choose(self.items, self.total_weight)

        if picked: return picked.data

    def sample(self, count):
        choosen = []
        items = self.items[:]

        while len(choosen) < count and len(items) > 0:
            picked = self.__choose(items)

            choosen.append(picked.data)
            items.remove(picked)

        return choosen

    def __choose(self, items, total_weight=None):
        if not total_weight:
            total_weight = sum([i.weight for i in items])

        accumulated = 0
        rand = random.uniform(0, total_weight)

        picked = None

        for item in items:
            accumulated += item.weight

            if accumulated >= rand:
                picked = item
                break

        return picked
