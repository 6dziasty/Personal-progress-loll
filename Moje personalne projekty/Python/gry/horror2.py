import pygame
import sys
import random

pygame.init()

# Stałe
WIDTH, HEIGHT = 800, 600
FPS = 60
FONT = pygame.font.SysFont("Arial", 24)

# Kolory
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (30, 30, 30)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)

# Horrorowe kolory i shaderowe efekty
BLOOD_RED = (80, 0, 0)
DIRTY_WALL = (50, 50, 50)
FLOOR_COLOR = (20, 20, 20)

# Ekran
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Creepy House")
clock = pygame.time.Clock()

# Obrazy
player_img = pygame.Surface((40, 60))
player_img.fill(YELLOW)

monster_img = pygame.Surface((60, 60))
monster_img.fill(RED)

key_img = pygame.Surface((20, 20))
key_img.fill((255, 215, 0))

# Stan gry
player_pos = [WIDTH // 2, HEIGHT - 70]
room = "outside"
in_kitchen = False
has_key = False
show_code = False
code_found = False
code_entered = False
jumpscare = False
jumpscare_timer = 0
code = "4371"
input_code = ""

# Pomieszczenia
rooms = {
    "outside": DARK_GRAY,
    "hall": DIRTY_WALL,
    "kitchen": (40, 20, 20),
    "code_room": (30, 0, 0)
}

# Drzwi i elementy
doors = {
    "outside_to_hall": pygame.Rect(350, 500, 100, 50),
    "hall_to_kitchen": pygame.Rect(100, 200, 80, 80),
    "kitchen_to_hall": pygame.Rect(10, 250, 60, 60),
    "hall_to_code": pygame.Rect(600, 150, 80, 100)
}

key_rect = pygame.Rect(600, 350, 20, 20)
lock_rect = pygame.Rect(620, 100, 40, 40)
code_area = pygame.Rect(580, 60, 100, 30)

# Potwór
monster_rect = pygame.Rect(700, 500, 60, 60)
monster_visible = False
monster_timer = 0

# Funkcje
def draw_text(text, x, y, color=WHITE, size=24):
    font = pygame.font.SysFont("Arial", size)
    render = font.render(text, True, color)
    screen.blit(render, (x, y))

def draw_room():
    screen.fill(rooms[room])
    if room == "outside":
        draw_text("Podejdź do drzwi", 300, 100)
        pygame.draw.rect(screen, (100, 100, 100), doors["outside_to_hall"])
    elif room == "hall":
        draw_text("Dom - Korytarz", 10, 10)
        pygame.draw.rect(screen, (80, 80, 80), doors["hall_to_kitchen"])
        pygame.draw.rect(screen, (60, 60, 60), doors["hall_to_code"])
    elif room == "kitchen":
        draw_text("Kuchnia", 10, 10)
        pygame.draw.rect(screen, (70, 70, 70), doors["kitchen_to_hall"])
        pygame.draw.rect(screen, (255, 0, 0), lock_rect)
        if not code_found:
            draw_text("Kod nad lodówką", code_area.x, code_area.y - 30, RED)
            pygame.draw.rect(screen, (100, 0, 0), code_area)
        if not has_key:
            screen.blit(key_img, key_rect)
    elif room == "code_room":
        draw_text("Pokój z drzwiami", 10, 10)
        if not code_entered:
            draw_text("Wprowadź kod: " + input_code, 300, 200, RED, 32)
        else:
            draw_text("Drzwi otwarte!", 300, 200, YELLOW, 32)

    if monster_visible:
        screen.blit(monster_img, monster_rect)

    screen.blit(player_img, player_pos)

    if show_code:
        draw_text("Kod: " + code, 10, 550, YELLOW, 28)

def show_jumpscare():
    global jumpscare, jumpscare_timer
    jumpscare_img = pygame.Surface((WIDTH, HEIGHT))
    jumpscare_img.fill(BLOOD_RED)
    draw_text("BUUU!", WIDTH//2 - 50, HEIGHT//2 - 30, WHITE, 48)
    screen.blit(jumpscare_img, (0, 0))
    jumpscare_timer += 1
    if jumpscare_timer > FPS:
        jumpscare = False
        jumpscare_timer = 0

def reset_game():
    global room, player_pos, has_key, code_found, code_entered, show_code, input_code, jumpscare
    room = "outside"
    player_pos = [WIDTH // 2, HEIGHT - 70]
    has_key = False
    code_found = False
    show_code = False
    code_entered = False
    input_code = ""
    jumpscare = False

# Główna pętla
done = False
while not done:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if jumpscare:
                continue
            if event.key == pygame.K_e:
                if room == "kitchen" and code_area.collidepoint(player_pos[0], player_pos[1]):
                    show_code = True
                    code_found = True
                elif room == "kitchen" and key_rect.collidepoint(player_pos[0], player_pos[1]) and code_found:
                    has_key = True
                elif room == "code_room" and not code_entered:
                    if input_code == code:
                        code_entered = True
                elif room == "hall" and doors["hall_to_code"].collidepoint(player_pos[0], player_pos[1]) and has_key:
                    room = "code_room"
                    player_pos = [300, 500]
                    monster_visible = True
                    monster_rect.x = 700
                    monster_rect.y = 500
            elif event.key == pygame.K_BACKSPACE:
                input_code = input_code[:-1]
            elif event.key in range(pygame.K_0, pygame.K_9 + 1):
                if room == "code_room" and not code_entered:
                    input_code += event.unicode

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= 5
    if keys[pygame.K_RIGHT]:
        player_pos[0] += 5
    if keys[pygame.K_UP]:
        player_pos[1] -= 5
    if keys[pygame.K_DOWN]:
        player_pos[1] += 5

    # Przejścia między pokojami
    if room == "outside" and doors["outside_to_hall"].collidepoint(player_pos):
        room = "hall"
        player_pos = [400, 500]
        jumpscare = True

    elif room == "hall":
        if doors["hall_to_kitchen"].collidepoint(player_pos):
            room = "kitchen"
            player_pos = [200, 300]

    elif room == "kitchen" and doors["kitchen_to_hall"].collidepoint(player_pos):
        room = "hall"
        player_pos = [150, 300]

    # Ruch potwora
    if monster_visible:
        if monster_rect.x > player_pos[0]:
            monster_rect.x -= 1
        if monster_rect.y > player_pos[1]:
            monster_rect.y -= 1
        if monster_rect.colliderect(pygame.Rect(player_pos[0], player_pos[1], 40, 60)):
            jumpscare = True
            monster_visible = False

    if jumpscare:
        show_jumpscare()
    else:
        draw_room()

    pygame.display.flip()

pygame.quit()
sys.exit()