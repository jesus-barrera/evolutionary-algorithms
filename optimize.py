from genetics import GeneticAlgorithm
from test_functions import rastrigin, ackley, sphere

if __name__ == '__main__':
    max_generations = 100
    population_size = 50

    domain = (-100, 100)

    GA = GeneticAlgorithm(rastrigin, domain)

    results = GA.optimize(population_size, max_generations)

    file = open('results.txt', 'w')

    for generation, best_fitness in enumerate(results):
        file.write('{0}, {1:.5f}\n'.format(generation, best_fitness[1]))

    file.close()
