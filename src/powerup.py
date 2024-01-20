import math

import pygame

from config import PROJECTILE_SPEED


class Powerup:
    def __init__(self, position, angle, shooter):
        self.position = list(position)
        self.angle = angle
        self._next_pos = self.get_next_position()
        self.radius = 2  # Size of the projectile
        self.shooter = shooter
        self.move_count = 0

    def get_next_position(self):
        self._next_pos = (
            self.position[0] + PROJECTILE_SPEED * math.sin(math.radians(self.angle)),
            self.position[1] - PROJECTILE_SPEED * math.cos(math.radians(self.angle))
        )
        return self._next_pos

    def move(self):
        self.position = self._next_pos
        self.move_count += PROJECTILE_SPEED

    def draw(self, window):
        pygame.draw.circle(window, (255, 255, 255), self.position, self.radius)

    def get_bounding_rect(self, pos=None):
        if pos is None:
            pos = self.position
        return pygame.Rect(pos[0] - self.radius, pos[1] - self.radius, self.radius * 2, self.radius * 2)

    def get_bounding_points(self):
        projectile_rect = self.get_bounding_rect()
        return [projectile_rect.topleft, projectile_rect.topright, projectile_rect.bottomright, projectile_rect.bottomleft]

    def bounce(self, wall):
        p = self
        x = self.position[0]
        y = self.position[1]
        wall_rect = wall.get_rect()
        wall_x1 = wall_rect.x
        wall_x2 = wall_rect.x + wall_rect.width
        wall_y1 = wall_rect.y
        wall_y2 = wall_rect.y + wall_rect.height

        if wall_y1 <= y <= wall_y2:
            p.angle = 360 - p.angle  # studs i X-led
        elif wall_x1 <= x < + wall_x2:
            p.angle = 180 - p.angle  # studs i Y-led
        else:
            p.angle = (p.angle + 180) % 306
