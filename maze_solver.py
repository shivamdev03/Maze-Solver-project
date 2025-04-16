import pygame
import sys
from collections import deque

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver with BFS")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Maze Setup
rows, cols = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE
maze = [[0 for _ in range(cols)] for _ in range(rows)]

# Start and End Points
start = (0, 0)
end = (rows - 1, cols - 1)

# BFS Algorithm
def bfs(maze, start, end):
    queue = deque([start])
    visited = set()
    visited.add(start)
    parent = {start: None}

    while queue:
        current = queue.popleft()
        if current == end:
            break

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r, c = current[0] + dr, current[1] + dc
            if 0 <= r < rows and 0 <= c < cols and maze[r][c] == 0 and (r, c) not in visited:
                queue.append((r, c))
                visited.add((r, c))
                parent[(r, c)] = current

    # Reconstruct Path
    path = []
    current = end
    while current:
        path.append(current)
        current = parent.get(current)
    path.reverse()

    return (path if path and path[-1] == end else None), visited

# Drawing Functions
def draw_grid():
    for r in range(rows):
        for c in range(cols):
            rect = pygame.Rect(c * GRID_SIZE, r * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            if maze[r][c] == 1:
                pygame.draw.rect(screen, BLACK, rect)
            pygame.draw.rect(screen, WHITE, rect, 1)

def draw_maze(path, visited):
    for r, c in visited:
        pygame.draw.rect(screen, BLUE, (c * GRID_SIZE, r * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    if path:
        for r, c in path:
            pygame.draw.rect(screen, GREEN, (c * GRID_SIZE, r * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Start and End Points
    pygame.draw.rect(screen, RED, (start[1] * GRID_SIZE, start[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(screen, YELLOW, (end[1] * GRID_SIZE, end[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Main Loop
clock = pygame.time.Clock()
running = True
solving = False
path, visited = [], set()

while running:
    screen.fill(WHITE)
    draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mouse Click to Add/Remove Walls
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            col, row = x // GRID_SIZE, y // GRID_SIZE
            if (row, col) != start and (row, col) != end:
                maze[row][col] = 1 - maze[row][col]  # Toggle wall

        # Keyboard Controls for Start/End Movement and Actions
        if event.type == pygame.KEYDOWN:
            if not solving:
                # Move Start (WASD)
                if event.key == pygame.K_w and start[0] > 0:
                    start = (start[0] - 1, start[1])
                if event.key == pygame.K_s and start[0] < rows - 1:
                    start = (start[0] + 1, start[1])
                if event.key == pygame.K_a and start[1] > 0:
                    start = (start[0], start[1] - 1)
                if event.key == pygame.K_d and start[1] < cols - 1:
                    start = (start[0], start[1] + 1)

                # Move End (Arrow Keys)
                if event.key == pygame.K_UP and end[0] > 0:
                    end = (end[0] - 1, end[1])
                if event.key == pygame.K_DOWN and end[0] < rows - 1:
                    end = (end[0] + 1, end[1])
                if event.key == pygame.K_LEFT and end[1] > 0:
                    end = (end[0], end[1] - 1)
                if event.key == pygame.K_RIGHT and end[1] < cols - 1:
                    end = (end[0], end[1] + 1)

            # Start Solving
            if event.key == pygame.K_SPACE:
                solving = True
                path, visited = bfs(maze, start, end)

            # Reset Maze
            if event.key == pygame.K_r:
                maze = [[0 for _ in range(cols)] for _ in range(rows)]
                solving = False
                path, visited = [], set()

    if solving:
        draw_maze(path, visited)
    else:
        draw_maze([], set())

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
sys.exit()
