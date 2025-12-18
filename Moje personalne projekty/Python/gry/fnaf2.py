import pygame
import sys
import random
from datetime import datetime, timedelta

# --- KONFIGURACJA ---
WIDTH, HEIGHT = 1000, 650
FPS = 60

# KOLORY
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
DARK_YELLOW = (180, 180, 0)
OFFICE_BG = (40, 40, 40)
DARK_GRAY = (25, 25, 25)

CAMERA_W, CAMERA_H = 180, 130

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rozbudowany FNAF w Pygame")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 24)
small_font = pygame.font.SysFont('Arial', 16)

# Ładowanie dźwięku jumpscare (wstaw plik jumpscare.wav w tym samym folderze)
try:
    jumpscare_sound = pygame.mixer.Sound("jumpscare.wav")
except:
    jumpscare_sound = None

# --- KAMERY ---
camera_bg_colors = [
    (30, 30, 60),
    (60, 30, 30),
    (30, 60, 30),
    (60, 60, 30),
    (50, 50, 100),
    (80, 30, 30),
]

# Układ kamer - logiczny plan (przykład, można zmieniać)
camera_positions = [
    (50, 50),      # 0 Lobby
    (300, 50),     # 1 Hallway
    (550, 50),     # 2 Kitchen
    (800, 50),     # 3 Dining Room
    (250, 250),    # 4 Storage
    (650, 250),    # 5 Office (tu gracz)
]

camera_names = ["Lobby", "Hallway", "Kitchen", "Dining Room", "Storage", "Office"]

class Camera:
    def __init__(self, idx, name, pos, bg_color):
        self.idx = idx
        self.name = name
        self.rect = pygame.Rect(pos[0], pos[1], CAMERA_W, CAMERA_H)
        self.view_surface = pygame.Surface((CAMERA_W, CAMERA_H))
        self.bg_color = bg_color

    def draw_small(self, surf):
        pygame.draw.rect(surf, WHITE, self.rect, 2)
        text = small_font.render(self.name, True, WHITE)
        surf.blit(text, (self.rect.x + 5, self.rect.y + 5))
        surf.blit(self.view_surface, (self.rect.x, self.rect.y + 25))

    def draw_large(self, surf):
        large_rect = pygame.Rect(50, 350, CAMERA_W*3, CAMERA_H*2)
        pygame.draw.rect(surf, WHITE, large_rect, 3)
        text = font.render(f"Kamera: {self.name}", True, WHITE)
        surf.blit(text, (large_rect.x + 10, large_rect.y - 30))
        scaled_view = pygame.transform.scale(self.view_surface, (CAMERA_W*3, CAMERA_H*2))
        surf.blit(scaled_view, large_rect.topleft)

