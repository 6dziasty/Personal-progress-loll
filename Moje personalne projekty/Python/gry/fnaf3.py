import pygame
import sys
import random
from datetime import datetime, timedelta

# --- KONFIGURACJA ---
WIDTH, HEIGHT = 1000, 650
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
OFFICE_BG = (40, 40, 40)
DARK_GRAY = (25, 25, 25)

CAMERA_W, CAMERA_H = 180, 130

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini FNAF w Pygame - VHCam Look")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 24)
small_font = pygame.font.SysFont('Arial', 18)

camera_bg_colors = [
    (30, 30, 60),
    (60, 30, 30),
    (30, 60, 30),
    (60, 60, 30),
]

camera_positions = [
    (50, 50),
    (250, 50),
    (450, 50),
    (650, 50),
]

camera_names = ["Lobby", "Hallway", "Dining Room", "Storage"]

class Camera:
    def __init__(self, name, pos, bg_color):
        self.name = name
        self.rect = pygame.Rect(pos[0], pos[1], CAMERA_W, CAMERA_H)
        self.view_surface = pygame.Surface((CAMERA_W, CAMERA_H))
        self.bg_color = bg_color

    def draw(self, surf):
        pygame.draw.rect(surf, WHITE, self.rect, 2)
        text = small_font.render(self.name, True, WHITE)
        surf.blit(self.view_surface, self.rect.topleft)
        surf.blit(text, (self.rect.x + 5, self.rect.y + 5))

class Enemy:
    def __init__(self, cam_route):
        self.cam_route = cam_route
        self.current_cam_idx = 0
        self.time_since_move = 0
        self.at_door_timer = 0
        self.back_to_start_timer = 0
        self.state = "moving"

    def update(self, dt, door_closed, lights_on):
        self.time_since_move += dt
        if self.state == "moving" and self.time_since_move >= 5:
            self.current_cam_idx += 1
            self.time_since_move = 0
            if self.current_cam_idx >= len(self.cam_route):
                self.state = "waiting"
                self.current_cam_idx = len(self.cam_route) - 1
        elif self.state == "waiting":
            self.at_door_timer += dt
            if door_closed:
                self.state = "backing"
                self.back_to_start_timer = 0
            elif self.at_door_timer >= 5:
                return True
        elif self.state == "backing":
            self.back_to_start_timer += dt
            if self.back_to_start_timer >= 3:
                self.current_cam_idx = 0
                self.state = "moving"
                self.time_since_move = 0
        return False

    def get_current_camera(self):
        return self.cam_route[self.current_cam_idx]

cameras = [Camera(camera_names[i], camera_positions[i], camera_bg_colors[i]) for i in range(len(camera_positions))]

enemy = Enemy([0, 1, 2])
selected_camera_index = 0
vhc_surface = pygame.Surface((CAMERA_W * 2, CAMERA_H * 2), pygame.SRCALPHA)

office_surface = pygame.Surface((WIDTH, HEIGHT))
office_surface.fill(OFFICE_BG)

current_time = datetime.strptime("12:00", "%H:%M")
game_end_time = datetime.strptime("06:00", "%H:%M") + timedelta(days=1)
time_speed = 1
game_over = False
win = False
doors_closed = False
lights_on = False
battery = 100

def apply_vhc_effect(surface):
    vhc_surface.fill((0, 0, 0, 50))
    for y in range(0, vhc_surface.get_height(), 4):
        pygame.draw.line(vhc_surface, (0, 255, 0, 30), (0, y), (vhc_surface.get_width(), y))
    surface.blit(vhc_surface, (50, 200), special_flags=pygame.BLEND_RGBA_ADD)

def draw_clock(surface, time):
    time_text = font.render(f"Czas: {time.strftime('%H:%M')}", True, YELLOW)
    surface.blit(time_text, (WIDTH - 180, HEIGHT - 50))

def draw_instructions(surface):
    lines = ["← →: zmiana kamery", "D: drzwi Office", "F: światło Office", "R: restart"]
    for i, text in enumerate(lines):
        instr = small_font.render(text, True, WHITE)
        surface.blit(instr, (20, HEIGHT - 20 - i * 20))

def draw_doors(surface, is_closed):
    color = GREEN if is_closed else RED
    pygame.draw.rect(surface, color, (WIDTH // 2 - 100, HEIGHT - 70, 200, 20))
    status_text = small_font.render("Drzwi: Zamknięte" if is_closed else "Drzwi: Otwarte", True, WHITE)
    surface.blit(status_text, (WIDTH // 2 - status_text.get_width() // 2, HEIGHT - 90))

def draw_game_over(surface, won):
    surface.fill(BLACK)
    text = font.render("WYGRANA!" if won else "PRZEGRANA", True, GREEN if won else RED)
    surface.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
    restart_text = small_font.render("R: Restart", True, WHITE)
    surface.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))

def reset_game():
    global current_time, game_over, win, doors_closed, enemy, lights_on, battery
    current_time = datetime.strptime("12:00", "%H:%M")
    game_over = False
    win = False
    doors_closed = False
    lights_on = False
    battery = 100
    enemy = Enemy([0, 1, 2])

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
            if game_over:
                if event.key == pygame.K_r:
                    reset_game()
            else:
                if event.key == pygame.K_RIGHT:
                    selected_camera_index = (selected_camera_index + 1) % len(cameras)
                elif event.key == pygame.K_LEFT:
                    selected_camera_index = (selected_camera_index - 1) % len(cameras)
                elif event.key == pygame.K_d:
                    doors_closed = not doors_closed
                elif event.key == pygame.K_f:
                    lights_on = not lights_on

    if not game_over:
        current_time += timedelta(seconds=dt * 60 * time_speed)
        if current_time >= game_end_time:
            game_over = True
            win = True
        if enemy.update(dt, doors_closed, lights_on):
            game_over = True
            win = False
        screen.fill(BLACK)
        for cam in cameras:
            cam.view_surface.fill(cam.bg_color)
        current_cam = cameras[selected_camera_index]
        if enemy.get_current_camera() == selected_camera_index:
            pygame.draw.circle(current_cam.view_surface, RED, (CAMERA_W // 2, CAMERA_H // 2), 20)
        for cam in cameras:
            cam.draw(screen)
        scaled_view = pygame.transform.scale(current_cam.view_surface, (CAMERA_W * 2, CAMERA_H * 2))
        office_surface.fill(OFFICE_BG)
        if lights_on:
            pygame.draw.rect(office_surface, YELLOW, (0, 0, WIDTH, HEIGHT), 20)
        screen.blit(office_surface, (0, 0))
        screen.blit(scaled_view, (50, 200))
        apply_vhc_effect(screen)
        draw_doors(screen, doors_closed)
        pygame.draw.rect(screen, WHITE, (WIDTH - 180, 20, 140, 20), 2)
        inner_w = int((battery / 100) * 136)
        pygame.draw.rect(screen, GREEN if battery > 20 else RED, (WIDTH - 178, 22, inner_w, 16))
        draw_clock(screen, current_time)
        draw_instructions(screen)
    else:
        draw_game_over(screen, win)
    pygame.display.flip()
