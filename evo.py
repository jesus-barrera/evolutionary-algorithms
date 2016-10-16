import abc
import random

from tools import Interval

MINIMIZE = 0
MAXIMIZE = 1

OFFSET = 1000

class EvolutionaryAlgorithm:
    """Evolutionary Algorithm for solving optimization problems."""

    __metaclass__ = abc.ABCMeta

    def __init__(
            self,
            population_size,
            mutation_probability,
            num_elites):

        self.population_size = population_size
        self.mutation_probability = mutation_probability
        self.num_elites = num_elites

        self.population = []

    @abc.abstractmethod
    def evolve(self, max_generations):
        """Implements an evolutionary algorithm."""
        return

    def solve(self, function, domain, problem_type=MINIMIZE, max_generations=100):
        """Solves an optimization problem using an evolutionary algorithm.

        Arguments:
        function -- objective function
        domain -- problem domain
        problem_type -- tells if MINIMIZE or MAXIMIZE the objective function (default MINIMIZE)
        max_generations -- number of generations to evolve the solution (default 100)
        """

        # set problem specifications
        self.function = function
        self.domain = Interval(*domain)
        self.problem_type = problem_type

        self.set_objective_functions()

        # the number of arguments the function takes tells the dimensions of the
        # problem
        self.dimensions = range(function.func_code.co_argcount)

        # run the algorithm to find the solution
        return self.evolve(max_generations)

    def random_inidividual(self):
        """Forms a random candidate solution.

        A candidate solution is a list of elements where each element represents
        a solution parameter.
        """

        return [random.uniform(self.domain.min, self.domain.max)
                for dimension in self.dimensions]

    def init_population(self):
        """Initialize the population with random individuals."""

        self.population = [self.random_inidividual()
                           for i in range(self.population_size)]

    def set_objective_functions(self):
        # two possible representations of the problem
        pos_func = lambda i: self.evaluate(i) + OFFSET
        neg_func = lambda i: -self.evaluate(i) + OFFSET * OFFSET

        if self.problem_type is MINIMIZE:
            # minimize f(x)
            self.fitness = neg_func # fitness(x) = -f(x) + k
            self.cost = pos_func    # cost(x) = f(x) + k

        else:
            # maximize f(x)
            self.fitness = pos_func # fitness(x) = f(x) + k
            self.cost = neg_func    # cost(x) = -f(x) + k

    def evaluate(self, individual):
        """Evaluates a candidate solution."""

        return self.function(*individual)

    def sort_population(self):
        """Sorts the population by the best solution."""

        is_maximize = self.problem_type == MAXIMIZE

        self.population.sort(key=self.evaluate, reverse=is_maximize)
