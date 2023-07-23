import pygame
import random
import math
#from testing import p
from queue import PriorityQueue
#paths=p()
# Define window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Define obstacle dimensions
OBSTACLE_WIDTH = 40

# Define obstacle positions
obstacles = [(300, 300), (200, 200), (400, 400), (500, 200), (600, 300)]

# Define start and end points
paths = [[(100, 100), (158, 81), (210, 259), (409, 324), (516, 327), (700, 500)]]

# Define Pygame colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()

# Create Pygame window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# Define function to check if a point collides with an obstacle
def collides_with_obstacle(point):
    for obstacle in obstacles:
        rect = pygame.Rect(obstacle[0], obstacle[1], OBSTACLE_WIDTH, OBSTACLE_WIDTH)
        if rect.collidepoint(point):
            #print("collides",point)
            return True
    return False

# Define function to calculate distance between two points
def distance(point1, point2):
    return ((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2) ** 0.5

# Define A* pathfinding function
def a_star(start, end):
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: distance(start, end)}

    while not open_set.empty():
        current = open_set.get()[1]

        if current == end:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                neighbor = (current[0] + i, current[1] + j)
                tentative_g_score = g_score[current] + distance(current, neighbor)
                if collides_with_obstacle(neighbor):
                    continue
                straight_line_distance = distance(neighbor, end)
                weighted_distance = 0.0063 * straight_line_distance + 0.002 * tentative_g_score
                f_score[neighbor] = weighted_distance
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    open_set.put((f_score[neighbor], neighbor))

    return None

# Define Ramer-Douglas-Peucker algorithm for path simplification
def simplify_path(points, tolerance=210):
    # Find the point with the maximum distance
    dmax = 0
    index = 0
    end = len(points) - 1
    for i in range(1, end):
        d = calculate_distance(points[i], (points[0][0], points[0][1]))
        if d > dmax:
            index = i
            dmax = d

    # If max distance is greater than tolerance, recursively simplify
    if dmax > tolerance:
        # Recursive call to simplify the path
        left = simplify_path(points[:index+1], tolerance)
        right = simplify_path(points[index:], tolerance)

        # Combine the simplified paths
        return left[:-1] + right
    else:
        # If max distance is less than tolerance, return the endpoints
        return [points[0], points[end]]

# Loop over each path
for path in paths:
    # Use A* to find path
    new_path = []
    for i in range(len(path) - 1):
        segment = a_star(path[i], path[i + 1])
        if segment:
            new_path.extend(segment[1:])  # add all points except the first one (to avoid duplicates)
    new_path.insert(0, path[0])  # add the first point of the original path
    path = new_path

    # Simplify the path
    path = simplify_path(path)

    # Print the path
    print(path)

    # Draw path and obstacles
    screen.fill(WHITE)
    pygame.draw.lines(screen, BLACK, False, path, 5)
    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, (obstacle[0], obstacle[1], OBSTACLE_WIDTH, OBSTACLE_WIDTH))

    # Update Pygame display
    pygame.display.update()
    for i in range(len(path)-1):
        best_path_length = sum([calculate_distance(path[i], path[i + 1]) for i in range(len(path) - 1)])
    print(best_path_length)
    # Run Pygame event loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


# Quit Pygame
pygame.quit()
