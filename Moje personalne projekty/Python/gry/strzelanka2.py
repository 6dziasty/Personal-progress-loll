import pygame
import random
import sys
import math

pygame.init()

WIDTH, HEIGHT = 500, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Strzelanka Ultimate")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
GREEN = (50, 220, 50)
BLUE = (50, 150, 255)
YELLOW = (255, 255, 0)
PURPLE = (200, 0, 200)
ORANGE = (255, 165, 0)

FONT = pygame.font.SysFont("arial", 24)

player = pygame.Rect(WIDTH//2 - 20, HEIGHT - 80, 40, 60)
player_speed = 7

bullets = []
rockets = []
grenades = []
bananas = []

weapon = "rifle"
ENEMY_TYPES = [
    {"color": GREEN, "speed": 2, "hp": 5},
    {"color": RED, "speed": 3, "hp": 2},
    {"color": BLUE, "speed": 2, "hp": 3},
]

enemies = []
explosions = []

stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT)] for _ in range(120)]

score = 0
hp = 100

clock = pygame.time.Clock()
running = True


def draw_background():
    WIN.fill((30, 30, 60))
    for star in stars:
        pygame.draw.circle(WIN, random.choice([WHITE, YELLOW, ORANGE, PURPLE]), star, 2)
        star[1] += 1
        if star[1] > HEIGHT:
            star[1] = 0
            star[0] = random.randint(0, WIDTH)


def draw_player():
    pygame.draw.rect(WIN, BLUE, (player.x + 10, player.y + 20, 20, 40))
    pygame.draw.circle(WIN, WHITE, (player.x + 20, player.y + 10), 10)


def draw_health_bar():
    pygame.draw.rect(WIN, RED, (10, 50, 100, 10))
    pygame.draw.rect(WIN, GREEN, (10, 50, max(hp, 0), 10))


def spawn_enemy():
    if random.randint(1, 40) == 1:
        type_data = random.choice(ENEMY_TYPES)
        enemy = {
            "rect": pygame.Rect(random.randint(0, WIDTH - 40), 0, 40, 40),
            "color": type_data["color"],
            "speed": type_data["speed"],
            "hp": type_data["hp"]
        }
        enemies.append(enemy)


def shoot_rifle():
    bullets.append({"rect": pygame.Rect(player.centerx - 2, player.y, 4, 10), "dir": 0})


def shoot_shotgun():
    angles = [-20, -10, 0, 10, 20]
    for angle in angles:
        bullets.append({"rect": pygame.Rect(player.centerx - 2, player.y, 4, 10), "dir": angle})


def shoot_rpg():
    rockets.append({"rect": pygame.Rect(player.centerx - 5, player.y, 10, 20), "speed": 7})


def throw_grenade():
    grenades.append({"rect": pygame.Rect(player.centerx - 8, player.y, 16, 16), "speed": 5, "timer": 60})


def throw_banana():
    bananas.append({"rect": pygame.Rect(player.centerx - 8, player.y, 16, 16), "speed": 6, "timer": 100})


def move_bullets():
    for bullet in bullets[:]:
        angle_rad = math.radians(bullet["dir"])
        bullet["rect"].y -= int(12 * math.cos(angle_rad))
        bullet["rect"].x += int(12 * math.sin(angle_rad))
        if bullet["rect"].y < 0 or bullet["rect"].x < 0 or bullet["rect"].x > WIDTH:
            bullets.remove(bullet)
        pygame.draw.rect(WIN, RED, bullet["rect"])


def move_rockets():
    for rocket in rockets[:]:
        rocket["rect"].y -= rocket["speed"]
        if rocket["rect"].y < 0:
            rockets.remove(rocket)
        pygame.draw.rect(WIN, YELLOW, rocket["rect"])


def move_grenades():
    for grenade in grenades[:]:
        grenade["rect"].y -= grenade["speed"]
        grenade["timer"] -= 1
        pygame.draw.rect(WIN, ORANGE, grenade["rect"])
        if grenade["timer"] <= 0:
            explosions.append({"pos": grenade["rect"].center, "timer": 30, "radius": 50})
            grenades.remove(grenade)


def move_bananas():
    for banana in bananas[:]:
        banana["rect"].y -= banana["speed"]
        banana["timer"] -= 1
        pygame.draw.rect(WIN, PURPLE, banana["rect"])
        if banana["timer"] <= 0:
            explosions.append({"pos": banana["rect"].center, "timer": 50, "radius": 80})
            bananas.remove(banana)


def move_enemies():
    global hp
    for enemy in enemies[:]:
        enemy["rect"].y += enemy["speed"]
        pygame.draw.ellipse(WIN, enemy["color"], enemy["rect"])
        pygame.draw.circle(WIN, BLACK, enemy["rect"].center, 5)
        if enemy["rect"].y > HEIGHT:
            enemies.remove(enemy)
            hp -= 10


def handle_collisions():
    global score
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet["rect"].colliderect(enemy["rect"]):
                bullets.remove(bullet)
                enemy["hp"] -= 1
                if enemy["hp"] <= 0:
                    enemies.remove(enemy)
                    score += 1
                break
    for rocket in rockets[:]:
        for enemy in enemies[:]:
            if rocket["rect"].colliderect(enemy["rect"]):
                explosions.append({"pos": enemy["rect"].center, "timer": 40, "radius": 60})
                rockets.remove(rocket)
                if enemy in enemies:
                    enemies.remove(enemy)
                score += 2
                break


def handle_explosions():
    for explosion in explosions[:]:
        pygame.draw.circle(WIN, random.choice([YELLOW, ORANGE, PURPLE]), explosion["pos"], explosion["radius"])
        explosion["timer"] -= 1
        if explosion["timer"] <= 0:
            explosions.remove(explosion)

while running:
    clock.tick(60)
    draw_background()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += player_speed

    if keys[pygame.K_SPACE]:
        if weapon == "rifle" and len(bullets) < 7:
            shoot_rifle()
        elif weapon == "shotgun" and len(bullets) < 15:
            shoot_shotgun()
        elif weapon == "rpg" and len(rockets) < 2:
            shoot_rpg()
        elif weapon == "grenade" and len(grenades) < 3:
            throw_grenade()
        elif weapon == "banana" and len(bananas) < 1:
            throw_banana()

    if keys[pygame.K_1]:
        weapon = "rifle"
    if keys[pygame.K_2]:
        weapon = "shotgun"
    if keys[pygame.K_3]:
        weapon = "rpg"
    if keys[pygame.K_4]:
        weapon = "grenade"
    if keys[pygame.K_5]:
        weapon = "banana"

    draw_player()
    spawn_enemy()
    move_bullets()
    move_rockets()
    move_grenades()
    move_bananas()
    move_enemies()
    handle_collisions()
    handle_explosions()

    score_text = FONT.render(f"Punkty: {score}  HP: {hp}  Broń: {weapon}", True, WHITE)
    WIN.blit(score_text, (10, 10))
    draw_health_bar()

    if hp <= 0:
        end_text = FONT.render("PRZEGRANA", True, RED)
        WIN.blit(end_text, (WIDTH//2 - end_text.get_width()//2, HEIGHT//2))
        pygame.display.update()
        pygame.time.delay(2000)
        running = False

    if score >= 50:
        win_text = FONT.render("WYGRANA!", True, GREEN)
        WIN.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2))
        pygame.display.update()
        pygame.time.delay(2000)
        running = False

    pygame.display.update()

pygame.quit()
sys.exit()
