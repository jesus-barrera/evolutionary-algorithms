from evo.genetics import BasicBinaryGA
from evo.functions import rastrigin, ackley, sphere
from evo.plot import EvoPlot

if __name__ == '__main__':
    ga = BasicBinaryGA()

    best = ga.optimize(function=rastrigin)

    plot = EvoPlot(ga.generations)

    plot.animate()
