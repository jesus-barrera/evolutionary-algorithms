from evo.bacterium import BacterialForaging
from evo.functions import rastrigin, ackley, sphere
from evo.plot import EvoPlot

if __name__ == '__main__':
    bfoa = BacterialForaging()

    best = bfoa.optimize(
                function=rastrigin,
                lower_bounds=[-50, -50],
                upper_bounds=[50, 50])

    print best

    plot = EvoPlot(bfoa.generations)

    plot.animate()