class Enemy:
    def __init__(self, name, cam_route):
        self.name = name
        self.cam_route = cam_route  # lista indeksów kamer
        self.current_cam_idx = 0
        self.state = "moving"  # moving, waiting, backing, jumpscare
        self.time_since_move = 0
        self.at_door_timer = 0
        self.back_to_start_timer = 0
        self.jumpscare_timer = 0
        self.jumpscare_duration = 3
        self.pos = (CAMERA_W//2, CAMERA_H//2)
        self.visible = False  # czy widoczny na kamerze (zależne od światła/drzwi)
        self.face_anim_phase = 0
        self.face_anim_time = 0

    def update(self, dt, doors_closed, lights_on):
        if self.state == "jumpscare":
            self.jumpscare_timer += dt
            if self.jumpscare_timer >= self.jumpscare_duration:
                self.reset()
            return False

        self.time_since_move += dt

        if self.state == "moving":
            if self.time_since_move > 5:
                self.current_cam_idx += 1
                self.time_since_move = 0
                if self.current_cam_idx >= len(self.cam_route):
                    self.state = "waiting"
                    self.current_cam_idx = len(self.cam_route) - 1
                    self.at_door_timer = 0
            self.visible = False

        elif self.state == "waiting":
            self.at_door_timer += dt
            self.visible = True
            if doors_closed:
                self.state = "backing"
                self.back_to_start_timer = 0
                self.at_door_timer = 0
            elif self.at_door_timer >= random.uniform(3,5):
                if lights_on:
                    self.state = "jumpscare"
                    self.jumpscare_timer = 0
                    if jumpscare_sound:
                        jumpscare_sound.play()
                    return True
                else:
                    # jeśli światło wyłączone - łatwiej przegrywasz - natychmiast jumpscare
                    self.state = "jumpscare"
                    self.jumpscare_timer = 0
                    if jumpscare_sound:
                        jumpscare_sound.play()
                    return True

        elif self.state == "backing":
            self.back_to_start_timer += dt
            self.visible = False
            if self.back_to_start_timer >= 3:
                self.reset()
        return False

    def reset(self):
        self.current_cam_idx = 0
        self.state = "moving"
        self.time_since_move = 0
        self.at_door_timer = 0
        self.back_to_start_timer = 0
        self.jumpscare_timer = 0
        self.visible = False

    def get_current_camera(self):
        return self.cam_route[self.current_cam_idx]

    def is_at_door(self):
        return self.state == "waiting"

    def draw_on_camera(self, surface):
        if self.visible:
            # animacja pulsującej twarzy (czerwone kółko z "oczkami")
            self.face_anim_time += 1/ FPS
            if self.face_anim_time > 0.5:
                self.face_anim_phase = (self.face_anim_phase + 1) % 2
                self.face_anim_time = 0

            base_pos = (CAMERA_W//2, CAMERA_H//2)
            if self.face_anim_phase == 0:
                pygame.draw.circle(surface, RED, base_pos, 20)
                pygame.draw.circle(surface, BLACK, (base_pos[0]-7, base_pos[1]-5), 7)
                pygame.draw.circle(surface, BLACK, (base_pos[0]+7, base_pos[1]-5), 7)
            else:
                pygame.draw.circle(surface, RED, base_pos, 20)
                pygame.draw.circle(surface, BLACK, (base_pos[0]-10, base_pos[1]-3), 5)
                pygame.draw.circle(surface, BLACK, (base_pos[0]+10, base_pos[1]-3), 5)

# Tworzymy kamery i wroga
cameras = [Camera(i, camera_names[i], camera_positions[i], camera_bg_colors[i % len(camera_bg_colors)]) for i in range(len(camera_names))]
enemy = Enemy("Animatronik", [0,1,4,5])  # wróg wędruje: Lobby -> Hallway -> Storage -> Office

selected_camera = 0

game_start_time = datetime.strptime("12:00", "%H:%M")
game_end_time = datetime.strptime("06:00", "%H:%M") + timedelta(days=1)
current_time = game_start_time
time_speed = 1

game_over = False
win = False
doors_closed = False
lights_on = False
battery = 100.0

# Powierzchnia efektu VHS (zielone linie)
vhc_surface = pygame.Surface((CAMERA_W*3, CAMERA_H*2), pygame.SRCALPHA)
def apply_vhc_effect(surface):
    vhc_surface.fill((0,0,0,60))
    for y in range(0, vhc_surface.get_height(), 4):
        pygame.draw.line(vhc_surface, (0,255,0,30), (0,y), (vhc_surface.get_width(), y))
    surface.blit(vhc_surface, (50, 350), special_flags=pygame.BLEND_RGBA_ADD)

def draw_battery(surface, level):
    pygame.draw.rect(surface, WHITE, (WIDTH - 180, 20, 140, 28), 2)
    inner_w = int((level / 100) * 136)
    color = GREEN if level > 20 else RED
    pygame.draw.rect(surface, color, (WIDTH - 176, 24, inner_w, 20))
    text = small_font.render(f"Bateria: {int(level)}%", True, WHITE)
    surface.blit(text, (WIDTH - 180, 50))

def draw_office(surface, doors_closed, lights_on):
    rect = pygame.Rect(550, 350, CAMERA_W*3, CAMERA_H*2)
    pygame.draw.rect(surface, OFFICE_BG, rect)
    pygame.draw.rect(surface, WHITE, rect, 3)

    door_height = 40
    door_rect = pygame.Rect(rect.x + rect.width//2 - 60, rect.y + rect.height - door_height, 120, door_height)
    door_color = GREEN if doors_closed else RED
    pygame.draw.rect(surface, door_color, door_rect)
    door_text = small_font.render("Drzwi: " + ("Zamknięte" if doors_closed else "Otwarte"), True, BLACK)
    surface.blit(door_text, (door_rect.x + 10, door_rect.y + 5))

    # Latarka - mały panel
    flashlight_rect = pygame.Rect(rect.x + 20, rect.y + 20, 100, 30)
    pygame.draw.rect(surface, DARK_GRAY, flashlight_rect)
    pygame.draw.rect(surface, WHITE, flashlight_rect, 2)
    text_flash = small_font.render("Latarka (F)", True, WHITE)
    surface.blit(text_flash, (flashlight_rect.x + 5, flashlight_rect.y + 5))

    # Jeśli światło włączone - rysujemy żółtą poświatę w drzwiach
    if lights_on:
        glow_rect = pygame.Rect(door_rect.x, door_rect.y - 60, door_rect.width, 60)
        glow = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
        glow.fill((255, 255, 150, 120))
        surface.blit(glow, glow_rect.topleft)

def draw_enemy_jumpscare(surface):
    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    radius = 150
    pygame.draw.circle(surface, RED, (center_x, center_y), radius)
    # Oczy w jumpscare - animowane
    eye_offset = 40
    pygame.draw.circle(surface, BLACK, (center_x - eye_offset, center_y - 30), 40)
    pygame.draw.circle(surface, BLACK, (center_x + eye_offset, center_y - 30), 40)
    pygame.draw.circle(surface, RED, (center_x - eye_offset, center_y - 30), 20)
    pygame.draw.circle(surface, RED, (center_x + eye_offset, center_y - 30), 20)

    # Usta (zęby)
    pygame.draw.rect(surface, BLACK, (center_x - 90, center_y + 40, 180, 50))
    for i in range(6):
        x = center_x - 90 + i*30 + 5
        pygame.draw.polygon(surface, WHITE, [(x, center_y + 40), (x + 10, center_y + 40), (x + 5, center_y + 80)])

def draw_clock(surface, time):
    time_text = font.render(f"Czas: {time.strftime('%H:%M')}", True, YELLOW)
    surface.blit(time_text, (20, 20))

def draw_instructions(surface):
    lines = [
        "← → : zmiana kamery",
        "D    : zamknij/otwórz drzwi (Office)",
        "F    : latarka (Office)",
        "R    : restart po przegranej",
        "ESC  : wyjście",
    ]
    for i, line in enumerate(lines):
        text = small_font.render(line, True, WHITE)
        surface.blit(text, (20, HEIGHT - 20 - (len(lines) - i) * 20))

def draw_vhs_effect(surface):
    for y in range(0, HEIGHT, 4):
        pygame.draw.line(surface, (0, 255, 0, 20), (0, y), (WIDTH, y))

def reset_game():
    global current_time, game_over, win, doors_closed, enemy, lights_on, battery
    current_time = game_start_time
    game_over = False
    win = False
    doors_closed = False
    lights_on = False
    battery = 100.0
    enemy.reset()

while True:
    dt = clock.tick(FPS) / 1_000

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
                    selected_camera = (selected_camera + 1) % len(cameras)
                elif event.key == pygame.K_LEFT:
                    selected_camera = (selected_camera - 1) % len(cameras)
                elif event.key == pygame.K_d:
                    if selected_camera == 5:  # Office index
                        doors_closed = not doors_closed
                elif event.key == pygame.K_f:
                    if selected_camera == 5:
                        lights_on = not lights_on

    if not game_over:
        current_time += timedelta(seconds=dt * 60 * time_speed)
        if current_time >= game_end_time:
            game_over = True
            win = True

        # Zużycie baterii
        drain_rate = 0
        if doors_closed:
            drain_rate += 15 * dt
        if lights_on:
            drain_rate += 10 * dt
        battery -= drain_rate
        if battery < 0:
            battery = 0
            # Jeśli brak baterii - światło i drzwi nie działają
            doors_closed = False
            lights_on = False

        # Aktualizacja wroga, sprawdzenie jumpscare
        if enemy.update(dt, doors_closed, lights_on):
            game_over = True
            win = False

        # Czyszczenie ekranów kamer
        for cam in cameras:
            cam.view_surface.fill(cam.bg_color)

        # Rysujemy wroga na kamerze, jeśli jest widoczny i na tej kamerze
        current_cam_obj = cameras[selected_camera]
        if enemy.get_current_camera() == current_cam_obj.idx:
            enemy.draw_on_camera(current_cam_obj.view_surface)

        # Rysowanie kamer w małej formie
        for cam in cameras:
            cam.draw_small(screen)

        # Rysujemy powiększoną kamerę
        current_cam_obj.draw_large(screen)

        # Efekt VHS na powiększonej kamerze
        apply_vhc_effect(screen)

        # Rysujemy biuro i jego elementy
        if selected_camera == 5:  # Office
            draw_office(screen, doors_closed, lights_on)

        # Rysujemy pasek baterii
        draw_battery(screen, battery)

        # Rysujemy zegar i instrukcje
        draw_clock(screen, current_time)
        draw_instructions(screen)

    else:
        # Jumpscare jeśli jest
        if enemy.state == "jumpscare":
            draw_enemy_jumpscare(screen)
        else:
            screen.fill(BLACK)
            msg = "WYGRAŁEŚ! GRATULACJE!" if win else "PRZEGRAŁEŚ! JESTEŚ MARTWY!"
            text = font.render(msg, True, GREEN if win else RED)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 50))
            instr = small_font.render("Naciśnij R, aby zrestartować", True, WHITE)
            screen.blit(instr, (WIDTH//2 - instr.get_width()//2, HEIGHT//2 + 20))

    pygame.display.flip()
