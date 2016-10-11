import math

def sphere(x, y):
    return x**2 + y**2

def rastrigin(x, y):
    return 20 + x**2 - 10 * math.cos(math.pi * x) + y**2 - 10 * math.cos(2 * math.pi * y)

def ackley(x, y):
    return -20 * math.exp(-0.2 * math.sqrt(0.5 * (x**2 + y**2))) - math.exp(0.5 * (math.cos(2 * math.pi * x) + math.cos(2 * math.pi * y))) + 20 + math.exp(1)
