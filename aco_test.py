from evo.ants import ContinuousACO
from evo.functions import rastrigin, ackley, sphere

if __name__ == '__main__':
    aco = ContinuousACO()

    aco.solve(function=rastrigin, domain=(-100, 100))
