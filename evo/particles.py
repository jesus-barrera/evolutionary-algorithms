import random
import copy
import numpy as np

from evo import EvolutionaryAlgorithm as EA, Generation

class Particle:
    def __init__(self, position):
        self.position = position
        self.velocity = np.zeros(len(position))

        self.set_best_position(position)

    def set_best_position(self, position):
        self.best_position = copy.copy(position)

class ParticleSwarm(EA):
    """Optimize a function using the Particle Swarm Optimization approach.

    Implements a gbest (global best) topology.
    """

    def __init__(
            self,
            population_size=100,
            num_elites=2,
            max_cognition_rate=2.05,
            max_social_rate=2.05,
            max_velocity=20):

        EA.__init__(self, population_size, 0, num_elites)

        self._max_cognition_rate = max_cognition_rate
        self._max_social_rate = max_social_rate
        self._max_velocity = max_velocity

    def _evolve(self):
        best_neighbor = EA._best(self)
        elites = self._pick_elites()

        for particle in self._population:
            cognition_rate = np.random.uniform(0, self._max_cognition_rate)
            social_rate = np.random.uniform(0, self._max_social_rate)

            # update velocity
            particle.velocity += (social_rate
                                  * (best_neighbor.position - particle.position)
                                  + cognition_rate
                                  * (particle.best_position - particle.position))

            # velocity limiting
            magnitude = np.linalg.norm(particle.velocity)

            if magnitude > self._max_velocity:
                particle.velocity = (particle.velocity / magnitude
                                     * self._max_velocity)

            # update particle position
            particle.position += particle.velocity

            # update best position
            if self._fitness(particle) > self._fitness(Particle(particle.best_position)):
                particle.set_best_position(particle.position)

        self._population.extend(elites)

    def _rand_individual(self):
        position = EA._rand_individual(self)

        return Particle(position)

    def _evaluate(self, particle):
        return self._function(*particle.position)

    def _best(self):
        best = EA._best(self)

        return copy.copy(best.position)

    def _get_generation(self):
        positions = [copy.copy(particle.position)
                     for particle in self._population]

        best = positions[0], self._function(*positions[0])

        return Generation(positions, best)
