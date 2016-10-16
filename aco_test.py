from ant_colony import ContinuousACO
from test_functions import rastrigin, ackley, sphere

if __name__ == '__main__':
    aco = ContinuousACO()

    aco.solve(function=rastrigin, domain=(-100, 100))
