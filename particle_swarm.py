import random
import copy
import numpy as np

from evo import EvolutionaryAlgorithm as EA, Generation

class Particle:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

        self.set_best_position(position)

    def set_best_position(self, position):
        self.best_position = copy.copy(position)

class ParticleSwarm(EA):
    """Particle Swarm Optimization using gbest topology."""

    def __init__(
            self,
            population_size=100,
            num_elites=2,
            max_cognition_rate=2.05,
            max_social_rate=2.05):

        EA.__init__(self, population_size, 0, num_elites)

        self.max_cognition_rate = max_cognition_rate
        self.max_social_rate = max_social_rate

        self.generations = []

    def evolve(self, max_generations):
        self.init_population()

        max_velocity = (self.domain.max - self.domain.min) * 0.01

        for generation in range(max_generations):
            self.sort_population()

            self.save_generation()

            best_neighbor = self.population[0]

            elites = self.population[:self.num_elites]

            self.population = self.population[self.num_elites:]

            for particle in self.population:
                cognition_rate = self.learning_rate(self.max_cognition_rate)
                social_rate = self.learning_rate(self.max_social_rate)

                # update velocity
                particle.velocity += (social_rate
                                      * (best_neighbor.position - particle.position)
                                      + cognition_rate
                                      * (particle.best_position - particle.position))

                # velocity limiting
                magnitude = np.linalg.norm(particle.velocity)

                if magnitude > max_velocity:
                    particle.velocity = (particle.velocity / magnitude) * max_velocity

                # update particle position
                particle.position += particle.velocity

                # update best position
                if self.fitness(particle) > self.fitness(Particle(particle.best_position, 0)):
                    particle.set_best_position(particle.position)

            self.population.extend(elites)

        return self.generations

    def random_inidividual(self):
        position = np.array(EA.random_inidividual(self))
        velocity = np.zeros(len(self.dimensions))

        return Particle(position, velocity)

    def evaluate(self, particle):
        return EA.evaluate(self, particle.position)

    def learning_rate(self, max_value):
        return np.array([random.uniform(0, max_value) for d in self.dimensions])

    def save_generation(self):
        positions = [copy.copy(particle.position)
                     for particle in self.population]

        best = self.evaluate(self.population[0])

        self.generations.append(Generation(positions, best))
