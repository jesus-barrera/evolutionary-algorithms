from evo.genetics import BasicBinaryGA
from evo.functions import rastrigin, ackley, sphere

if __name__ == '__main__':
    GA = BasicBinaryGA()

    results = GA.solve(function=rastrigin, domain=(-100, 100))

    file = open('results.txt', 'w')

    for generation, best_fitness in enumerate(results):
        file.write('{0}, {1:.5f}\n'.format(generation, best_fitness[1]))

    file.close()
