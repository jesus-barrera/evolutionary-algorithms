import copy
import random
import numpy as np
from evo import EvolutionaryAlgorithm as EA

class DifferentialEvolution(EA):
    def __init__(
            self,
            population_size=40,
            crossover_rate=0.1,
            stepsize=0.5):

        EA.__init__(self, population_size, 0, 0)

        self.crossover_rate = crossover_rate
        self.stepsize = stepsize

    def _evolve(self):
        children = []

        for i, individual in enumerate(self._population):
            population = copy.copy(self._population)
            del population[i] # make sure current individual is not selected

            r1, r2, r3 = random.sample(population, 3)

            mutant = r1 + self.stepsize * (r2 - r3)

            # crossover
            trial = np.zeros(self._dimensions)
            rj = random.randrange(self._dimensions)

            for j in range(self._dimensions):
                if random.random() <= self.crossover_rate or j == rj:
                    trial[j] = mutant[j]
                else:
                    trial[j] = individual[j]

            if self._cost(trial) < self._cost(individual):
                children.append(trial)
            else:
                children.append(individual)

        self._population = children
