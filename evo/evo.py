import abc
import random
import numpy as np
from collections import namedtuple
from tools import Interval

MINIMIZE = 0
MAXIMIZE = 1

OFFSET = 1000

Generation = namedtuple('Generation', ['population', 'best'])

class EvolutionaryAlgorithm:
    """Evolutionary Algorithm for solving optimization problems."""

    __metaclass__ = abc.ABCMeta

    def __init__(
            self,
            population_size,
            mutation_probability,
            num_elites):

        self._population_size = population_size
        self._mutation_probability = mutation_probability
        self._num_elites = num_elites

        self._population = []

    def optimize(
            self,
            function,
            lower_bounds=[],
            upper_bounds=[],
            problem_type=MINIMIZE,
            max_generations=100):
        """Optimize a function using evolutionary techniques.

        Arguments:
        function -- objective function
        lower_bounds -- lower bounds for each variable
        upper_bounds -- upper bounds for each variable
        problem_type -- tells if MINIMIZE or MAXIMIZE the objective function (default MINIMIZE)
        max_generations -- number of generations to evolve the solution (default 100)
        """

        self._set_problem(function, lower_bounds, upper_bounds, problem_type)
        self._init_algorithm()

        self.generations = []

        count = 0

        while True:
            self._sort_population()

            self.generations.append(self._get_generation())

            if count < max_generations:
                self._evolve()
                count += 1
            else:
                break

        return self._best()

    def _init_algorithm(self):
        self._init_population()

    def _init_population(self):
        self._population = [self._rand_individual()
                            for i in range(self._population_size)]

    @abc.abstractmethod
    def _evolve(self):
        return

    def _get_generation(self):
        population = copy.copy(self.population)
        best = population[0], self._function(*population[0])

        return Generation(population, best)

    def _rand_individual(self):
        params = []

        for i in range(self._dimensions):
            rand = np.random.uniform(self._lower_bounds[i], self._upper_bounds[i])
            params.append(rand)

        return np.array(params)

    def _sort_population(self):
        is_maximize = self._problem_type == MAXIMIZE

        self._population.sort(key=self._evaluate, reverse=is_maximize)

    def _best(self):
        return self._population[0]

    def _evaluate(self, individual):
        return self._function(*individual)

    def _pick_elites(self):
        elites = self._population[:self._num_elites]

        self._population = self._population[self._num_elites:]

        return elites

    def _set_problem(self, function, lower_bounds, upper_bounds, problem_type):
        self._function = function
        self._problem_type = problem_type

        # calculate dimensions
        self._dimensions = function.func_code.co_argcount

        # set boundaries
        self._lower_bounds = self._new_bounds(lower_bounds, -1000)
        self._upper_bounds = self._new_bounds(upper_bounds, 1000)

        self._set_objective_functions()

    def _new_bounds(self, bounds, value):
        if bounds:
            return np.array(bounds)
        else:
            return np.zeros(self._dimensions) + value

    def _set_objective_functions(self):
        pos_func = lambda i: self._evaluate(i) + OFFSET
        neg_func = lambda i: -self._evaluate(i) + OFFSET * OFFSET

        if self._problem_type is MINIMIZE:
            self._fitness = neg_func
            self._cost = pos_func
        else:
            self._fitness = pos_func
            self._cost = neg_func
