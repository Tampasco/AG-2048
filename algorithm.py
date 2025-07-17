import random

valid_moves = ['up', 'down', 'left', 'right']


def generate_individual(size):
    return [random.choice(valid_moves) for _ in range(size)]


def generate_population(population_size, individual_size):
    return [generate_individual(individual_size) for _ in range(population_size)]


