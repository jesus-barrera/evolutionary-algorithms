import random

from evo import EvolutionaryAlgorithm as EA, Generation
from tools import RandomSelector

class BasicBinaryGA(EA):
    """A basic binary genetic algorithm."""

    def __init__(
            self,
            population_size=50,
            mutation_probability=0.01,
            num_elites=2,
            genelen=15):

        EA.__init__( self, population_size, mutation_probability, num_elites)

        self._genelen = genelen
        self._genotype_size = 2**genelen

    def _init_algorithm(self):
        # genes represent a variable value; as genes have a length of genelen, we
        # can only represent 2^genelen values in the variable's domain, thus the
        # resolution indicates the difference between each of these values.
        self._resolution = (float(self._domain.max - self._domain.min)
                           / (self._genotype_size - 1))

        self._init_population()

    def _evolve(self):
        selector = RandomSelector()

        selector.assign([(i, self._fitness(i)) for i in self._population])

        # preserve the best individuals
        children = self._pick_elites()

        while len(children) < self._population_size:
            # selection
            parents = selector.sample(2)

            # individuals must be encoded to its binary representation as
            # required by the crossover and mutation operators
            encoded_parents = map(self._encode, parents)

            # crossover
            decendents = self._crossover(*encoded_parents)

            # mutation
            decendents = map(self._mutate, decendents)

            children.extend(map(self._decode, decendents))

        self._population = children

    def _rand_individual(self):
        return [random.randrange(self._genotype_size)
                for d in range(self._dimensions)]

    def _best(self):
        self._get_fenotypes(self._population[0])

    def _get_generation(self):
        population = map(self._get_fenotypes, self._population)

        best = population[0]

        return Generation(population, (best, self._function(*best)))

    def _evaluate(self, individual):
        individual = self._get_fenotypes(individual)

        return self._function(*individual)

    def _fenotype(self, genotype):
        return self._domain.min + genotype * self._resolution

    def _get_fenotypes(self, individual):
        return map(self._fenotype, individual)

    def _crossover(self, parent_a, parent_b):
        cross_point = random.randrange(1, len(parent_a))

        child_a = parent_a[:cross_point] + parent_b[cross_point:]
        child_b = parent_b[:cross_point] + parent_a[cross_point:]

        return child_a, child_b

    def _mutate(self, individual):
        mutated = list(individual)

        for index, bit in enumerate(individual):
            if random.random() < self._mutation_probability:
                if bit is '1':
                    mutated[index] = '0'
                else:
                    mutated[index] = '1'

        return ''.join(mutated)

    def _encode(self, individual):
        return ''.join(map(self._gene_bits, individual))

    def _decode(self, chromosome):
        individual = []

        while chromosome:
            bits = chromosome[:self._genelen]
            value = self._gene_value(bits)
            individual.append(value)
            chromosome = chromosome[self._genelen:]

        return individual

    def _gene_bits(self, value):
        return format(value, 'b').zfill(self._genelen)

    def _gene_value(self, bits):
        return int(bits, 2)
