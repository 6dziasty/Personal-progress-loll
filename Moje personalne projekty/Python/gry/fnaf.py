import pygame
import sys
import random
from datetime import datetime, timedelta

# --- KONFIGURACJA ---
WIDTH, HEIGHT = 800, 600
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

CAMERA_W, CAMERA_H = 180, 130

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini FNAF w Pygame - z drzwiami i różnymi kamerami")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 24)
small_font = pygame.font.SysFont('Arial', 18)

# --- DODANE: kolory tła dla każdej kamery (różne!) ---
camera_bg_colors = [
    (30, 30, 60),    # Lobby - ciemny granat
    (60, 30, 30),    # Hallway - ciemny bordowy
    (30, 60, 30),    # Dining Room - ciemna zieleń
    (60, 60, 30),    # Office - ciemny oliwkowy
]

class Camera:
    def __init__(self, name, pos, bg_color):
        self.name = name
        self.rect = pygame.Rect(pos[0], pos[1], CAMERA_W, CAMERA_H)
        self.view_surface = pygame.Surface((CAMERA_W, CAMERA_H))
        self.bg_color = bg_color

    def draw(self, surf, x, y):
        pygame.draw.rect(surf, WHITE, (x, y, CAMERA_W, CAMERA_H), 2)
        text = small_font.render(self.name, True, WHITE)
        surf.blit(text, (x + 5, y + 5))
        surf.blit(self.view_surface, (x, y + 30))

class Enemy:
    def __init__(self, name, cam_route):
        self.name = name
        self.cam_route = cam_route
        self.current_cam_idx = 0
        self.pos_in_cam = [CAMERA_W // 2, CAMERA_H // 2]
        self.move_dir = 1
        self.move_speed = 1
        self.move_counter = 0
        self.time_since_move = 0

    def update(self):
        self.time_since_move += 1 / FPS
        self.pos_in_cam[0] += self.move_dir * self.move_speed
        self.move_counter += 1
        if self.move_counter > 50:
            self.move_dir *= -1
            self.move_counter = 0

    def draw(self, surface):
        pygame.draw.circle(surface, RED, (int(self.pos_in_cam[0]), int(self.pos_in_cam[1])), 10)

    def move_to_next_camera(self):
        self.current_cam_idx = (self.current_cam_idx + 1) % len(self.cam_route)
        self.pos_in_cam = [CAMERA_W // 2, CAMERA_H // 2]
        self.move_dir = 1
        self.move_counter = 0
        self.time_since_move = 0

    def get_current_camera(self):
        return self.cam_route[self.current_cam_idx]

camera_positions = [
    (50, 50),
    (250, 50),
    (450, 50),
    (650, 50),
]
camera_names = ["Lobby", "Hallway", "Dining Room", "Office"]
cameras = [Camera(camera_names[i], camera_positions[i], camera_bg_colors[i]) for i in range(len(camera_positions))]

enemies = [
    Enemy("Phantom Freddy", [cameras[0], cameras[1], cameras[2]]),
    Enemy("Shadow Bonnie", [cameras[2], cameras[3], cameras[0]]),
]

selected_camera_index = 0

game_start_time = datetime.strptime("12:00", "%H:%M")
game_end_time = datetime.strptime("06:00", "%H:%M") + timedelta(days=1)
current_time = game_start_time
time_speed = 1

game_over = False
win = False

# --- DODANE: stan drzwi (tylko na "Office") ---
doors_closed = False

def draw_clock(surface, time):
    time_text = font.render(f"Czas: {time.strftime('%H:%M')}", True, YELLOW)
    surface.blit(time_text, (WIDTH - 180, HEIGHT - 50))

# --- PRZENIESIONE instrukcje do PRAWEGO DOLNEGO ROGU ---
def draw_instructions(surface):
    instr1 = small_font.render("Strzałki ← →: zmiana kamery", True, WHITE)
    instr2 = small_font.render("D: zamknij/otwórz drzwi (tylko Office)", True, WHITE)
    instr3 = small_font.render("ESC: wyjście", True, WHITE)
    surface.blit(instr1, (WIDTH - 280, HEIGHT - 90))
    surface.blit(instr2, (WIDTH - 280, HEIGHT - 70))
    surface.blit(instr3, (WIDTH - 280, HEIGHT - 50))

def check_enemy_on_camera(enemy, cam_idx):
    global doors_closed
    if enemy.current_cam_idx == cam_idx:
        # Jeśli drzwi są zamknięte i jesteś na kamerze Office (idx 3), wróg nie może Cię złapać
        if cam_idx == 3 and doors_closed:
            return False
        if enemy.time_since_move > 3:
            if abs(enemy.pos_in_cam[0] - CAMERA_W // 2) < 15:
                if random.random() < 0.1:
                    return True
    return False

def draw_doors(surface, is_closed):
    # Prosty prostokąt na dole powiększonego widoku symbolizujący drzwi
    door_color = GREEN if is_closed else RED
    door_rect = pygame.Rect(50, 50 + CAMERA_H * 2 - 30, CAMERA_W * 2, 30)
    pygame.draw.rect(surface, door_color, door_rect)
    text = small_font.render("Drzwi: " + ("Zamknięte" if is_closed else "Otwarte"), True, BLACK)
    surface.blit(text, (door_rect.x + 10, door_rect.y + 5))

def draw_game_over(surface, won):
    surface.fill(BLACK)
    if won:
        text = font.render("PRZETRWAŁEŚ! WYGRANA!", True, GREEN)
    else:
        text = font.render("ZŁAPANY! KONIEC GRY!", True, RED)
    surface.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

while True:
    dt = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_RIGHT:
                selected_camera_index = (selected_camera_index + 1) % len(cameras)
            elif event.key == pygame.K_LEFT:
                selected_camera_index = (selected_camera_index - 1) % len(cameras)
            elif event.key == pygame.K_d:
                # Tylko na kamerze Office (idx 3) możesz zamknąć/otworzyć drzwi
                if selected_camera_index == 3:
                    doors_closed = not doors_closed

    if not game_over:
        current_time += timedelta(seconds=dt * 60 * time_speed)
        if current_time >= game_end_time:
            game_over = True
            win = True

        for enemy in enemies:
            enemy.update()

        if pygame.time.get_ticks() % 5000 < 100:
            for enemy in enemies:
                enemy.move_to_next_camera()

        screen.fill(BLACK)

        for i, cam in enumerate(cameras):
            x = 50 + i * (CAMERA_W + 10)
            y = 350
            cam.draw(screen, x, y)

        selected_cam = cameras[selected_camera_index]
        selected_cam.view_surface.fill(selected_cam.bg_color)  # DODANE różne tło kamer

        for enemy in enemies:
            if enemy.get_current_camera() == selected_cam:
                enemy.draw(selected_cam.view_surface)

        pygame.draw.rect(screen, WHITE, (50, 50, CAMERA_W * 2, CAMERA_H * 2), 3)
        cam_name_text = font.render(f"Kamera: {selected_cam.name}", True, WHITE)
        screen.blit(cam_name_text, (50, 20))

        scaled_view = pygame.transform.scale(selected_cam.view_surface, (CAMERA_W * 2, CAMERA_H * 2))
        screen.blit(scaled_view, (50, 50))

        # Rysuj drzwi tylko na kamerze Office
        if selected_camera_index == 3:
            draw_doors(screen, doors_closed)

        draw_clock(screen, current_time)
        draw_instructions(screen)

        for enemy in enemies:
            if check_enemy_on_camera(enemy, selected_camera_index):
                game_over = True
                win = False

    else:
        draw_game_over(screen, win)

    pygame.display.flip()
