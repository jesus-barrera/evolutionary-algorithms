import random

from evo import EvolutionaryAlgorithm
from tools import RandomSelector

class BasicBinaryGA(EvolutionaryAlgorithm):
    """A basic binary genetic algorithm."""

    def __init__(
            self,
            population_size=50,
            mutation_probability=0.01,
            num_elites=2,
            genelen=15):

        EvolutionaryAlgorithm.__init__(self, population_size, mutation_probability, num_elites)

        self.genelen = genelen
        self.genotype_size = 2**genelen

    def evolve(self, max_generations):
        # genes represent a variable value; as genes have a length of genelen, we
        # can only represent 2^genelen values in the variable's domain, thus the
        # resolution indicates the difference between each of these values.
        self.resolution = (float(self.domain.max - self.domain.min)
                           / (self.genotype_size - 1))

        self.init_population()

        results = []
        selector = RandomSelector()

        for generation in range(max_generations):
            self.sort_population()

            fittest = self.get_fenotypes(self.population[0])
            value = self.function(*fittest)

            results.append((fittest, value))

            # print generation best fit
            print '{}: f{} = {}'.format(generation, fittest, value)

            # preserve the best individuals
            children = self.population[:self.num_elites]

            selector.assign([(i, self.fitness(i)) for i in self.population])

            while len(children) < len(self.population):
                # selection
                parents = selector.sample(2)

                # individuals must be encoded to its binary representation as
                # required by the crossover and mutation operators
                encoded_parents = map(self.encode, parents)

                # crossover
                decendents = self.crossover(*encoded_parents)

                # mutation
                decendents = map(self.mutate, decendents)

                children.extend(map(self.decode, decendents))

            self.population = children

        return results

    def random_inidividual(self):
        x = random.randrange(self.genotype_size)
        y = random.randrange(self.genotype_size)

        return x, y

    def evaluate(self, individual):
        """Evaluate a solution in the objective function."""

        individual = self.get_fenotypes(individual)

        return self.function(*individual)

    def fenotype(self, genotype):
        """Maps a genotype to its corresponding fenotype."""

        return self.domain.min + genotype * self.resolution


    def get_fenotypes(self, individual):
        """Maps the individual's genotypes into fenotypes."""

        x, y = individual

        return self.fenotype(x), self.fenotype(y)

    def crossover(self, parent_a, parent_b):
        """Combines two individuals into two new individuals."""

        cross_point = random.randrange(1, len(parent_a))

        child_a = parent_a[:cross_point] + parent_b[cross_point:]
        child_b = parent_b[:cross_point] + parent_a[cross_point:]

        return child_a, child_b

    def mutate(self, individual):
        """Flips each bit of individual with a probability of mutation_probability."""

        mutated = list(individual)

        for index, bit in enumerate(individual):
            if random.random() < self.mutation_probability:
                if bit is '1':
                    mutated[index] = '0'
                else:
                    mutated[index] = '1'

        return ''.join(mutated)

    def encode(self, individual):
        """Encodes the individual into a binary secuence."""

        x, y = individual

        return self.gene_bits(x) + self.gene_bits(y)

    def decode(self, chromosome):
        """Decodes the binary secuence into a tuple of integer values."""

        x = self.gene_value(chromosome[:self.genelen])
        y = self.gene_value(chromosome[self.genelen:])

        return x, y

    def gene_bits(self, value):
        """Returns the binary representation of value."""

        return format(value, 'b').zfill(self.genelen)

    def gene_value(self, bits):
        """Returns the integer value represented by the binary string."""

        return int(bits, 2)
