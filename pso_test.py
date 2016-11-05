from evo.particles import ParticleSwarm
from evo.functions import rastrigin, ackley, sphere
from evo.plot import EvoPlot

if __name__ == '__main__':
    pso = ParticleSwarm()

    best = pso.optimize(function=rastrigin)

    plot = EvoPlot(pso.generations)

    plot.animate()
