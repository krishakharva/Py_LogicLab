import pygame
import random
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = '230,50'

pygame.init()

WIDTH, HEIGHT = 500, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FLAPPY BIRD")
clock = pygame.time.Clock()

SKY_BLUE = (135, 206, 235)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
YELLOW = (255, 200, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
ORANGE = (255, 150, 0)

MENU = 0
PLAYING = 1
GAME_OVER = 2

bird_rect = pygame.Rect(100, HEIGHT//2, 30, 30)
bird_velocity = 0

pipes = []
pipe_width = 60
score = 0
high_score = 0

base_pipe_gap = 230      
base_pipe_speed = 2.5    
base_spawn_interval = 95 
base_gravity = 0.35      

pipe_gap = base_pipe_gap
pipe_speed = base_pipe_speed
spawn_interval = base_spawn_interval
gravity = base_gravity

def update_difficulty(score):
    global pipe_gap, pipe_speed, spawn_interval, gravity
    
    if score >= 50:
        pipe_gap = 125
        pipe_speed = 7.5
        spawn_interval = 38
        gravity = 0.72
    elif score >= 35:
        pipe_gap = 140
        pipe_speed = 6.5
        spawn_interval = 45
        gravity = 0.68
    elif score >= 25:
        pipe_gap = 155
        pipe_speed = 5.8
        spawn_interval = 52
        gravity = 0.62
    elif score >= 18:
        pipe_gap = 170
        pipe_speed = 5.0
        spawn_interval = 60
        gravity = 0.58
    elif score >= 12:
        pipe_gap = 185
        pipe_speed = 4.2
        spawn_interval = 72
        gravity = 0.52
    elif score >= 7:
        pipe_gap = 200
        pipe_speed = 3.5
        spawn_interval = 85
        gravity = 0.45
    elif score >= 3:
        pipe_gap = 215
        pipe_speed = 3.0
        spawn_interval = 90
        gravity = 0.40

font_title = pygame.font.Font(None, 72)
font_large = pygame.font.Font(None, 60)
font_medium = pygame.font.Font(None, 40)
font_small = pygame.font.Font(None, 30)

def create_pipe():
    height = random.randint(150, HEIGHT - pipe_gap - 150)
    return {
        'x': WIDTH,
        'top_height': height,
        'bottom_y': height + pipe_gap,
        'scored': False
    }

def reset_game():
    global bird_rect, bird_velocity, pipes, score, game_state, spawn_timer
    global pipe_gap, pipe_speed, spawn_interval, gravity
    
    bird_rect.y = HEIGHT//2
    bird_velocity = 0
    pipes = []
    score = 0
    spawn_timer = 0
    
    pipe_gap = base_pipe_gap
    pipe_speed = base_pipe_speed
    spawn_interval = base_spawn_interval
    gravity = base_gravity
    
    game_state = PLAYING

game_state = MENU
spawn_timer = 0
fade_alpha = 0

running = True
while running:
    screen.fill(SKY_BLUE)
    
    for i in range(3):
        cloud_x = (i * 200 + pygame.time.get_ticks() // 1000 * 20) % (WIDTH + 100) - 50
        cloud_y = 50 + i * 150
        for j in range(3):
            pygame.draw.circle(screen, (200, 220, 240), 
                             (cloud_x + j*20, cloud_y - j*10), 20 - j*5)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                if game_state == MENU:
                    game_state = PLAYING
                    reset_game()
                elif game_state == PLAYING:
                    bird_velocity = -10
                elif game_state == GAME_OVER:
                    if score > high_score:
                        high_score = score
                    game_state = MENU
    
    if game_state == PLAYING:
        update_difficulty(score)
        
        bird_velocity += gravity
        bird_rect.y += bird_velocity
        
        spawn_timer += 1
        if spawn_timer > spawn_interval:
            pipes.append(create_pipe())
            spawn_timer = 0
        
        for pipe in pipes[:]:
            pipe['x'] -= pipe_speed
            
            if not pipe['scored'] and pipe['x'] + pipe_width < bird_rect.x:
                pipe['scored'] = True
                score += 1
            
            if pipe['x'] + pipe_width < -50:
                pipes.remove(pipe)
        
        for pipe in pipes:
            if (bird_rect.x < pipe['x'] + pipe_width and
                bird_rect.x + bird_rect.width > pipe['x']):
                if (bird_rect.y < pipe['top_height'] or
                    bird_rect.y + bird_rect.height > pipe['bottom_y']):
                    if score > high_score:
                        high_score = score
                    game_state = GAME_OVER
        
        if bird_rect.y < 0 or bird_rect.y + bird_rect.height > HEIGHT:
            if score > high_score:
                high_score = score
            game_state = GAME_OVER
    
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, (pipe['x'], 0, pipe_width, pipe['top_height']))
        pygame.draw.rect(screen, DARK_GREEN, (pipe['x']-5, pipe['top_height']-20, pipe_width+10, 20))
        pygame.draw.rect(screen, (50, 200, 50), (pipe['x']+5, pipe['top_height']-15, 10, 10))
        
        pygame.draw.rect(screen, GREEN, (pipe['x'], pipe['bottom_y'], pipe_width, HEIGHT - pipe['bottom_y']))
        pygame.draw.rect(screen, DARK_GREEN, (pipe['x']-5, pipe['bottom_y'], pipe_width+10, 20))
        pygame.draw.rect(screen, (50, 200, 50), (pipe['x']+5, pipe['bottom_y']+5, 10, 10))
    
    if game_state != MENU:
        angle = bird_velocity * 2
        if angle > 45: angle = 45
        if angle < -45: angle = -45
        
        bird_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(bird_surface, YELLOW, (15, 15), 15)
        pygame.draw.circle(bird_surface, (255, 220, 0), (15, 12), 12)
        wing_y = 10 + (bird_velocity * 0.5)
        pygame.draw.ellipse(bird_surface, (255, 150, 0), (5, wing_y, 15, 10))
        pygame.draw.circle(bird_surface, WHITE, (20, 10), 6)
        pygame.draw.circle(bird_surface, BLACK, (22, 10), 3)
        pygame.draw.polygon(bird_surface, ORANGE, [(28, 13), (35, 15), (28, 17)])
        
        rotated_bird = pygame.transform.rotate(bird_surface, angle)
        screen.blit(rotated_bird, (bird_rect.x, bird_rect.y))
    
    if game_state == MENU:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 30))
        screen.blit(overlay, (0, 0))
        
        title_shadow = font_title.render("FLAPPY", True, (0, 0, 50))
        screen.blit(title_shadow, (WIDTH//2 - 160, 80))
        title = font_title.render("FLAPPY", True, WHITE)
        screen.blit(title, (WIDTH//2 - 163, 77))
        
        bird_title = font_title.render("BIRD", True, YELLOW)
        screen.blit(bird_title, (WIDTH//2 - 100, 150))
        
        start_text = font_medium.render("Press SPACE to Start", True, GREEN)
        screen.blit(start_text, (WIDTH//2 - 130, 500))
        
        if high_score > 0:
            high_text = font_small.render(f"High Score: {high_score}", True, YELLOW)
            screen.blit(high_text, (WIDTH//2 - 80, 560))
        
        instruction = font_small.render("Tap SPACE to fly", True, (150, 150, 200))
        screen.blit(instruction, (WIDTH//2 - 80, 620))
        
        esc_text = font_small.render("Press ESC to exit", True, (100, 100, 150))
        screen.blit(esc_text, (WIDTH//2 - 70, 750))
    
    elif game_state == PLAYING:
        score_shadow = font_large.render(str(score), True, (0, 0, 50))
        screen.blit(score_shadow, (WIDTH//2 - 18, 52))
        score_text = font_large.render(str(score), True, WHITE)
        screen.blit(score_text, (WIDTH//2 - 20, 50))
        
        if score > 0:
            high_indicator = font_small.render(f"Best: {high_score}", True, (150, 150, 200))
            screen.blit(high_indicator, (10, 10))
        
        esc_hint = font_small.render("ESC to exit", True, (80, 80, 120))
        screen.blit(esc_hint, (WIDTH - 100, 10))
    
    elif game_state == GAME_OVER:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        fade_alpha = min(180, fade_alpha + 5)
        overlay.set_alpha(fade_alpha)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        game_over_text = font_large.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (WIDTH//2 - 130, HEIGHT//2 - 150))
        
        score_display = font_medium.render(f"Score: {score}", True, WHITE)
        screen.blit(score_display, (WIDTH//2 - 80, HEIGHT//2 - 70))
        
        high_display = font_medium.render(f"Best: {high_score}", True, YELLOW)
        screen.blit(high_display, (WIDTH//2 - 70, HEIGHT//2 - 20))
        
        pulse = abs(pygame.time.get_ticks() % 1000 - 500) / 500
        color = (int(100 + 155 * pulse), 255, int(100 + 155 * pulse))
        restart_text = font_small.render("Press SPACE to continue", True, color)
        screen.blit(restart_text, (WIDTH//2 - 120, HEIGHT//2 + 100))
        
        esc_text = font_small.render("Press ESC to exit", True, (150, 150, 200))
        screen.blit(esc_text, (WIDTH//2 - 70, HEIGHT//2 + 160))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()