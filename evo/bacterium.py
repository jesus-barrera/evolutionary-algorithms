import math
import numpy as np
import copy
import random
from evo import EvolutionaryAlgorithm as EA, Generation, Individual

class Cell(Individual):
    def __init__(self, vector):
        Individual.__init__(self, vector)

        self.cost = 0
        self.avg_cost = 0

class BacterialForaging(EA):
    def __init__(
            self,
            step_size=0.2   ,
            population_size=50,
            chemotaxis_steps=100,
            reduction_steps=4,
            reproduction_steps=4,
            elimination_steps=2,
            attraction_depth=1,
            repulsion_depth=1,
            attraction_width=0.2,
            repulsion_width=10,
            elimination_probability=0.25):

        EA.__init__(self, population_size, 0, 0)

        self._step_size = step_size
        self._chemotaxis_steps = chemotaxis_steps
        self._reduction_steps = reduction_steps
        self._reproduction_steps = reproduction_steps
        self._elimination_steps = elimination_steps
        self._attraction_depth = attraction_depth
        self._repulsion_depth = repulsion_depth
        self._attraction_width = attraction_width
        self._repulsion_width = repulsion_width
        self._elimination_probability = elimination_probability

    def optimize(
            self,
            function,
            lower_bounds=[],
            upper_bounds=[],
            problem_type='min'):

        self._set_problem(function, lower_bounds, upper_bounds, problem_type)
        self._init_population()

        self.generations = []

        global_best = None

        for l in range(self._elimination_steps):
            print len(self._population)
            for k in range(self._reproduction_steps):
                best = self._chemotaxis()

                # update global best
                if not global_best or best.cost < global_best.cost:
                    global_best = best

                # sort by averange effective cost
                self._population.sort(key=lambda cell: cell.cost)

                # eliminate worst individuals and clone the best
                best = self._population[:self._population_size/2]

                self._population = best + best

            for cell in self._population:
                if random.random() <= self._elimination_probability:
                    cell.vector = EA._rand_individual(self)

        return global_best.vector

    def _evolve(self):
        return

    def _chemotaxis(self):
        for j in range(self._chemotaxis_steps):
            best = None

            for cell in self._population:
                self._compute_effective_cost(cell)

                if not best or cell.cost < best.cost:
                    best = copy.deepcopy(cell)

                cell.avg_cost = cell.cost
                v = self._rand_unit_vector()

                for m in range(self._reduction_steps):
                    # tumble cell
                    other = Cell(cell.vector + self._step_size * v)

                    self._compute_effective_cost(other)

                    if other.cost < cell.cost:
                        cell.vector = other.vector
                        cell.cost = other.cost

                        cell.avg_cost += cell.cost
                    else:
                        break

            population = [copy.deepcopy(cell.vector)
                          for cell in self._population]

            generation = Generation(population, (best.vector, self._evaluate(best)))

            self.generations.append(generation)

        return best

    def _compute_effective_cost(self, cell):
        sum = 0

        for other in self._population:
            diff = np.ndarray.sum((cell.vector - other.vector)**2)

            sum += (self._repulsion_depth * math.exp(-self._repulsion_width * diff)
                    - self._attraction_depth * math.exp(-self._attraction_width * diff))

        cell.cost =  self._cost(cell) + sum

    def _rand_unit_vector(self):
        v = np.random.uniform(-1, 1, self._dimensions)

        return v / np.linalg.norm(v)

    def _rand_individual(self):
        return Cell(EA._rand_individual(self))

    def _evaluate(self, cell):
        return self._function(*cell.vector)
