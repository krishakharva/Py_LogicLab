import pygame
import math
import random
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = '80,50'

pygame.init()

WIDTH, HEIGHT = 900, 1600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("Happy Birthday!")
clock = pygame.time.Clock()

BLACK = (8, 8, 20)
GOLD = (255, 215, 0)
DARK_GOLD = (200, 170, 0)
WHITE = (255, 255, 255)
CREAM = (255, 248, 220)
ROSE = (255, 200, 200)
DARK_GRAY = (50, 50, 50)

INTRO = 0
OPENING = 1
CARD = 2
CELEBRATION = 3

state = INTRO
timer = 0
progress = 0.0
float_offset = 0

particles = []
confetti = []

class Particle:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.randint(1, 2)
        self.speed = random.uniform(0.1, 0.3)
    
    def update(self):
        self.y -= self.speed
        if self.y < -50:
            self.y = HEIGHT + 50
            self.x = random.randint(0, WIDTH)
    
    def draw(self):
        pygame.draw.circle(screen, (255, 215, 0), (int(self.x), int(self.y)), self.size)

class Confetti:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-100, -20)
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(3, 6)
        self.size = random.randint(4, 8)
        self.rotation = random.uniform(0, 2 * math.pi)
        self.rot_speed = random.uniform(-0.1, 0.1)
        self.color = random.choice([GOLD, (255, 100, 150), (100, 200, 255), (100, 255, 100), (200, 100, 255), (255, 50, 50), (255, 255, 255)])
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rotation += self.rot_speed
        if self.y > HEIGHT + 50:
            self.y = random.randint(-100, -20)
            self.x = random.randint(0, WIDTH)
            self.color = random.choice([GOLD, (255, 100, 150), (100, 200, 255), (100, 255, 100), (200, 100, 255), (255, 50, 50), (255, 255, 255)])
    
    def draw(self):
        points = []
        size = self.size
        for i in range(4):
            angle = i * math.pi / 2 + self.rotation
            points.append((self.x + size * math.cos(angle), self.y + size * math.sin(angle)))
        pygame.draw.polygon(screen, self.color, points)

def draw_text(text, x, y, color, size, alpha=255):
    font = pygame.font.Font(None, size)
    surface = font.render(text, True, color)
    if alpha < 255:
        surface.set_alpha(alpha)
    rect = surface.get_rect(center=(x, y))
    screen.blit(surface, rect)

def draw_envelope(x, y, width, height, scale=1.0):
    if scale <= 0:
        return
    
    w = width * scale
    h = height * scale
    cx = x + w // 2
    
    shadow_rect = pygame.Rect(x + 15, y + 15, w, h)
    pygame.draw.rect(screen, (20, 20, 40), shadow_rect, border_radius=15)
    
    env_rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, CREAM, env_rect, border_radius=12)
    pygame.draw.rect(screen, GOLD, env_rect, 3, border_radius=12)
    
    flap_points = [(x, y), (cx, y + h * 0.35), (x + w, y)]
    pygame.draw.polygon(screen, ROSE, flap_points)
    pygame.draw.polygon(screen, GOLD, flap_points, 2)
    
    pygame.draw.circle(screen, GOLD, (int(cx), int(y + h * 0.18)), int(15 * scale))
    
    draw_text("FOR YOU", cx, y + h * 0.65, GOLD, int(40 * scale))

def draw_card(x, y, width, height, scale=1.0):
    if scale <= 0:
        return
    
    w = width * scale
    h = height * scale
    
    shadow_rect = pygame.Rect(x + 20, y + 20, w, h)
    pygame.draw.rect(screen, (20, 20, 40), shadow_rect, border_radius=20)
    
    card_rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, CREAM, card_rect, border_radius=20)
    pygame.draw.rect(screen, GOLD, card_rect, 4, border_radius=20)
    
    inner_rect = pygame.Rect(x + 20, y + 20, w - 40, h - 40)
    pygame.draw.rect(screen, ROSE, inner_rect, 2, border_radius=15)

for _ in range(30):
    particles.append(Particle())
for _ in range(30):
    confetti.append(Confetti())

