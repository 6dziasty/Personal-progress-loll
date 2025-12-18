import pygame
import sys
import time

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Speedrun Parkour - Postacie i poziomy + Jetpack")
clock = pygame.time.Clock()

# Kolory
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLUE = (50, 100, 255)
RED = (255, 0, 0)
BG = (20, 20, 20)
YELLOW = (255, 255, 0)
TELEPORT_COLOR = (200, 100, 255)
TRAMPOLINE_COLOR = (255, 165, 0)
SLOW_ZONE_COLOR = (100, 100, 100)
WALL_COLOR = (150, 150, 150)
SPIKES_COLOR = (255, 50, 50)
LASER_COLOR = (255, 0, 255)
ELEVATOR_COLOR = (100, 255, 255)

# Czcionki
font_big = pygame.font.SysFont(None, 72)
font_small = pygame.font.SysFont(None, 36)

# Stałe fizyki i ruchu
GRAVITY = 0.5
JUMP_BASE = -14
SPEED_BASE = 5
DASH_SPEED_BASE = 30
DASH_DURATION_BASE = 6
DASH_COOLDOWN_BASE = 2.0
SLIDE_SPEED_BASE = 15

# Postacie i ich umiejętności
characters = {
    "Skoczek": {
        "jump_mult": 1.5,
        "dash_cooldown_mult": 1.0,
        "slide_speed_mult": 1.0,
        "jetpack": False,
    },
    "Błyskawica": {
        "jump_mult": 1.0,
        "dash_cooldown_mult": 0.6,
        "slide_speed_mult": 1.0,
        "jetpack": False,
    },
    "Kontroler": {
        "jump_mult": 1.0,
        "dash_cooldown_mult": 1.0,
        "slide_speed_mult": 0.5,  # wolniejszy spadek
        "jetpack": False,
    },
    "Jetpack": {  # NOWA POSTAĆ
        "jump_mult": 1.0,
        "dash_cooldown_mult": 1.0,
        "slide_speed_mult": 1.0,
        "jetpack": True,
        "jetpack_fuel": 2.0  # sekundy latania
    },
}

