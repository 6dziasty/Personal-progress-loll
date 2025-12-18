import pygame
import random
import sys

# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna gry
WIDTH, HEIGHT = 500, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kosmiczna Strzelanka")

# Kolory
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Czcionka
FONT = pygame.font.SysFont("arial", 30)

# Gracz (statek)
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 40
player = pygame.Rect(WIDTH//2 - PLAYER_WIDTH//2, HEIGHT - 60, PLAYER_WIDTH, PLAYER_HEIGHT)
player_speed = 5

# Lista pocisków
bullets = []
bullet_speed = 10

# Lista wrogów
enemies = []
enemy_speed = 3
ENEMY_WIDTH, ENEMY_HEIGHT = 40, 30

# Wynik
score = 0

# Zegar do kontroli FPS
clock = pygame.time.Clock()
running = True

# Główna pętla gry
while running:
    clock.tick(60)  # 60 klatek na sekundę
    WIN.fill((10, 10, 30))  # Tło

    # Obsługa zdarzeń (np. zamknięcie okna)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Obsługa klawiszy
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += player_speed
    if keys[pygame.K_SPACE]:
        # Dodanie pocisku jeśli nie ma ich za dużo
        if len(bullets) < 5:
            bullets.append(pygame.Rect(player.centerx - 2, player.y, 4, 10))

    # Rysowanie gracza
    pygame.draw.rect(WIN, WHITE, player)

    # Aktualizacja i rysowanie pocisków
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)
        pygame.draw.rect(WIN, RED, bullet)

    # Dodawanie nowych wrogów losowo
    if random.randint(1, 30) == 1:
        x = random.randint(0, WIDTH - ENEMY_WIDTH)
        enemies.append(pygame.Rect(x, 0, ENEMY_WIDTH, ENEMY_HEIGHT))

    # Aktualizacja i rysowanie wrogów
    for enemy in enemies[:]:
        enemy.y += enemy_speed
        if enemy.y > HEIGHT:
            enemies.remove(enemy)
        pygame.draw.rect(WIN, GREEN, enemy)

    # Kolizje: pocisk vs wróg
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1
                break

    # Wyświetlanie wyniku
    text = FONT.render(f"Punkty: {score}", True, WHITE)
    WIN.blit(text, (10, 10))

    # Aktualizacja okna
    pygame.display.update()

# Zamknięcie gry
pygame.quit()
sys.exit()
