import math

import pygame

from config import PROJECTILE_SPEED
from projectile import Projectile


class Bullet(Projectile):
    def __init__(self, position, angle, shooter):
        super().__init__(position, angle, shooter)
        self._next_pos = self._calculate_next_pos()
        self.move()
        self.radius = 2  # Size of the projectile

    def get_next_position(self):
        return self._next_pos

    def _calculate_next_pos(self):
        return (
            self.position[0] + PROJECTILE_SPEED * math.sin(math.radians(self.angle)),
            self.position[1] - PROJECTILE_SPEED * math.cos(math.radians(self.angle))
        )

    def move(self):
        self.position = self._next_pos
        self.move_count += PROJECTILE_SPEED
        self._next_pos = self._calculate_next_pos()

    def draw(self, window):
        pygame.draw.circle(window, (255, 255, 255), self.position, self.radius)

    def draw_hitbox(self, window):
        pygame.draw.rect(window, (0, 0, 200), self.get_bounding_rect())
    def get_bounding_rect(self, pos=None):
        if pos is None:
            pos = self.position
        return pygame.Rect(pos[0] - self.radius, pos[1] - self.radius, self.radius * 2, self.radius * 2)
