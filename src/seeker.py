import math

import pygame

from config import SEEKER_SPEED
from projectile import Projectile


class Seeker(Projectile):
    def __init__(self, position, angle, shooter, target):
        super().__init__(position, angle, shooter)
        self._next_pos = self._calculate_next_pos()
        self.move()
        self.radius = 2  # Size of the projectile
        self.target = target

    def get_next_position(self):
        return self._next_pos

    def _calculate_next_pos(self):
        return (
            self.position[0] + SEEKER_SPEED * math.sin(math.radians(self.angle)),
            self.position[1] - SEEKER_SPEED * math.cos(math.radians(self.angle))
        )

    def move(self):
        self.position = self._next_pos
        self.move_count += SEEKER_SPEED
        if self.move_count > 50:
            self.seek()
        self._next_pos = self._calculate_next_pos()

    def seek(self):
        target_angle = self.calculate_angle(self.position, self.target.get_center_pos())
        self.angle = self.adjust_bullet_angle(target_angle, 2)

    def adjust_bullet_angle(self, target_angle, adjustment_step=1):
        angle_diff = (target_angle - self.angle + 360) % 360

        if angle_diff <= 180:
            new_angle = self.angle + adjustment_step
        else:
            new_angle = self.angle - adjustment_step

        return new_angle % 360

    @staticmethod
    def calculate_angle(pos1, pos2):
        dx = pos2[0] - pos1[0]
        dy = pos1[1] - pos2[1]
        angle_radians = math.atan2(dy, dx)
        angle_degrees = math.degrees(angle_radians)
        return (90 - angle_degrees) % 360

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
