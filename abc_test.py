from evo.bees import ArtificialBeeColony
from evo.functions import rastrigin, ackley, sphere
from evo.plot import EvoPlot

if __name__ == '__main__':
    abc = ArtificialBeeColony()

    best = abc.optimize(
                function=ackley,
                lower_bounds=[-50, -50],
                upper_bounds=[50, 50])

    plot = EvoPlot(abc.generations)

    plot.animate()
