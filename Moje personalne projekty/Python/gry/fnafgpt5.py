

import pygame
import sys
import random

# --- Ustawienia ---
WIDTH, HEIGHT = 800, 480
FPS = 30

# prędkość animatronika (im wyższa, tym szybciej idzie)
ANIM_SPEED = 0.5  # piksele na klatkę

# dystans od korytarza do biurka w 'pojedynczym pomiarze'
HALLWAY_START_X = WIDTH + 50
HALLWAY_END_X = WIDTH // 2 + 50

# --- Kolory ---
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (40,40,40)
DARK = (20,20,30)
YELLOW = (230,230,120)
RED = (200,0,0)
GREEN = (0,200,0)
BLUE = (0,0,200)

# --- Inicjalizacja pygame ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FNAF - starter (luźny)")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)
bigfont = pygame.font.SysFont(None, 72)

# --- Stan gry ---
in_camera = False
left_door_closed = False
right_door_closed = False
light_on = False
game_over = False

# Animatronik: będzie się pojawiał od czasu do czasu i przesuwał w stronę biura.
class Animatronic:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = HALLWAY_START_X
        self.y = HEIGHT//2 + 20
        self.active = False
        # losowy delay zanim pojawi się (w sekundach)
        self.spawn_delay = random.randint(3, 10) * FPS
        self.counter = 0
        # łatwy tryb: kolor i rozmiar prosty
        self.color = (random.randint(80,200), 20, random.randint(20,80))
        self.width = 60
        self.height = 100

    def start(self):
        self.active = True

    def update(self):
        if not self.active:
            self.counter += 1
            if self.counter >= self.spawn_delay:
                self.start()
            return

        self.x -= ANIM_SPEED
        # jeśli przeszedł za bardzo, zresetuj i ustaw delay
        if self.x < -200:
            self.reset()

    def draw(self, surface, camera_view=False):
        if not self.active:
            return
        # rysujemy prostą sylwetkę
        rect = pygame.Rect(int(self.x), int(self.y - self.height//2), self.width, self.height)
        if camera_view:
            # w kamerze widzimy go trochę bliżej i bardziej "detalicznie"
            pygame.draw.rect(surface, self.color, rect)
            # oczy
            eye_w = 8
            eye_h = 8
            pygame.draw.circle(surface, WHITE, (int(self.x+15), int(self.y-10)), eye_w)
            pygame.draw.circle(surface, WHITE, (int(self.x+45), int(self.y-10)), eye_w)
        else:
            # w biurze rysujemy go małego jako sylwetkę w drzwiach/korytarzu
            pygame.draw.rect(surface, (80,80,80), rect)

    def reached_office(self):
        # kryterium: x blisko biurka
        return self.x <= HALLWAY_END_X

anim = Animatronic()

# pomocnicze rysowanie tekstu
def draw_text(surf, text, x, y, color=WHITE, font_obj=None):
    if font_obj is None:
        font_obj = font
    img = font_obj.render(text, True, color)
    surf.blit(img, (x,y))

# --- Ekrany ---
def draw_office():
    """Rysuje biuro gracza"""
    screen.fill(DARK)
    # biurko
    desk_rect = pygame.Rect(WIDTH//2 - 120, HEIGHT//2 + 60, 240, 80)
    pygame.draw.rect(screen, (70,50,30), desk_rect)
    # krzesło
    pygame.draw.rect(screen, (30,30,30), (WIDTH//2 - 20, HEIGHT//2 + 20, 40, 40))
    # okno kamery (jeśli kamera jest on -> pokaz mini podgląd korytarza)
    pygame.draw.rect(screen, (10,10,10), (50,50,300,200))
    draw_text(screen, "Kamera: ".upper() + ("ON" if in_camera else "OFF"), 60, 60)
    # drzwi po bokach
    left_door = pygame.Rect(0, HEIGHT//2 - 80, 60, 160)
    right_door = pygame.Rect(WIDTH-60, HEIGHT//2 - 80, 60, 160)
    pygame.draw.rect(screen, (50,50,60), left_door)
    pygame.draw.rect(screen, (50,50,60), right_door)
    # zaznacz zamknięte drzwi
    if left_door_closed:
        pygame.draw.rect(screen, (20,20,80), left_door)
    if right_door_closed:
        pygame.draw.rect(screen, (20,20,80), right_door)
    # światła przy drzwiach (małe pola)
    if light_on:
        pygame.draw.rect(screen, YELLOW, (left_door.right+5, left_door.top+20, 20, 20))
        pygame.draw.rect(screen, YELLOW, (right_door.left-25, right_door.top+20, 20, 20))
    # rysuj animatronika na trasie (jeśli jest aktywny)
    anim.draw(screen, camera_view=False)
    # statusy
    draw_text(screen, f"Sterowanie: [C]amera [A]LeweDrzwi [D]PraweDrzwi [L]Light", 10, HEIGHT-30)
    draw_text(screen, f"Kamera: {'ON' if in_camera else 'OFF'}", WIDTH-220, 10)
    draw_text(screen, f"Left door: {'CLOSED' if left_door_closed else 'OPEN'}", WIDTH-220, 30)
    draw_text(screen, f"Right door: {'CLOSED' if right_door_closed else 'OPEN'}", WIDTH-220, 50)
    draw_text(screen, f"Light: {'ON' if light_on else 'OFF'}", WIDTH-220, 70)

def draw_camera_view():
    """Prosty widok z kamery — pokazuje korytarz i animatronika"""
    screen.fill(BLACK)
    # rama kamery
    cam_rect = pygame.Rect(60,40, WIDTH-120, HEIGHT-80)
    pygame.draw.rect(screen, (10,10,30), cam_rect)
    # korytarz - proste perspektywy
    pygame.draw.rect(screen, (30,30,40), (cam_rect.left+20, cam_rect.top+20, cam_rect.width-40, cam_rect.height-40))
    # rysujemy animatronika widocznego w kadrze (przesuniętego względem sceny biura)
    # mapujemy jego x do kamery: jeśli poza kadr -> nie rysujemy
    # w prosty sposób: jeśli anim.x < HALLWAY_START_X and > -100 rysujemy w oknie
    if anim.active:
        # oblicz jego pozycję względną do kamery
        rel = (anim.x - HALLWAY_END_X) / (HALLWAY_START_X - HALLWAY_END_X)  # 0..1
        cam_x = cam_rect.left + int(rel * (cam_rect.width - 100)) + 20
        cam_y = cam_rect.top + cam_rect.height//2
        # prosty efekt - bardziej widoczny gdy blisko
        size = 30 + int((1 - rel) * 80)
        rect = pygame.Rect(cam_x, cam_y - size//2, 40, size)
        pygame.draw.rect(screen, anim.color, rect)
        # oczy
        pygame.draw.circle(screen, WHITE, (rect.left+10, rect.top+10), 5)
        pygame.draw.circle(screen, WHITE, (rect.left+30, rect.top+10), 5)
    # teksty
    draw_text(screen, "CAMERA VIEW (C aby wyjść)", 70, 50)
    draw_text(screen, "Animatronik: " + ("AKTYWNY" if anim.active else "brak"), 70, 70)

def draw_jumpscare():
    screen.fill(RED)
    t = bigfont.render("JUMPSCARE!", True, BLACK)
    screen.blit(t, (WIDTH//2 - t.get_width()//2, HEIGHT//2 - t.get_height()//2))

# --- Główna pętla gry ---
def main():
    global in_camera, left_door_closed, right_door_closed, light_on, game_over

    scare_timer = 0
    JUMPSCARE_DURATION = FPS * 2  # 2 sekundy

    running = True
    while running:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
                if event.key == pygame.K_c:
                    in_camera = not in_camera
                if event.key == pygame.K_a:
                    left_door_closed = not left_door_closed
                if event.key == pygame.K_d:
                    right_door_closed = not right_door_closed
                if event.key == pygame.K_l:
                    light_on = not light_on

        if not running:
            break

        # Update
        if not game_over:
            anim.update()

            # jeśli anim dotrze do biura, sprawdź warunki
            if anim.active and anim.reached_office():
                # jeśli którakolwiek z drzwii jest zamknięta -> anim zostaje zatrzymany (nie jumpscare)
                if left_door_closed or right_door_closed:
                    # anim przy drzwiach -> cofamy go (symulacja: wraca do korytarza)
                    anim.x = HALLWAY_START_X + random.randint(10,150)
                    anim.active = False
                    anim.counter = 0
                    anim.spawn_delay = random.randint(5, 12) * FPS
                else:
                    # brak zamkniętych drzwi -> jumpscare
                    game_over = True
                    scare_timer = 0

        # Rysowanie
        if game_over:
            draw_jumpscare()
            scare_timer += 1
            if scare_timer >= JUMPSCARE_DURATION:
                # reset gry po jumpscare
                anim.reset()
                game_over = False
        else:
            if in_camera:
                draw_camera_view()
            else:
                draw_office()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()