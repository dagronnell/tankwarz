import math
import pygame

from collision import polygons_collide
from config import TANK_SPEED, TANK_ROTATION_SPEED
from projectile import Projectile
from scene import place_tank
from seeker import Seeker
from bullet import Bullet


class Tank:
    def __init__(self, image_path, walls, angle=0):
        self.original_image = pygame.image.load(image_path)
        self.image = self.original_image
        self.size = self.original_image.get_size()
        self.draw_position = None
        self.angle = angle  # Angle in degrees
        self.walls = walls
        self.other_tank = None
        self.last_angle = None
        self.last_shot_time = 0
        self.shoot_cooldown = 200  # milliseconds
        self.projectile_count = 0
        self.score = 0
        self.image_center = self.original_image.get_rect().center

    def set_other_tank(self, tank):
        self.other_tank = tank

    def update_draw_position(self, new_pos):
        self.draw_position = new_pos

    def draw(self, window):
        if self.angle != self.last_angle:
            self.image = pygame.transform.rotate(self.original_image, -self.angle)
            self.last_angle = self.angle

        rect = self.image.get_rect(center=(self.draw_position[0] + self.size[0] // 2,
                                           self.draw_position[1] + self.size[1] // 2))
        window.blit(self.image, rect.topleft)

    def _get_pos(self, offset_x, offset_y):
        # Rotate the offset by the tank's current angle to get the correct position
        rad_angle = math.radians(self.angle)
        rotated_offset_x = offset_x * math.cos(rad_angle) - offset_y * math.sin(rad_angle)
        rotated_offset_y = offset_x * math.sin(rad_angle) + offset_y * math.cos(rad_angle)

        return (
            self.draw_position[0] + self.size[0] / 2 + rotated_offset_x,
            self.draw_position[1] + self.size[1] / 2 + rotated_offset_y
        )

    def get_cannon_position(self):
        return self._get_pos(1, -29)

    def get_center_pos(self):
        return self._get_pos(1, 0)

    def get_next_position(self, direction):
        return (
            self.draw_position[0] + direction * TANK_SPEED * math.sin(math.radians(self.angle)),
            self.draw_position[1] - direction * TANK_SPEED * math.cos(math.radians(self.angle))
        )

    def move(self, direction):
        next_pos = self.get_next_position(direction)
        hit_wall = False
        tank_bounding_rect = self.get_bounding_rect(next_pos)
        for wall in self.walls:
            if wall.get_rect().colliderect(tank_bounding_rect):
                if polygons_collide(self.get_bounding_points(next_pos), wall.get_bounding_points()):
                    hit_wall = True
                    break
        hit_other_tank = False
        if not hit_wall:
            if self.other_tank.get_bounding_rect().colliderect(tank_bounding_rect):
                if polygons_collide(self.get_bounding_points(next_pos), self.other_tank.get_bounding_points()):
                    hit_other_tank = True
        if not hit_wall and not hit_other_tank:
            self.update_draw_position(next_pos)

    def rotate(self, direction):
        old_angle = self.angle
        self.angle -= direction * TANK_ROTATION_SPEED
        self.angle = self.angle % 360

        player_tank_bounding_rect = self.get_bounding_rect()
        for wall in self.walls:
            if wall.get_rect().colliderect(player_tank_bounding_rect):
                if polygons_collide(wall.get_bounding_points(), self.get_bounding_points()):
                    self.angle = old_angle
                    return

        if player_tank_bounding_rect.colliderect(self.other_tank.get_bounding_rect()):
            self.angle = old_angle
            return

    def shoot(self, current_time, projectile_type):
        if current_time - self.last_shot_time >= self.shoot_cooldown:
            self.last_shot_time = current_time
            cannon_pos = self.get_cannon_position()
            if projectile_type is Bullet:
                return Bullet(cannon_pos, self.angle, self)
            elif projectile_type is Seeker:
                return Seeker(cannon_pos, self.angle, self, self.other_tank)

        return None

    def get_bounding_points(self, position=None):
        if position is None:
            position = self.draw_position
        # Calculate the four corners of the tank based on the center and angle
        w, h = self.size
        offset_x = 0
        offset_y = 0
        cx, cy = position[0] + w // 2, position[1] + h // 2

        # Define the corners relative to the center
        corners = [
            (-w // 2 + offset_x, -h // 2 + offset_y),
            (w // 2 - offset_x, -h // 2 + offset_y),
            (w // 2 - offset_x, h // 2 - offset_y),
            (-w // 2 + offset_x, h // 2 - offset_y)
        ]

        points = []
        for corner in corners:
            # Rotate each corner around the center of the tank
            rad_angle = math.radians(self.angle)
            x = cx + corner[0] * math.cos(rad_angle) - corner[1] * math.sin(rad_angle)
            y = cy + corner[0] * math.sin(rad_angle) + corner[1] * math.cos(rad_angle)
            points.append((int(x), int(y)))

        return points

    def get_bounding_rect(self, pos=None):
        points = self.get_bounding_points(pos)
        min_x = min([p[0] for p in points])
        max_x = max([p[0] for p in points])
        min_y = min([p[1] for p in points])
        max_y = max([p[1] for p in points])
        return pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)

    def draw_hitbox(self, window):
        pygame.draw.polygon(window, (255, 0, 0), self.get_bounding_points(), 1)
        pygame.draw.rect(window, (0, 255, 0), self.get_bounding_rect(), 1)
        pygame.draw.circle(window, (0, 0, 255), self.get_cannon_position(), 1)
        pygame.draw.circle(window, (0, 0, 255), self.get_center_pos(), 1)

    def hit(self):
        self.other_tank.add_points()
        place_tank(self, self.walls)

    def add_points(self):
        self.score = self.score + 1