# Klasy przeszkód i mechanik (bez zmian)
class MovingPlatform:
    def __init__(self, x, y, width, height, range_x, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.start_x = x
        self.range_x = range_x
        self.speed = speed
        self.direction = 1
    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.x > self.start_x + self.range_x or self.rect.x < self.start_x:
            self.direction *= -1
    def draw(self, surface, camera_offset):
        pygame.draw.rect(surface, GREEN, (self.rect.x - camera_offset, self.rect.y, self.rect.width, self.rect.height))

class Teleport:
    def __init__(self, rect, target_pos):
        self.rect = rect
        self.target_pos = target_pos
    def draw(self, surface, camera_offset):
        pygame.draw.rect(surface, TELEPORT_COLOR, (self.rect.x - camera_offset, self.rect.y, self.rect.width, self.rect.height))

class Trampoline:
    def __init__(self, rect, bounce_power):
        self.rect = rect
        self.bounce_power = bounce_power
    def draw(self, surface, camera_offset):
        pygame.draw.rect(surface, TRAMPOLINE_COLOR, (self.rect.x - camera_offset, self.rect.y, self.rect.width, self.rect.height))

class SlowZone:
    def __init__(self, rect, slow_factor):
        self.rect = rect
        self.slow_factor = slow_factor
    def draw(self, surface, camera_offset):
        pygame.draw.rect(surface, SLOW_ZONE_COLOR, (self.rect.x - camera_offset, self.rect.y, self.rect.width, self.rect.height))

class Spikes:
    def __init__(self, rect):
        self.rect = rect
    def draw(self, surface, camera_offset):
        pygame.draw.rect(surface, SPIKES_COLOR, (self.rect.x - camera_offset, self.rect.y, self.rect.width, self.rect.height))

class Elevator:
    def __init__(self, x, y, width, height, range_y, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.start_y = y
        self.range_y = range_y
        self.speed = speed
        self.direction = 1
    def update(self):
        self.rect.y += self.speed * self.direction
        if self.rect.y > self.start_y + self.range_y or self.rect.y < self.start_y:
            self.direction *= -1
    def draw(self, surface, camera_offset):
        pygame.draw.rect(surface, ELEVATOR_COLOR, (self.rect.x - camera_offset, self.rect.y, self.rect.width, self.rect.height))

class Laser:
    def __init__(self, rect, active_time=1, inactive_time=1):
        self.rect = rect
        self.active_time = active_time
        self.inactive_time = inactive_time
        self.timer = 0
        self.active = True
    def update(self, dt):
        self.timer += dt
        cycle = self.active_time + self.inactive_time
        if self.timer > cycle:
            self.timer -= cycle
        self.active = self.timer <= self.active_time
    def draw(self, surface, camera_offset):
        color = LASER_COLOR if self.active else (80, 0, 80)
        pygame.draw.rect(surface, color, (self.rect.x - camera_offset, self.rect.y, self.rect.width, self.rect.height))

# Poziomy - dodaję nowy poziom nr 3
levels = [
    {
        "platforms": [
            pygame.Rect(0, 550, 1400, 50),
            pygame.Rect(300, 500, 60, 20),
            pygame.Rect(600, 440, 60, 20),
            pygame.Rect(900, 370, 60, 20),
            pygame.Rect(1150, 320, 60, 20),
            pygame.Rect(1400, 280, 60, 20),
        ],
        "moving_platforms": [
            MovingPlatform(1600, 250, 80, 20, 200, 3),
            MovingPlatform(1900, 350, 80, 20, 150, 4),
        ],
        "teleports": [
            Teleport(pygame.Rect(400, 530, 40, 20), (700, 400)),
            Teleport(pygame.Rect(1200, 300, 40, 20), (1600, 230)),
        ],
        "trampolines": [
            Trampoline(pygame.Rect(750, 420, 60, 10), bounce_power=-20),
        ],
        "slow_zones": [
            SlowZone(pygame.Rect(850, 550, 50, 50), slow_factor=0.5),
        ],
        "spikes": [
            Spikes(pygame.Rect(1000, 550, 100, 20)),
        ],
        "elevators": [
            Elevator(1800, 300, 80, 20, 150, 2),
        ],
        "lasers": [
            Laser(pygame.Rect(1300, 200, 10, 100)),
        ],
        "goal": pygame.Rect(2000, 200, 40, 40)
    },
    {
        "platforms": [
            pygame.Rect(0, 550, 1500, 50),
            pygame.Rect(400, 500, 50, 20),
            pygame.Rect(800, 450, 50, 20),
            pygame.Rect(1200, 400, 50, 20),
            pygame.Rect(1600, 350, 50, 20),
            pygame.Rect(1900, 300, 50, 20),
            pygame.Rect(2200, 260, 50, 20),
            pygame.Rect(2500, 220, 50, 20),
        ],
        "moving_platforms": [
            MovingPlatform(1400, 300, 80, 20, 300, 4),
            MovingPlatform(1800, 350, 80, 20, 250, 5),
            MovingPlatform(2300, 270, 80, 20, 200, 3),
        ],
        "teleports": [
            Teleport(pygame.Rect(450, 480, 40, 20), (1100, 360)),
            Teleport(pygame.Rect(2000, 280, 40, 20), (2400, 230)),
        ],
        "trampolines": [
            Trampoline(pygame.Rect(1000, 390, 60, 10), bounce_power=-22),
            Trampoline(pygame.Rect(2300, 210, 60, 10), bounce_power=-24),
        ],
        "slow_zones": [
            SlowZone(pygame.Rect(1600, 550, 50, 50), slow_factor=0.4),
            SlowZone(pygame.Rect(2400, 260, 50, 50), slow_factor=0.3),
        ],
        "spikes": [
            Spikes(pygame.Rect(1500, 550, 100, 20)),
            Spikes(pygame.Rect(2500, 220, 100, 20)),
        ],
        "elevators": [
            Elevator(2600, 400, 80, 20, 150, 3),
        ],
        "lasers": [
            Laser(pygame.Rect(1700, 200, 10, 150)),
            Laser(pygame.Rect(2200, 250, 10, 100)),
        ],
        "goal": pygame.Rect(2700, 180, 40, 40)
    },
    # NOWY POZIOM 3 - TRUDNY I Z WIELOMA MECHANIKAMI
    {
        "platforms": [
            pygame.Rect(0, 550, 1800, 50),
            pygame.Rect(350, 480, 70, 20),
            pygame.Rect(750, 420, 70, 20),
            pygame.Rect(1200, 370, 70, 20),
            pygame.Rect(1600, 330, 70, 20),
            pygame.Rect(2000, 300, 70, 20),
            pygame.Rect(2300, 270, 50, 20),
            pygame.Rect(2600, 240, 50, 20),
            pygame.Rect(2900, 210, 50, 20),
        ],
        "moving_platforms": [
            MovingPlatform(900, 400, 90, 20, 400, 4),
            MovingPlatform(1400, 350, 80, 20, 300, 5),
            MovingPlatform(1900, 320, 80, 20, 250, 3),
            MovingPlatform(2100, 290, 60, 20, 350, 3),
        ],
        "teleports": [
            Teleport(pygame.Rect(400, 460, 40, 20), (1100, 340)),
            Teleport(pygame.Rect(2500, 220, 40, 20), (2800, 190)),
        ],
        "trampolines": [
            Trampoline(pygame.Rect(1300, 360, 60, 10), bounce_power=-25),
            Trampoline(pygame.Rect(2250, 260, 60, 10), bounce_power=-28),
        ],
        "slow_zones": [
            SlowZone(pygame.Rect(1700, 550, 60, 60), slow_factor=0.4),
            SlowZone(pygame.Rect(2400, 270, 50, 50), slow_factor=0.3),
        ],
        "spikes": [
            Spikes(pygame.Rect(1500, 550, 120, 20)),
            Spikes(pygame.Rect(2700, 230, 120, 20)),
        ],
        "elevators": [
            Elevator(3000, 300, 80, 20, 150, 3),
        ],
        "lasers": [
            Laser(pygame.Rect(1800, 250, 10, 150)),
            Laser(pygame.Rect(2200, 280, 10, 120)),
            Laser(pygame.Rect(2500, 260, 10, 100)),
        ],
        "goal": pygame.Rect(3200, 180, 40, 40)
    },
]

def draw_text_center(text, font, color, surface, y):
    txt = font.render(text, True, color)
    x = (SCREEN_WIDTH - txt.get_width()) // 2
    surface.blit(txt, (x, y))

def character_select():
    selected = 0
    names = list(characters.keys())
    while True:
        screen.fill(BG)
        draw_text_center("Wybierz postać:", font_big, WHITE, screen, 100)
        for i, name in enumerate(names):
            color = YELLOW if i == selected else WHITE
            desc = ""
            if name == "Skoczek":
                desc = "Wyższy skok"
            elif name == "Błyskawica":
                desc = "Krótszy cooldown dash"
            elif name == "Kontroler":
                desc = "Wolniejszy spadek"
            elif name == "Jetpack":
                desc = "Jetpack - latanie chwilowe"
            txt = font_small.render(f"{name} - {desc}", True, color)
            screen.blit(txt, (SCREEN_WIDTH//2 - txt.get_width()//2, 250 + i*50))
        draw_text_center("Strzałki ↑ ↓, ENTER - wybierz", font_small, WHITE, screen, 400)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    selected = (selected - 1) % len(names)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    selected = (selected + 1) % len(names)
                elif event.key == pygame.K_RETURN:
                    return names[selected]

        clock.tick(60)

def menu(unlocked_levels):
    selected = 0
    while True:
        screen.fill(BG)
        draw_text_center("Wybierz poziom:", font_big, WHITE, screen, 100)
        for i in range(len(levels)):
            color = YELLOW if i == selected else WHITE
            status = "Odblokowany" if i in unlocked_levels else "Zablokowany"
            txt = font_small.render(f"{i+1}. Poziom - {status}", True, color)
            screen.blit(txt, (SCREEN_WIDTH//2 - txt.get_width()//2, 250 + i*50))
        draw_text_center("Strzałki ↑ ↓, ENTER, ESC - wyjście", font_small, WHITE, screen, 400)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    selected = (selected - 1) % len(levels)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    selected = (selected + 1) % len(levels)
                elif event.key == pygame.K_RETURN:
                    if selected in unlocked_levels:
                        return selected
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        clock.tick(60)

def countdown():
    for i in range(3, 0, -1):
        screen.fill(BG)
        txt = font_big.render(str(i), True, WHITE)
        screen.blit(txt, (SCREEN_WIDTH//2 - txt.get_width()//2, SCREEN_HEIGHT//2 - txt.get_height()//2))
        pygame.display.flip()
        time.sleep(1)
    screen.fill(BG)
    start_txt = font_big.render("START!", True, GREEN)
    screen.blit(start_txt, (SCREEN_WIDTH//2 - start_txt.get_width()//2, SCREEN_HEIGHT//2 - start_txt.get_height()//2))
    pygame.display.flip()
    time.sleep(1)

def game(level_index, unlocked_levels, char_name):
    char = characters[char_name]
    jump_power = JUMP_BASE * char["jump_mult"]
    dash_cooldown = DASH_COOLDOWN_BASE * char["dash_cooldown_mult"]
    slide_speed = SLIDE_SPEED_BASE * char["slide_speed_mult"]

    player = pygame.Rect(100, 500, 40, 40)
    velocity_y = 0
    on_ground = False
    can_double_jump = False

    dash_time = -dash_cooldown
    dashing = False
    dash_frames_left = 0
    penalty = 0
    win = False

    level = levels[level_index]

    platforms = level["platforms"]
    moving_platforms = level["moving_platforms"]
    teleports = level["teleports"]
    trampolines = level["trampolines"]
    slow_zones = level["slow_zones"]
    spikes = level.get("spikes", [])
    elevators = level.get("elevators", [])
    lasers = level.get("lasers", [])
    goal = level["goal"]

    start_time = time.time()
    sliding = False

    # Dla jetpacka
    jetpack_fuel = char.get("jetpack_fuel", 0)
    jetpack_fuel_left = jetpack_fuel
    jetpack_active = False

    while True:
        dt = clock.tick(60) / 1000
        screen.fill(BG)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        # Dash
        if keys[pygame.K_d] and not dashing and time.time() - dash_time >= dash_cooldown:
            dashing = True
            dash_frames_left = DASH_DURATION_BASE
            dash_time = time.time()

        if dashing:
            player.x += DASH_SPEED_BASE
            dash_frames_left -= 1
            if dash_frames_left <= 0:
                dashing = False
        else:
            move_speed = SPEED_BASE
            # Spowolnienie w slow zones
            slow_factor = 1.0
            for sz in slow_zones:
                if player.colliderect(sz.rect):
                    slow_factor = sz.slow_factor
                    break
            move_speed = int(move_speed * slow_factor)
            if keys[pygame.K_LEFT]:
                player.x -= move_speed
            if keys[pygame.K_RIGHT]:
                player.x += move_speed

        # Jetpack (nowa mechanika)
        if char["jetpack"]:
            if keys[pygame.K_SPACE] and jetpack_fuel_left > 0:
                velocity_y = -8  # unoszenie
                jetpack_active = True
                jetpack_fuel_left -= dt
            else:
                jetpack_active = False
                velocity_y += GRAVITY  # grawitacja działa normalnie, ale wolniej przy "Kontroler"

            # Jeśli na ziemi to tankuj jetpack
            on_ground_old = on_ground
            if on_ground and not on_ground_old:
                jetpack_fuel_left = jetpack_fuel
        else:
            # Skok i double jump dla innych postaci
            if keys[pygame.K_SPACE]:
                if on_ground:
                    velocity_y = jump_power
                    can_double_jump = True
                elif can_double_jump:
                    velocity_y = jump_power
                    can_double_jump = False
            # Spadek
            velocity_y += GRAVITY * (char["slide_speed_mult"])

        # Ślizg w powietrzu
        sliding = False
        if not on_ground and keys[pygame.K_s] and not char["jetpack"]:
            velocity_y += slide_speed
            sliding = True

        player.y += velocity_y

        # Aktualizacja ruchomych platform
        for mp in moving_platforms:
            mp.update()

        # Aktualizacja wind
        for el in elevators:
            el.update()

        # Aktualizacja laserów
        for laser in lasers:
            laser.update(dt)

        # Kolizje z platformami i windami
        prev_on_ground = on_ground
        on_ground = False
        for plat in platforms + [mp.rect for mp in moving_platforms] + [el.rect for el in elevators]:
            if player.colliderect(plat) and velocity_y >= 0:
                player.bottom = plat.top
                velocity_y = 0
                on_ground = True

        if on_ground and not prev_on_ground:
            can_double_jump = False
            if char["jetpack"]:
                jetpack_fuel_left = jetpack_fuel  # tankowanie jetpacka po lądowaniu

        # Kolizja ze spike'ami (śmierć)
        for spike in spikes:
            if player.colliderect(spike.rect):
                player.x = 100
                player.y = 500
                velocity_y = 0
                penalty += 5
                jetpack_fuel_left = jetpack_fuel  # reset paliwa jetpacka

        # Kolizja z laserami (śmierć jak laser aktywny)
        for laser in lasers:
            if laser.active and player.colliderect(laser.rect):
                player.x = 100
                player.y = 500
                velocity_y = 0
                penalty += 5
                jetpack_fuel_left = jetpack_fuel

        # Teleporty
        for tele in teleports:
            if player.colliderect(tele.rect):
                player.x, player.y = tele.target_pos
                velocity_y = 0

        # Trampoliny
        for tramp in trampolines:
            if player.colliderect(tramp.rect) and velocity_y >= 0:
                velocity_y = tramp.bounce_power

        # Death zone
        if player.y > SCREEN_HEIGHT:
            player.x = 100
            player.y = 500
            velocity_y = 0
            penalty += 5
            jetpack_fuel_left = jetpack_fuel

        # Kamera
        camera_offset = player.x - 100

        # Meta
        if player.colliderect(goal) and not win:
            win = True
            total = time.time() - start_time + penalty
            if level_index + 1 < len(levels):
                unlocked_levels.add(level_index + 1)

        # Timer
        if not win:
            elapsed = time.time() - start_time + penalty
        else:
            elapsed = total
            win_msg = font_big.render("Speedrun zakończony!", True, YELLOW)
            screen.blit(win_msg, (SCREEN_WIDTH // 2 - win_msg.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

        timer = font_small.render(f"Czas: {elapsed:.2f}s", True, WHITE)
        screen.blit(timer, (10, 10))

        dash_status = "Gotowy" if time.time() - dash_time >= dash_cooldown else "Ładuje..."
        dash_text = font_small.render(f"Dash: {dash_status}", True, YELLOW)
        screen.blit(dash_text, (10, 50))

        # Paliwo jetpacka (jeśli wybrany)
        if char["jetpack"]:
            fuel_ratio = jetpack_fuel_left / jetpack_fuel
            fuel_bar_length = 100
            pygame.draw.rect(screen, WHITE, (10, 80, fuel_bar_length, 10), 2)
            pygame.draw.rect(screen, YELLOW, (10, 80, int(fuel_bar_length * fuel_ratio), 10))
            jetpack_text = font_small.render("Jetpack paliwo", True, YELLOW)
            screen.blit(jetpack_text, (10, 95))

        # Rysowanie
        pygame.draw.rect(screen, BLUE, (player.x - camera_offset, player.y, player.width, player.height))
        for plat in platforms:
            pygame.draw.rect(screen, GREEN, (plat.x - camera_offset, plat.y, plat.width, plat.height))
        for mp in moving_platforms:
            mp.draw(screen, camera_offset)
        for tele in teleports:
            tele.draw(screen, camera_offset)
        for tramp in trampolines:
            tramp.draw(screen, camera_offset)
        for sz in slow_zones:
            sz.draw(screen, camera_offset)
        for spike in spikes:
            spike.draw(screen, camera_offset)
        for el in elevators:
            el.draw(screen, camera_offset)
        for laser in lasers:
            laser.draw(screen, camera_offset)
        pygame.draw.rect(screen, RED, (goal.x - camera_offset, goal.y, goal.width, goal.height))

        pygame.display.flip()

        if win:
            time.sleep(2)
            return True

def main():
    unlocked_levels = {0}
    while True:
        char_name = character_select()
        level_index = menu(unlocked_levels)
        countdown()
        game(level_index, unlocked_levels, char_name)

if __name__ == "__main__":
    main()
