import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

class EvoPlot():
    def __init__(self, generations):
        self.generations = generations

        # population plot
        self.population_fig = plt.figure()

        self.population_fig.add_subplot(1, 1, 1)

        plt.xlabel('x')
        plt.ylabel('y')

        # calculate axis limits
        min_x = 0
        max_x = 0

        min_y = 0
        max_y = 0

        for population in [i.population for i in generations]:
            for x, y in population:
                min_x = min(min_x, x)
                max_x = max(max_x, x)

                min_y = min(min_y, y)
                max_y = max(max_y, y)

        plt.xlim(min_x, max_x)
        plt.ylim(min_y, max_y)

        self.population_line, = plt.plot([], [], 'bo')

        self.anim = animation.FuncAnimation(
                                            self.population_fig,
                                            self.update,
                                            len(generations),
                                            self.init,
                                            interval=50,
                                            blit=True)

        self.population_fig.canvas.mpl_connect('key_press_event', self.on_press)

        self.frame = 0
        self.pause = False

        # function plot
        function_data = [generation.best[1] for generation in generations]

        self.function_fig = plt.figure()
        self.function_fig.add_subplot(1, 1, 1)

        plt.xlabel('Generacion')
        plt.ylabel('Objetivo')

        plt.xlim(0, len(generations))
        plt.ylim(0, max(function_data))

        self.function_line, = plt.plot(function_data, 'g--')

    def init(self):
        self.population_line.set_data([[], []])

        return self.population_line,

    def update(self, num):
        self.frame = num
        self.update_population(num)

        return self.population_line,

    def update_population(self, num):
        population = self.generations[num].population

        x_values = []
        y_values = []

        for x, y in population:
            x_values.append(x)
            y_values.append(y)

        self.population_line.set_data(x_values, y_values)

    def on_press(self, event):
        if event.key == 'e':
            self.toggle_pause()
        elif self.pause and event.key in ('q', 'w'):
            if event.key == 'q':
                frame = max(self.frame - 1, 0)
            else:
                frame = min(self.frame + 1, len(self.generations) - 1)

            self.update(frame)
            self.population_fig.canvas.draw()

    def toggle_pause(self):
        self.pause = not self.pause

        if self.pause:
            self.anim.event_source.stop()
        else:
            self.anim.event_source.start()

    def animate(self):
        plt.show()
