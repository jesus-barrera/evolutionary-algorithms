import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

class EvoPlot():
    def __init__(self, generations):
        self.generations = generations

        self.figure = plt.figure()

        # create subplots
        self.figure.add_axes([0.3, 0.55, 0.4, 0.4])

        plt.xlabel('x')
        plt.ylabel('y')
        plt.xlim(-1000, 1000)
        plt.ylim(-1000, 1000)

        self.population_line, = plt.plot([], [], 'bo')

        self.figure.add_axes([0.3, 0.07, 0.4, 0.4])
        plt.xlabel('Generacion')
        plt.ylabel('f(x)')
        plt.xlim(0, len(generations))
        plt.ylim(0, max([generation.best for generation in generations]))

        self.generation_line, = plt.plot([], [], 'r--')

        self.anim = animation.FuncAnimation(
                                            self.figure,
                                            self.update,
                                            len(generations),
                                            self.init,
                                            interval=50,
                                            blit=True)

        self.pause = False

        self.figure.canvas.mpl_connect('key_press_event', self.on_press)


    def init(self):
        self.population_line.set_data([[], []])
        self.generation_line.set_data([[], []])

        return self.generation_line, self.population_line

    def update(self, num):
        print num

        self.update_population(num)
        self.update_generation(num)

        return self.generation_line, self.population_line

    def update_population(self, num):
        population = self.generations[num].population

        x_values = []
        y_values = []

        for x, y in population:
            x_values.append(x)
            y_values.append(y)

        self.population_line.set_data(x_values, y_values)

    def update_generation(self, num):
        num += 1

        bests = [generation.best
                 for generation in self.generations[:num]]

        self.generation_line.set_data(range(num), bests)

    def on_press(self, event):
        if event.key == 'p':
            self.toggle_pause()

    def toggle_pause(self):
        self.pause = not self.pause

        if self.pause:
            self.anim.event_source.stop()
        else:
            self.anim.event_source.start()

    def animate(self):
        plt.show()
