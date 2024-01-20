import random

from config import WINDOW_WIDTH, WINDOW_HEIGHT


def check_tank_wall_collision(tank, walls):
    for wall in walls:
        if tank.get_bounding_rect().colliderect(wall.get_rect()):
            return True
    return False


def place_tank(tank, walls):
    placed = False
    max_distance = 0
    count = 0
    best_pos = None
    while not placed and count < 100:
        x = random.randint(0, WINDOW_WIDTH - tank.size[0])
        y = random.randint(0, WINDOW_HEIGHT - tank.size[1])
        tank.update_draw_position((x, y))
        if not check_tank_wall_collision(tank, walls):
            if tank.other_tank:
                distance_other_tank = calculate_distance(tank.get_center_pos(), tank.other_tank.get_center_pos())
                count += 1
                if distance_other_tank > max_distance:
                    max_distance = distance_other_tank
                    best_pos = (x, y)

            else:
                placed = True

    if not placed:
        tank.update_draw_position(best_pos)


def calculate_distance(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5
