from particle_swarm import ParticleSwarm
from test_functions import rastrigin, ackley, sphere
from evo import MAXIMIZE
from plot import EvoPlot

if __name__ == '__main__':
    pso = ParticleSwarm()

    results = pso.solve(function=ackley, domain=(-1000, 1000))

    plot = EvoPlot(results)

    plot.animate()
