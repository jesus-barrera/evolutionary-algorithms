from evo.de import DifferentialEvolution
from evo.functions import rastrigin, ackley, sphere
from evo.plot import EvoPlot

if __name__ == '__main__':
    de = DifferentialEvolution()

    best = de.optimize(function=rastrigin)

    plot = EvoPlot(de.generations)

    plot.animate()
