import math
import random
import pdb

from evo import EvolutionaryAlgorithm
from tools import RandomSelector, Interval

class ContinuousACO(EvolutionaryAlgorithm):
    """Continuous Ant Colony Optimization.

    A simple ant system for solving a continuous-domain problem in a n-dimensional
    space.
    """

    def __init__(
            self,
            population_size=100,
            num_elites=1,
            pheromone_importance=1,
            evaporation_rate=0.8,
            deposition_constant=100,
            initial_pheromone=1e-5,
            num_intervals=40):

        EvolutionaryAlgorithm.__init__(self, population_size, 0, num_elites)

        self.pheromone_importance = pheromone_importance
        self.evaporation_rate = evaporation_rate
        self.deposition_constant = deposition_constant
        self.initial_pheromone = initial_pheromone
        self.num_intervals = num_intervals

        self.pheromones = []

    def evolve(self, max_generations):
        self.discretize()
        self.init_pheromones()
        self.init_population()

        elite_ants = []

        for generation in range(max_generations):
            selectors = []

            # set the probabilities for each interval in each dimension
            for dimension in self.dimensions:
                selector = RandomSelector()

                for i, pheromone in enumerate(self.pheromones[dimension]):
                    # the weight indicates the relative probability for the
                    # interval to be selected, which is proportional to its
                    # amount of pheromones.
                    weight = math.pow(pheromone, self.pheromone_importance)
                    selector.add(self.intervals[i], weight)

                selectors.append(selector)

            for ant in self.population:
                for dimension in self.dimensions:
                    # randomly select an interval on this dimension
                    interval = selectors[dimension].pick()

                    # set the solution within the selected interval
                    ant[dimension] = random.uniform(interval.min, interval.max)

            # place elite ants back to the colony
            self.population.extend(elite_ants)

            deposited_pheromones = map(self.deposited_pheromones, self.population)

            # evaporation and deposition of pheromones
            for dimension in self.dimensions:
                pheromones = self.pheromones[dimension]

                for i, interval in enumerate(self.intervals):
                    # evaporate pheromones of interval
                    pheromones[i] *= 1 - self.evaporation_rate

                    # deposit pheromones in visitied intervals
                    for k, ant in enumerate(self.population):
                        if  interval.min <= ant[dimension] < interval.max:
                            pheromones[i] += deposited_pheromones[k]

            self.sort_population()

            best_ant = self.population[0]

            # remove elite ants from colony
            elite_ants = self.population[:self.num_elites]
            self.population = self.population[self.num_elites:]

            # print best solution
            print '{}: f{} = {}'.format(generation, best_ant, self.evaluate(best_ant))

    def discretize(self):
        """Divides the problem's domain into discretized intervals."""

        self.intervals = []

        step = (self.domain.max - self.domain.min) / float(self.num_intervals)

        for i in range(self.num_intervals):
            start = self.domain.min + step * i
            end = start + step

            self.intervals.append(Interval(start, end))

    def init_pheromones(self):
        """Sets the initial pheromone amount for each discrete interval in each dimension."""

        self.pheromones = [[self.initial_pheromone for interval in self.intervals]
                           for dimension in self.dimensions]

    def deposited_pheromones(self, ant):
        """Calculates the ammount of pheromones deposited by an ant."""

        return self.deposition_constant / self.cost(ant)
