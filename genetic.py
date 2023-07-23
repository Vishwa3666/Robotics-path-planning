import pygame
import random
import math
import sys
# --- Genetic Algorithm Parameters ---
POPULATION_SIZE = 60
ELITISM_RATE = 0.2
MUTATION_RATE = 0.1
MAX_GENERATIONS = 5

# --- Environment Parameters ---
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
OBSTACLE_WIDTH = 40
OBSTACLE_COLOR = (255, 0, 0)
START_POSITION = (100, 100)
END_POSITION = (700, 500)
START_COLOR = (0, 255, 0)
END_COLOR = (0, 0, 255)

# --- Helper Functions ---
def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def check_collision(point, obstacles):
    for obstacle in obstacles:
        if calculate_distance(point, obstacle) < OBSTACLE_WIDTH / 2 + 10:
            return True
    return False

def generate_population(start, end, obstacles, num_points=7):
    population = []
    for i in range(POPULATION_SIZE):
        path = [start]
        for j in range(num_points - 2):
            point = (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT))
            while check_collision(point, obstacles):
                point = (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT))
            path.append(point)
        path.append(end)
        population.append(path)
    return population

def fitness(path):
    total_distance = 0
    for i in range(len(path) - 1):
        total_distance += calculate_distance(path[i], path[i + 1])
    return 1 / total_distance

def crossover(parent1, parent2):
    child = [parent1[0]]
    for i in range(1, len(parent1) - 1):
        if random.random() < 0.5:
            child.append(parent1[i])
        else:
            child.append(parent2[i])
    child.append(parent1[-1])
    return child

def mutate(path,obstacles):
    for i in range(1, len(path) - 1):
        if random.random() < MUTATION_RATE:
            point = (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT))
            while check_collision(point, obstacles):
                point = (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT))
            path[i] = point
    return path

def select_parents(population):
    population_size = len(population)
    fitness_scores = [fitness(path) for path in population]
    total_fitness = sum(fitness_scores)
    probabilities = [fitness_scores[i] / total_fitness for i in range(population_size)]
    cumulative_probabilities = [sum(probabilities[:i + 1]) for i in range(population_size)]
    elite_size = int(ELITISM_RATE * population_size)
    elite_indices = sorted(range(population_size), key=lambda i: fitness_scores[i], reverse=True)[:elite_size]
    non_elite_indices = [i for i in range(population_size) if i not in elite_indices]
    parents = [population[i] for i in elite_indices]
    for i in range(int((1 - ELITISM_RATE) * population_size)):
        r = random.random()
        for j in range(population_size - elite_size):
            if r <= cumulative_probabilities[non_elite_indices[j]]:
                parents.append(population[non_elite_indices[j]])
                break
    return parents


def evolve_population(population, obstacles):
    new_population = []
    elitism_size = int(ELITISM_RATE * len(population))
    elite_paths = sorted(population, key=fitness, reverse=True)[:elitism_size]
    new_population.extend(elite_paths)
    while len(new_population) < len(population):
        parents = select_parents(population)
        parent1, parent2 = parents[0], parents[1]
        child = crossover(parent1, parent2)
        child = mutate(child,obstacles)
        if not check_collision(child[-2], obstacles):
            new_population.append(child)
    return new_population

def draw_obstacles(obstacles, surface):
    for obstacle in obstacles:
        x, y = obstacle
        rect = pygame.Rect(x - OBSTACLE_WIDTH/2, y - OBSTACLE_WIDTH/2, OBSTACLE_WIDTH, OBSTACLE_WIDTH)
        pygame.draw.rect(surface, OBSTACLE_COLOR, rect)

def draw_path(path, surface):
    pygame.draw.lines(surface, (0, 0, 0), False, path, 2)
    font = pygame.font.Font(None, 20)
    for point in path:
        text = font.render(f"({point[0]}, {point[1]})", True, (0, 0, 0))
        surface.blit(text, point)

def draw_start_and_end(surface):
    pygame.draw.circle(surface, START_COLOR, START_POSITION, 10)
    pygame.draw.circle(surface, END_COLOR, END_POSITION, 10)

def draw_path_points(path, surface):
    for point in path:
        pygame.draw.circle(surface, (255, 0, 0), point, 5)

def main():
    pygame.init()
    surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    obstacles = [(300, 300), (200, 200), (400, 400), (500, 200), (600, 300)]
    population = generate_population(START_POSITION, END_POSITION, obstacles)

    for i in range(MAX_GENERATIONS):
        population = evolve_population(population, obstacles)
        surface.fill((255, 255, 255))
        draw_obstacles(obstacles, surface)
        draw_start_and_end(surface)
        best_path = sorted(population, key=fitness, reverse=True)[0]
        draw_path(best_path, surface)
        draw_path_points(best_path, surface) # Draw circles at each point in the path
        pygame.time.wait(1000)
        pygame.display.update()

if __name__ == '__main__':
    main()