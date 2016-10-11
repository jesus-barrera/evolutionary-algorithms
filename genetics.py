import random

MINIMIZE = 0
MAXIMIZE = 1

'''
A basic binary genetic algorithm.
'''
class GeneticAlgorithm:
    mutation_probability = 0.01
    genelen = 15
    fitness_offset = 10000
    problem_type = MINIMIZE

    def __init__(self, function, domain):
        self.population = []
        self.fitness_list = []
        self.fitness_sum = 0

        # problem bounaries
        self.set_bounds(domain)
        self.function = function

    def set_bounds(self, domain):
        self.domain = domain

        # genes represent a variable value; as genes have a length of genelen, we
        # can only represent 2^genelen values in the variable's domain, thus the
        # resolution indicates the difference between each of these values.
        self.resolution = float(domain[1] - domain[0]) / (2**self.genelen - 1)

    def optimize(self, population_size, max_generations):
        # set random population
        self.init_population(population_size)

        results = []

        for generation in range(max_generations):
            self.calculate_fitness()

            # evaluate current generation
            fittest, value = self.evaluate_fittest()
            results.append((fittest, value)) # save result

            print '{}:f{} = {}'.format(generation, fittest, value) # print best fit

            children = []
            while len(children) < len(self.population):
                # selection
                parents = self.select_mates()

                # individuals must be encoded to its binary representation as
                # required by the crossover and mutation operators
                encoded_parents = map(self.encode, parents)

                # crossover
                decendents = self.crossover(*encoded_parents)

                # mutation
                decendents = map(self.mutate, decendents)

                decendents = map(self.decode, decendents)

                # convenient preservation of the parents
                if (self.fitness(decendents[0]) >= self.fitness(parents[0])):
                    children.append(decendents[0])

                if (self.fitness(decendents[1]) >= self.fitness(parents[1])):
                    children.append(decendents[1])

            self.population = children

        return results

    # Initialize population with random individuals.
    def init_population(self, size):
        self.population = []

        genotype_size = 2**self.genelen

        for i in range(size):
            x = random.randrange(genotype_size)
            y = random.randrange(genotype_size)

            self.population.append((x, y))

    # Evaluates the best individual of the current generation.
    def evaluate_fittest(self):
        fittest, fitness = self.get_fittest()

        fittest = self.get_fenotypes(fittest)
        value = self.function(*fittest)

        return fittest, value

    # Calculates the fitness for each individual in population.
    def calculate_fitness(self):
        self.fitness_list = map(self.fitness, self.population)
        self.fitness_sum = sum(self.fitness_list) # save the sum for later use

    # Returns the individual's fitness. It is calculated by simply evaluating the
    # function with the individual's fenotypes. If the problem is a minimization
    # problem the negative of the function is used. An arbitrary offset is added
    # to the result so the fitness is always greater than 0.
    def fitness(self, individual):
        x, y = self.get_fenotypes(individual)

        if (self.problem_type is MINIMIZE):
            return -self.function(x, y) + self.fitness_offset
        else:
            return self.function(x, y) + self.fitness_offset

    # Maps a genotype to its corresponding fenotype; this is the actual value
    # of a problem variable.
    def fenotype(self, genotype):
        return self.domain[0] + genotype * self.resolution

    # Maps the individual's genotypes into fenotypes.
    def get_fenotypes(self, individual):
        x, y = individual

        return self.fenotype(x), self.fenotype(y)

    # Finds the fittest individual in population; returns a tuple containing the
    # fittest individual and it's fitness.
    def get_fittest(self):
        index, fitness = max(enumerate(self.fitness_list), key=lambda item: item[1])

        return self.population[index], fitness

    # Probabilisticaly selects two individuals.
    def select_mates(self):
        first = self.select()
        second = self.select()

        # make sure to select diferent individuals
        while second is first: second = self.select()

        return first, second

    # Selects one individual from propulation using the roulette aproach.
    def select(self):
        i = 0
        rand = random.uniform(0, self.fitness_sum)
        accumulator = self.fitness_list[i]

        while accumulator < rand:
            i += 1
            accumulator += self.fitness_list[i]

        return self.population[i]

    # Combines two individuals into two new individuals
    def crossover(self, parent_a, parent_b):
        cross_point = random.randrange(1, len(parent_a))

        child_a = parent_a[:cross_point] + parent_b[cross_point:]
        child_b = parent_b[:cross_point] + parent_a[cross_point:]

        return child_a, child_b

    # Flips each bit of individual with a probability of mutation_probability.
    def mutate(self, individual):
        mutated = list(individual)

        for index, bit in enumerate(individual):
            if random.random() < self.mutation_probability:
                if bit is '1':
                    mutated[index] = '0'
                else:
                    mutated[index] = '1'

        return ''.join(mutated)

    # Encodes the individual into a binary secuence.
    def encode(self, individual):
        x, y = individual

        return self.gene_bits(x) + self.gene_bits(y)

    # Decodes the binary secuence into a tuple of integer values.
    def decode(self, chromosome):
        x = self.gene_value(chromosome[:self.genelen])
        y = self.gene_value(chromosome[self.genelen:])

        return x, y

    # Returns a binary representation of value; the argument value must fit in a
    # string of length genelen.
    def gene_bits(self, value):
        return format(value, 'b').zfill(self.genelen)

    # Returns the integer value represented by the binary string.
    def gene_value(self, bits):
        return int(bits, 2)
