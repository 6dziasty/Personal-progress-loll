import pygame
import sys
import random

# Inicjalizacja
pygame.init()
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mroczny Las")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 28)

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_RED = (100, 0, 0)

# Postać gracza
player_img = pygame.Surface((50, 90))
player_img.fill((150, 150, 150))
player = player_img.get_rect(midbottom=(100, screen_height - 70))
player_speed = 5

# Potwór
monster_img = pygame.Surface((60, 100))
monster_img.fill((50, 0, 0))
monster = monster_img.get_rect(midbottom=(-100, screen_height - 70))
monster_visible = False
monster_speed = 2

# Jumpscare
jumpscare_img = pygame.Surface((screen_width, screen_height))
jumpscare_img.fill(BLACK)
jumpscare_face = pygame.font.SysFont("arial", 200).render(":)", True, RED)
jumpscare_timer = 0
jumpscare_active = False

# Tło
forest_bg = pygame.Surface((screen_width * 2, screen_height))
forest_bg.fill((30, 30, 30))
for i in range(50):
    pygame.draw.rect(forest_bg, (20, 80, 20), (random.randint(0, screen_width * 2), screen_height - 100, 40, 100))

# Domek
house_area_x = 1000
house_entered = False
house_inside = False

# UI
def draw_ui():
    pygame.draw.rect(screen, (100, 100, 100), (10, 10, 200, 40))
    screen.blit(font.render("← → by chodzić", True, WHITE), (20, 15))

# Latarka
def draw_light():
    light = pygame.Surface((screen_width, screen_height))
    light.fill(BLACK)
    pygame.draw.circle(light, (0, 0, 0, 0), player.center, 150)
    light.set_colorkey((0, 0, 0))
    screen.blit(light, (0, 0))

# Dialogi
dialogues = [
    (300, "Co to za miejsce..."),
    (500, "Czuję, że ktoś mnie obserwuje..."),
    (800, "Czy to... domek?")
]
current_dialogue = ""
dialogue_timer = 0

# Potwór pojawia się
spawn_monster_at = 1100

# Główna pętla
distance = 0
running = True
while running:
    screen.fill((0, 0, 0))
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Ruch
    if keys[pygame.K_RIGHT]:
        player.x += player_speed
        distance += player_speed
    elif keys[pygame.K_LEFT]:
        player.x -= player_speed
        distance -= player_speed
    player.clamp_ip(pygame.Rect(0, 0, screen_width, screen_height))

    # Tło lasu lub domku
    if house_inside:
        screen.fill((30, 0, 0))
        screen.blit(font.render("Wnętrze chaty...", True, WHITE), (screen_width // 2 - 100, 30))
    else:
        screen.blit(forest_bg, (-distance, 0))

    # Dialogi
    for trigger_x, text in dialogues:
        if distance >= trigger_x and dialogue_timer == 0:
            current_dialogue = text
            dialogue_timer = pygame.time.get_ticks()

    if current_dialogue:
        screen.blit(font.render(current_dialogue, True, WHITE), (screen_width // 2 - 200, screen_height - 100))
        if pygame.time.get_ticks() - dialogue_timer > 3000:
            current_dialogue = ""
            dialogue_timer = 0

    # Wejście do domku
    if distance >= house_area_x and not house_entered:
        current_dialogue = "Wchodzisz do starej chaty..."
        house_entered = True
        dialogue_timer = pygame.time.get_ticks()
        pygame.time.set_timer(pygame.USEREVENT + 1, 3000, loops=1)
    elif event.type == pygame.USEREVENT + 1:
        house_inside = True
        distance = 0
        player.x = 100

    # Potwór
    if distance >= spawn_monster_at and not monster_visible and not house_inside:
        monster_visible = True
        monster.x = screen_width + 200
    if monster_visible and not house_inside:
        monster.x -= monster_speed
        screen.blit(monster_img, monster)

    # Jumpscare aktywacja
    if monster_visible and monster.colliderect(player) and not jumpscare_active:
        jumpscare_active = True
        jumpscare_timer = pygame.time.get_ticks()

    # Jumpscare
    if jumpscare_active:
        screen.blit(jumpscare_img, (0, 0))
        screen.blit(jumpscare_face, (screen_width // 2 - 100, screen_height // 2 - 100))
        if pygame.time.get_ticks() - jumpscare_timer > 2000:
            jumpscare_active = False
            monster_visible = False
            monster.x = -100

    # Gracz
    if not jumpscare_active:
        screen.blit(player_img, player)

    # Latarka i UI
    draw_light()
    draw_ui()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
