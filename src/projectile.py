import math

import pygame

from config import PROJECTILE_SPEED, PROJECTILE_MAX_MOVE


class Projectile:
    def __init__(self, position, angle, shooter):
        self.position = list(position)
        self.angle = angle
        self.shooter = shooter
        self.move_count = 0

    def get_bounding_rect(self):
        raise NotImplementedError("Implemented in subclass")

    def get_bounding_points(self):
        projectile_rect = self.get_bounding_rect()
        return [projectile_rect.topleft, projectile_rect.topright, projectile_rect.bottomright, projectile_rect.bottomleft]

    def bounce(self, wall):
        p = self
        x = p.position[0]
        y = p.position[1]
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
            p.angle = (p.angle + 180) % 360

        self._next_pos = self.position

    def is_dead(self):
        return self.move_count > PROJECTILE_MAX_MOVE
