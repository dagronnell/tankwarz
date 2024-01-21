import pygame

from collision import polygons_collide
from config import WINDOW_WIDTH, WINDOW_HEIGHT, BACKGROUND_COLOR, PROJECTILE_MAX_COUNT, PROJECTILE_MAX_MOVE
from scene import place_tank
from tank import Tank
from wall import create_walls

# Initialize pygame
pygame.init()
clock = pygame.time.Clock()
pygame.mixer.init()
fire_sound = pygame.mixer.Sound('snd/cannon1.wav')
hit_sound = pygame.mixer.Sound('snd/explosion1.wav')
score_font_size = 24
score_font = pygame.font.Font(None, score_font_size)

# Set up the display window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tank Death Match")

# Initialize objects, tanks, walls & projectiles
walls = create_walls()

player1_tank = Tank("icons/tank4.png", walls)
player2_tank = Tank("icons/tank4.png", walls)
place_tank(player1_tank, walls)
player1_tank.set_other_tank(player2_tank)
player2_tank.set_other_tank(player1_tank)
place_tank(player2_tank, walls)

tanks = [player1_tank, player2_tank]

projectiles = []
player1_projectile_count, player2_projectile_count = 0, 0


def control_tank(tank, up, down, left, right, fire):
    if up or down:
        direction = 1 if up else -1
        tank.move(direction)

    if left or right:
        direction = 1 if left else -1
        tank.rotate(direction)

    if fire:
        if tank.projectile_count < PROJECTILE_MAX_COUNT:
            new_projectile = tank.shoot(current_time)
            if new_projectile:
                fire_sound.play()
                projectiles.append(new_projectile)
                tank.projectile_count += 1


# Main game loop
running = True
while running:
    current_time = pygame.time.get_ticks()  # Get the current time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # player_tank handling
    keys = pygame.key.get_pressed()
    control_tank(player1_tank,
                 keys[pygame.K_UP], keys[pygame.K_DOWN],
                 keys[pygame.K_LEFT], keys[pygame.K_RIGHT],
                 keys[pygame.K_SPACE]
                 )
    control_tank(player2_tank,
                 keys[pygame.K_w], keys[pygame.K_s],
                 keys[pygame.K_a], keys[pygame.K_d],
                 keys[pygame.K_1]
                 )

    window.fill(BACKGROUND_COLOR)
    for tank in tanks:
        tank.draw(window)
        # tank.draw_hitbox(window)

    for wall in walls:
        wall.draw(window)

    # Move projectiles and check for collisions
    active_projectiles = []
    hit_tank = False
    for projectile in projectiles:
        projectile.move()
        hit_wall = False
        hit_tank = False
        next_pos = projectile.get_next_position()
        for wall in walls:
            if projectile.get_bounding_rect(next_pos).colliderect(wall.get_rect()):
                projectile.bounce(wall)
                hit_wall = True
                break

        if not hit_wall:
            for tank in tanks:
                if projectile.get_bounding_rect().colliderect(tank.get_bounding_rect()):
                    if polygons_collide(tank.get_bounding_points(), projectile.get_bounding_points()):
                        tank.hit()
                        hit_sound.play()
                        hit_tank = True
                        break

        if not hit_tank and projectile.move_count < PROJECTILE_MAX_MOVE:
            active_projectiles.append(projectile)
            projectile.draw(window)
        else:
            if projectile.shooter == player1_tank:
                player1_tank.projectile_count -= 1
            else:
                player2_tank.projectile_count -= 1

        if hit_tank:
            break

    if not hit_tank:
        projectiles = active_projectiles
    else:
        projectiles = []
        player1_tank.projectile_count = 0
        player2_tank.projectile_count = 0

    player1_score_text = score_font.render(f"Player_1: {player1_tank.score}", True, (255, 255, 255))
    window.blit(player1_score_text, (10, window.get_height() - score_font_size - 10))

    player2_score_text = score_font.render(f"Player_2: {player2_tank.score}", True, (255, 255, 255))
    window.blit(player2_score_text, (window.get_width() - player2_score_text.get_width() - 10, window.get_height() - score_font_size - 10))

    pygame.display.flip()
    clock.tick(60)

# Quit pygame
pygame.quit()