running = True
while running:
    dt = clock.tick(60) / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    
    screen.fill(BLACK)
    
    for p in particles:
        p.update()
        p.draw()
    
    if state == INTRO:
        timer += dt
        
        float_offset = math.sin(timer * 0.5) * 15
        scale = min(1.0, timer / 1.0)
        
        env_width = 350
        env_height = 260
        x = WIDTH//2 - (env_width * scale) // 2
        y = HEIGHT//2 - (env_height * scale) // 2 + float_offset - 350
        
        draw_envelope(x, y, env_width, env_height, scale)
        
        if timer > 2.5:
            state = OPENING
            timer = 0
            progress = 0.0
    
    elif state == OPENING:
        timer += dt
        progress += 0.015
        progress = min(1.0, progress)
        
        ease = progress * progress * (3 - 2 * progress)
        
        env_width = 350
        env_height = 260
        env_scale = 1.0 - ease * 0.5
        x = WIDTH//2 - (env_width * env_scale) // 2
        y = HEIGHT//2 - (env_height * env_scale) // 2 - 350
        draw_envelope(x, y, env_width, env_height, env_scale)
        
        if ease > 0.2:
            card_scale = (ease - 0.2) / 0.8
            card_scale = min(1.0, card_scale * 1.1)
            card_width = 420
            card_height = 280
            cx = WIDTH//2 - (card_width * card_scale) // 2
            cy = HEIGHT//2 - (card_height * card_scale) // 2 - 350
            draw_card(cx, cy, card_width, card_height, card_scale)
        
        if ease > 0.4:
            alpha = int(255 * (ease - 0.4) / 0.6)
            draw_text("Opening your wish...", WIDTH//2, HEIGHT - 80, WHITE, 32, alpha)
        
        if progress >= 1.0:
            state = CARD
            timer = 0
    
    elif state == CARD:
        timer += dt
        
        card_width = 420
        card_height = 280
        cx = WIDTH//2 - card_width // 2
        cy = HEIGHT//2 - card_height // 2 - 350
        draw_card(cx, cy, card_width, card_height, 1.0)
        
        card_center_y = HEIGHT//2 - 350
        
        if timer < 1.0:
            alpha = int(255 * (timer / 1.0))
            draw_text("HAPPY", WIDTH//2, card_center_y - 70, DARK_GOLD, 40, alpha)
        elif timer < 2.0:
            draw_text("HAPPY", WIDTH//2, card_center_y - 70, DARK_GOLD, 40)
            alpha = int(255 * ((timer - 1.0) / 1.0))
            draw_text("BIRTHDAY!", WIDTH//2, card_center_y - 20, GOLD, 44, alpha)
        else:
            draw_text("HAPPY", WIDTH//2, card_center_y - 70, DARK_GOLD, 40)
            draw_text("BIRTHDAY!", WIDTH//2, card_center_y - 20, GOLD, 44)
            
            if timer < 3.5:
                alpha = int(255 * ((timer - 2.0) / 1.5))
                draw_text("Wishing you a day", WIDTH//2, card_center_y + 25, DARK_GRAY, 22, alpha)
                draw_text("filled with happiness,", WIDTH//2, card_center_y + 50, DARK_GRAY, 22, alpha)
                draw_text("laughter and", WIDTH//2, card_center_y + 75, DARK_GRAY, 22, alpha)
                draw_text("beautiful memories!", WIDTH//2, card_center_y + 100, DARK_GRAY, 22, alpha)
            else:
                draw_text("Wishing you a day", WIDTH//2, card_center_y + 25, DARK_GRAY, 22)
                draw_text("filled with happiness,", WIDTH//2, card_center_y + 50, DARK_GRAY, 22)
                draw_text("laughter and", WIDTH//2, card_center_y + 75, DARK_GRAY, 22)
                draw_text("beautiful memories!", WIDTH//2, card_center_y + 100, DARK_GRAY, 22)
        
        if timer > 5.0:
            state = CELEBRATION
            timer = 0
    
    elif state == CELEBRATION:
        timer += dt
        
        card_width = 420
        card_height = 280
        cx = WIDTH//2 - card_width // 2
        cy = HEIGHT//2 - card_height // 2 - 350
        draw_card(cx, cy, card_width, card_height, 1.0)
        
        card_center_y = HEIGHT//2 - 350
        
        draw_text("HAPPY", WIDTH//2, card_center_y - 70, DARK_GOLD, 40)
        draw_text("BIRTHDAY!", WIDTH//2, card_center_y - 20, GOLD, 44)
        draw_text("Wishing you a day", WIDTH//2, card_center_y + 25, DARK_GRAY, 22)
        draw_text("filled with happiness,", WIDTH//2, card_center_y + 50, DARK_GRAY, 22)
        draw_text("laughter and", WIDTH//2, card_center_y + 75, DARK_GRAY, 22)
        draw_text("beautiful memories!", WIDTH//2, card_center_y + 100, DARK_GRAY, 22)
        
        for c in confetti:
            c.update()
            c.draw()
    
    pygame.display.flip()

pygame.quit()