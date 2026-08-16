import pygame
import random
import math
import os

os.environ['SDL_VIDEO_WINDOW_POS']='65,50'
pygame.init()
W, H = 900, 800
screen = pygame.display.set_mode((W, H), pygame.NOFRAME)
pygame.display.set_caption("Happy Independence Day!")
clock = pygame.time.Clock()

SAFFRON = (255, 153, 51)
WHITE = (255, 255, 255)
GREEN = (19, 136, 8)
NAVY_BLUE = (0, 0, 128)
GOLD = (255, 215, 0)
BLACK = (0, 0, 0)

class PartyPopperParticle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(3, 12)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed - 5
        self.color = color
        self.size = random.randint(3, 8)
        self.life = random.randint(40, 90)
        self.max_life = self.life
        self.gravity = 0.1
        self.shape = random.choice(['circle', 'square', 'line'])
        self.rotation = random.uniform(0, 2 * math.pi)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.vx *= 0.99
        self.life -= 1
        self.rotation += 0.05
        return self.life > 0
    
    def draw(self, screen):
        alpha = int(255 * (self.life / self.max_life))
        size = int(self.size * (self.life / self.max_life))
        if size <= 0:
            return
        
        color = (self.color[0], self.color[1], self.color[2])
        x, y = int(self.x), int(self.y)
        
        if self.shape == 'circle':
            pygame.draw.circle(screen, color, (x, y), max(1, size))
        elif self.shape == 'square':
            rect = pygame.Rect(x - size//2, y - size//2, size, size)
            pygame.draw.rect(screen, color, rect)
        else:
            end_x = x + size * 2 * math.cos(self.rotation)
            end_y = y + size * 2 * math.sin(self.rotation)
            pygame.draw.line(screen, color, (x, y), (int(end_x), int(end_y)), max(1, size//2))

def draw_text(text, x, y, color, size):
    font = pygame.font.Font(None, size)
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x, y))
    screen.blit(surface, rect)

poppers = []

def create_party_poppers(x, y):
    tricolor = [SAFFRON, WHITE, GREEN]
    for _ in range(150):
        poppers.append(PartyPopperParticle(x, y, random.choice(tricolor)))

running = True
frame = 0

create_party_poppers(W//2, H//2)

while running:
    screen.fill((5, 5, 20))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                x = random.randint(100, W-100)
                y = random.randint(100, H//2)
                create_party_poppers(x, y)
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            create_party_poppers(x, y)
    
    if random.random() < 0.02:
        x = random.randint(100, W-100)
        y = random.randint(100, H//2)
        create_party_poppers(x, y)
    
    flag_width = 400
    flag_height = 250
    flag_x = (W - flag_width) // 2
    flag_y = (H - flag_height) // 2 + 80
    
    stripe_h = flag_height // 3
    
    for i in range(flag_width):
        x = flag_x + i
        wave = int(4 * math.sin(i * 0.04 + frame * 0.02))
        
        pygame.draw.line(screen, SAFFRON, (x, flag_y + wave), (x, flag_y + stripe_h + wave), 3)
        pygame.draw.line(screen, WHITE, (x, flag_y + stripe_h + wave), (x, flag_y + 2*stripe_h + wave), 3)
        pygame.draw.line(screen, GREEN, (x, flag_y + 2*stripe_h + wave), (x, flag_y + 3*stripe_h + wave), 3)
    
    chakra_x = flag_x + flag_width // 2
    chakra_y = flag_y + flag_height // 2
    chakra_r = 20
    
    pygame.draw.circle(screen, NAVY_BLUE, (chakra_x, chakra_y), chakra_r, 2)
    pygame.draw.circle(screen, NAVY_BLUE, (chakra_x, chakra_y), 3)
    for i in range(24):
        theta = i * (2 * math.pi / 24) + frame * 0.015
        end_x = chakra_x + chakra_r * math.cos(theta)
        end_y = chakra_y + chakra_r * math.sin(theta)
        pygame.draw.line(screen, NAVY_BLUE, (chakra_x, chakra_y), (end_x, end_y), 1)
    
    for p in poppers[:]:
        if not p.update():
            poppers.remove(p)
        else:
            p.draw(screen)
    
    draw_text("HAPPY INDEPENDENCE DAY", W//2, 45, GOLD, 50)
    draw_text("15th August 2026", W//2, 80, WHITE, 28)
    draw_text("Jai Hind!", W//2, 110, WHITE, 38)
    
    frame += 1
    pygame.display.flip()
    clock.tick(60)

pygame.quit()