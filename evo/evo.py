import abc
import random
import copy
import numpy as np
from collections import namedtuple
from tools import Interval

Generation = namedtuple('Generation', ['population', 'best'])

# TODO: implement a _normalize abstract method and use it in evaluate, _get_generation
# and _best, so subclases dont have to override these methods, but only implement
# a the _normalize one.
class EvolutionaryAlgorithm:
    __metaclass__ = abc.ABCMeta

    def __init__(
            self,
            population_size,
            mutation_probability,
            num_elites):

        # these are some tipical EA parameters; may not be used by all EAs.
        self._population_size = population_size
        self._mutation_probability = mutation_probability
        self._num_elites = num_elites

        self._population = []

    def optimize(
            self,
            function,
            domain=(-100, 100),
            lower_bounds=[],
            upper_bounds=[],
            problem_type='min',
            max_generations=100):
        """Optimize a function using evolutionary techniques.

        Arguments:
        function -- function to optimize, also known as objective function
        lower_bounds -- lower bounds for each solution parameter
        upper_bounds -- upper bounds for each solution parameter
        problem_type -- one of 'max' or 'min' strings. Tells if maximize or
                        minimize the objective function (default 'min')
        max_generations -- number of generations to evolve the solution (default 100)
        """

        # domain is used for backwards compatibility. Algoriths must use
        # lower_bounds and upper_bounds instead
        self._domain = Interval(*domain)

        self._set_problem(function, lower_bounds, upper_bounds, problem_type)
        self._init_algorithm()

        # stores the results of each generation; this data is intented for analysis
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
        population = copy.deepcopy(self._population)

        best = population[0]

        return Generation(population, (best, self._function(*best)))

    def _rand_individual(self):
        params = np.zeros(self._dimensions)

        for i in range(self._dimensions):
            params[i] = random.uniform(
                            self._lower_bounds[i],
                            self._upper_bounds[i])

        return params

    def _sort_population(self):
        is_maximize = self._problem_type == 'max'

        self._population.sort(key=self._evaluate, reverse=is_maximize)

    def _best(self):
        # as the population is sorted before each generation, we expect the first
        # individual to be the best
        return self._population[0]

    def _evaluate(self, individual):
        return self._function(*individual)

    def _pick_elites(self):
        # asumes the population is sorted by best; get the first (so best) _num_elites
        # individuals
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

        self._set_objective_function()

    def _new_bounds(self, bounds, value):
        if bounds:
            return np.array(bounds)
        else:
            return np.zeros(self._dimensions) + value

    def _fitness(self, individual):
        val = self._objective(individual)

        if val >= 0:
            return 10000 / (1 + val)
        else:
            return 10000 + abs(val)

    def _cost(self, individual):
        val = self._objective(individual)

        if val >= 0:
            return 10000 + val
        else:
            return 10000 / (1 + abs(val))

    def _set_objective_function(self):
        # the fitness and cost methods defined above are designed to minimize a
        # function. If the problem is a maximization problem, it must be converted
        # into a minimization problem. This is done by simply minimizing -f(x)
        if self._problem_type is 'max':
            self._objective = lambda individual: self._evaluate(individual) * -1
        else:
            self._objective = self._evaluate
