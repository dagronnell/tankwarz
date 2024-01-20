import math
import random

import pygame

from config import WINDOW_WIDTH, WINDOW_HEIGHT

THICKNESS = 10


class Wall:
    def __init__(self, position, size, color=(128, 128, 128)):
        self.position = position
        self.size = size
        self.rect = pygame.Rect(position, size)
        self.color = color

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

    def get_rect(self):
        return self.rect

    def get_bounding_points(self):
        rect = self.get_rect()
        return [rect.topleft, rect.topright, rect.bottomright, rect.bottomleft]

    def is_vertical(self):
        return self.size[1] > self.size[0]


def skip(b):
    return not b and random.randint(0, 100) > 40


def create_walls():
    width = 8
    height = 6
    seed = random.randint(0, 0xFFFF_FFFF)
    random.seed(seed)
    grid = [[0 for _ in range(width)] for _ in range(height)]

    # Riktningar
    N, S, E, W = 1, 2, 4, 8
    DX = {E: 1, W: -1, N: 0, S: 0}
    DY = {E: 0, W: 0, N: -1, S: 1}
    OPPOSITE = {E: W, W: E, N: S, S: N}

    # Aldous-Broder algoritm för att generera banan
    x, y = random.randint(0, width-1), random.randint(0, height-1)
    remaining = width * height - 1

    while remaining > 0:
        for direction in random.sample([N, S, E, W], 4):
            nx, ny = x + DX[direction], y + DY[direction]
            if 0 <= nx < width and 0 <= ny < height:
                if grid[ny][nx] == 0:
                    grid[y][x] |= direction
                    grid[ny][nx] |= OPPOSITE[direction]
                    remaining -= 1

                x, y = nx, ny
                break

    cell_size = 100
    wall_thickness = 15
    walls = []
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            top_left_x = x * cell_size
            top_left_y = y * cell_size

            if cell & E == 0 and not skip(x == width-1 or y == height-1):
                walls.append(Wall((top_left_x + cell_size - wall_thickness, top_left_y), (wall_thickness, cell_size)))

            if cell & S == 0 and not skip(x == width-1 or y == height-1):
                walls.append(Wall((top_left_x, top_left_y + cell_size - wall_thickness), (cell_size, wall_thickness)))

            if y == 0:
                walls.append(Wall((top_left_x, top_left_y), (cell_size, wall_thickness)))

            if x == 0:
                walls.append(Wall((top_left_x, top_left_y), (wall_thickness, cell_size)))

    return walls
