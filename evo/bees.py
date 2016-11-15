import copy
import random
from evo import EvolutionaryAlgorithm as EA, Generation
from tools import RandomSelector

class ForagerBee():
    def __init__(self, position):
        self.position = position
        self.trial_count = 0

class ArtificialBeeColony(EA):
    def __init__(
            self,
            population_size=100):

        EA.__init__(self, population_size, 0, 0)

        self._foragers_size = self._population_size / 2
        self._onlookers_size = self._foragers_size

        self._foragers = []

    def _init_algorithm(self):
        self._stagnation_limit = self._population_size * self._dimensions / 2

        self._init_foragers()

    def _init_foragers(self):
        self._foragers = [self._rand_forager()
                          for i in range(self._foragers_size)]

    def _evolve(self):
        self._do_forager_phase()
        self._do_onlooker_phase()
        self._do_scout_phase()

    def _do_forager_phase(self):
        for forager in self._foragers:
            self._forager_search(forager)

    def _do_onlooker_phase(self):
        selector = RandomSelector()

        for forager in self._foragers:
            selector.add(forager, self._fitness(forager))

        for i in range(self._onlookers_size):
            forager = selector.choose()

            self._forager_search(forager)

    def _do_scout_phase(self):
        for forager in self._foragers:
            if forager.trial_count > self._stagnation_limit:
                forager.position = EA._rand_individual(self)
                forager.trial_count = 0

    def _forager_search(self, forager):
        choice = forager

        while choice is forager:
            choice = random.choice(self._foragers)

        d = random.randrange(self._dimensions)
        r = random.uniform(-1, 1)

        trial = ForagerBee(copy.copy(forager.position))

        trial.position[d] = (forager.position[d]
                             + r * (forager.position[d] - choice.position[d]))

        if self._fitness(trial) > self._fitness(forager):
            forager.position = trial.position
            forager.trial_count = 0
        else:
            forager.trial_count += 1

    def _rand_forager(self):
        position = EA._rand_individual(self)

        return ForagerBee(position)

    def _sort_population(self):
        is_maximize = self._problem_type == 'max'

        self._foragers.sort(key=self._evaluate, reverse=is_maximize)

    def _evaluate(self, bee):
        return self._function(*bee.position)

    def _best(self):
        return self._foragers[0].position

    def _get_generation(self):
        positions = [copy.copy(bee.position)
                     for bee in self._foragers]

        best = positions[0]

        return Generation(positions, (best, self._function(*best)))
