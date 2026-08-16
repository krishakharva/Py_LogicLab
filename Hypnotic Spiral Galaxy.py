import pygame
import math
import colorsys

pygame.init()
W, H = 800, 800
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

t = 0
running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    t += 0.02
    for i in range(200):
        angle = i * 0.3 + t
        radius = 50 + i * 0.8
        x = W//2 + radius * math.cos(angle)
        y = H//2 + radius * math.sin(angle)
        
        hue = (i / 200 + t * 0.05) % 1.0
        color = colorsys.hsv_to_rgb(hue, 1.0, 0.9)
        color = tuple(int(c * 255) for c in color)
        
        size = 2 + 2 * math.sin(i * 0.2 + t)
        pygame.draw.circle(screen, color, (int(x), int(y)), int(size))
    
    pygame.display.flip()
    clock.tick(60)
pygame.quit()