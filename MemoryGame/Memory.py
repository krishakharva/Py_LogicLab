import pygame
import random
import os
import math

os.environ['SDL_VIDEO_WINDOW_POS'] = '235,50'

pygame.init()

WIDTH, HEIGHT = 500, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("MEMORY GAME")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (8, 8, 30)

FRUITS = [
    "🍒", "🍎", "🥝", "🍊",
    "🥭", "🍇", "🍓", "🍉"
]

ROWS = 4
COLS = 4
TOTAL_PAIRS = 8
TOTAL_CARDS = TOTAL_PAIRS * 2

TILE_SIZE = 100
MARGIN = 15
START_X = (WIDTH - (COLS * (TILE_SIZE + MARGIN) - MARGIN)) // 2
START_Y = 130

grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
matched = [[False for _ in range(COLS)] for _ in range(ROWS)]
animating = [[False for _ in range(COLS)] for _ in range(ROWS)]
animation_progress = [[0.0 for _ in range(COLS)] for _ in range(ROWS)]
first_choice = None
second_choice = None
score = 0
moves = 0
waiting = False
wait_timer = 0
hover_pos = None

particles = []
game_won = False
win_timer = 0
celebration_active = False

font = pygame.font.Font(None, 28)
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 36)

class Particle:
    def __init__(self, x, y, color=None, size=None, vx=None, vy=None):
        self.x = x
        self.y = y
        if vx is not None:
            self.vx = vx
        else:
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 10)
            self.vx = math.cos(angle) * speed
        if vy is not None:
            self.vy = vy
        else:
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 10)
            self.vy = math.sin(angle) * speed - 3
        self.life = random.randint(40, 80)
        self.max_life = self.life
        if color:
            self.color = color
        else:
            self.color = random.choice([
                (255, 50, 50), (255, 150, 50), (255, 255, 50),
                (50, 255, 50), (50, 150, 255), (255, 50, 255),
                (255, 200, 100), (100, 255, 200)
            ])
        self.size = size if size else random.randint(3, 8)
        self.gravity = 0.15
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.vx *= 0.99
        self.life -= 1
        return self.life > 0
    
    def draw(self, screen):
        alpha = int(255 * (self.life / self.max_life))
        color = (self.color[0], self.color[1], self.color[2], alpha)
        size = int(self.size * (self.life / self.max_life))
        if size > 0:
            pygame.draw.circle(screen, color[:3], (int(self.x), int(self.y)), max(1, size))

def create_grid():
    available_fruits = FRUITS[:TOTAL_PAIRS]
    fruits = available_fruits * 2
    random.shuffle(fruits)
    
    card_index = 0
    for i in range(ROWS):
        for j in range(COLS):
            grid[i][j] = fruits[card_index]
            card_index += 1

def draw_card(x, y, card_value, is_revealed, is_matched, is_animating, progress, is_hover):
    if is_animating:
        scale = 1.0 - progress
        if scale < 0: scale = 0
        new_size = int(TILE_SIZE * scale)
        if new_size < 5:
            return
        offset = (TILE_SIZE - new_size) // 2
        x += offset
        y += offset
        
        pygame.draw.rect(screen, (40, 35, 80), (x, y, new_size, new_size), border_radius=10)
        pygame.draw.rect(screen, (150, 100, 255, int(100 * scale)), 
                        (x, y, new_size, new_size), 2, border_radius=10)
        
        try:
            font_size = int(new_size * 0.55)
            emoji_font = pygame.font.SysFont('segoeuiemoji', font_size)
            fruit_text = emoji_font.render(card_value, True, WHITE)
            text_rect = fruit_text.get_rect(center=(x + new_size//2, y + new_size//2 + 2))
            screen.blit(fruit_text, text_rect)
        except:
            fallback_font = pygame.font.Font(None, font_size)
            fruit_text = fallback_font.render(card_value, True, WHITE)
            text_rect = fruit_text.get_rect(center=(x + new_size//2, y + new_size//2 + 2))
            screen.blit(fruit_text, text_rect)
        
        if scale < 0.3:
            for _ in range(8):
                px = x + random.randint(0, new_size)
                py = y + random.randint(0, new_size)
                color = random.choice([(255, 200, 100), (255, 100, 200), (100, 200, 255)])
                size = random.randint(2, 6)
                pygame.draw.circle(screen, color, (px, py), size)
        return
    
    if is_matched:
        return
    
    if is_revealed:
        colors = [
            (180, 100, 255),
            (100, 180, 255),
            (255, 120, 200),
            (100, 255, 200)
        ]
        color_index = (hash(card_value) % 4)
        base_color = colors[color_index]
        
        for i in range(8):
            alpha = 25 - i * 2
            pygame.draw.rect(screen, (base_color[0], base_color[1], base_color[2], alpha), 
                           (x-i, y-i, TILE_SIZE+i*2, TILE_SIZE+i*2), 2, border_radius=15)
        
        pygame.draw.rect(screen, (50, 45, 90), (x, y, TILE_SIZE, TILE_SIZE), border_radius=15)
        pygame.draw.rect(screen, base_color, (x, y, TILE_SIZE, TILE_SIZE), 3, border_radius=15)
        
        for i in range(3):
            sparkle_x = x + 15 + i * 35
            sparkle_y = y + 15 + (i * 25) % 60
            pygame.draw.circle(screen, (255, 255, 255, 50), (sparkle_x, sparkle_y), 3)
        
        try:
            font_size = int(TILE_SIZE * 0.55)
            emoji_font = pygame.font.SysFont('segoeuiemoji', font_size)
            fruit_text = emoji_font.render(card_value, True, WHITE)
            text_rect = fruit_text.get_rect(center=(x + TILE_SIZE//2, y + TILE_SIZE//2 + 2))
            screen.blit(fruit_text, text_rect)
        except:
            fallback_font = pygame.font.Font(None, font_size)
            fruit_text = fallback_font.render(card_value, True, WHITE)
            text_rect = fruit_text.get_rect(center=(x + TILE_SIZE//2, y + TILE_SIZE//2 + 2))
            screen.blit(fruit_text, text_rect)
    else:
        if is_hover:
            for i in range(5):
                alpha = 40 - i * 6
                pygame.draw.rect(screen, (150, 100, 255, alpha), 
                               (x-i, y-i, TILE_SIZE+i*2, TILE_SIZE+i*2), 3, border_radius=15)
        
        gradient = pygame.Surface((TILE_SIZE, TILE_SIZE))
        for i in range(TILE_SIZE):
            r = 35 + int(20 * (i / TILE_SIZE))
            g = 30 + int(20 * (i / TILE_SIZE))
            b = 80 + int(40 * (i / TILE_SIZE))
            pygame.draw.line(gradient, (r, g, b), (0, i), (TILE_SIZE, i))
        screen.blit(gradient, (x, y))
        
        pygame.draw.rect(screen, (100, 80, 200), (x, y, TILE_SIZE, TILE_SIZE), 2, border_radius=15)
        
        pattern_size = 20
        for px in range(x + 10, x + TILE_SIZE - 10, pattern_size):
            for py in range(y + 10, y + TILE_SIZE - 10, pattern_size):
                if (px // pattern_size + py // pattern_size) % 2 == 0:
                    pygame.draw.circle(screen, (70, 60, 140, 50), (px, py), 3)
        
        pygame.draw.circle(screen, (80, 70, 160), (x + TILE_SIZE//2, y + TILE_SIZE//2), 30, 2)
        pygame.draw.circle(screen, (90, 80, 170), (x + TILE_SIZE//2, y + TILE_SIZE//2), 20, 1)
        
        q_font = pygame.font.Font(None, 50)
        q_mark = q_font.render("?", True, (100, 90, 180))
        q_rect = q_mark.get_rect(center=(x + TILE_SIZE//2, y + TILE_SIZE//2 + 2))
        screen.blit(q_mark, q_rect)

def draw_grid():
    for i in range(ROWS):
        for j in range(COLS):
            x = j * (TILE_SIZE + MARGIN) + START_X
            y = i * (TILE_SIZE + MARGIN) + START_Y
            is_hover = (hover_pos == (i, j))
            draw_card(x, y, grid[i][j], revealed[i][j], matched[i][j], 
                     animating[i][j], animation_progress[i][j], is_hover)

def create_party_poppers():
    for _ in range(300):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT // 2)
        particles.append(Particle(x, y))
    
    for _ in range(50):
        x = WIDTH // 2 + random.randint(-200, 200)
        y = HEIGHT // 2 + random.randint(-150, 150)
        p = Particle(x, y, (255, 215, 0), random.randint(8, 18))
        p.vy = random.uniform(-20, -5)
        p.vx = random.uniform(-12, 12)
        particles.append(p)
    
    for _ in range(30):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        color = random.choice([(255, 50, 50), (255, 150, 50), (255, 255, 50),
                               (50, 255, 50), (50, 150, 255), (255, 50, 255)])
        p = Particle(x, y, color, random.randint(5, 12))
        p.vy = random.uniform(-15, -3)
        p.vx = random.uniform(-8, 8)
        particles.append(p)

def start_card_animation(row, col):
    animating[row][col] = True
    animation_progress[row][col] = 0.0

def check_all_cards_completed():
    for i in range(ROWS):
        for j in range(COLS):
            if grid[i][j] is not None and not matched[i][j]:
                return False
    return True

def reset_game():
    global grid, revealed, matched, animating, animation_progress
    global score, moves, first_choice, second_choice
    global waiting, particles, game_won, celebration_active
    
    grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
    revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
    matched = [[False for _ in range(COLS)] for _ in range(ROWS)]
    animating = [[False for _ in range(COLS)] for _ in range(ROWS)]
    animation_progress = [[0.0 for _ in range(COLS)] for _ in range(ROWS)]
    create_grid()
    score = 0
    moves = 0
    first_choice = None
    second_choice = None
    waiting = False
    particles = []
    game_won = False
    celebration_active = False

create_grid()

running = True
while running:
    screen.fill(BLACK)
    
    for i in range(15):
        alpha = 8 + i * 2
        radius = 150 + i * 20
        pygame.draw.circle(screen, (40, 30, 80, alpha), (WIDTH//2, HEIGHT//2 - 20), radius, 1)
    
    title_text = font_large.render("MEMORY", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH//2, 40))
    screen.blit(title_text, title_rect)
    
    progress_text = font.render(f"Score: {score}  Moves: {moves}", True, (150, 150, 220))
    progress_rect = progress_text.get_rect(center=(WIDTH//2, 80))
    screen.blit(progress_text, progress_rect)
    
    progress_bar_width = 200
    progress_bar_x = (WIDTH - progress_bar_width) // 2
    progress_bar_y = 100
    
    total_cards = 0
    matched_cards = 0
    for i in range(ROWS):
        for j in range(COLS):
            if grid[i][j] is not None:
                total_cards += 1
                if matched[i][j]:
                    matched_cards += 1
    
    progress = matched_cards / total_cards if total_cards > 0 else 0
    pygame.draw.rect(screen, (30, 30, 70), (progress_bar_x, progress_bar_y, progress_bar_width, 8), border_radius=4)
    pygame.draw.rect(screen, (100, 200, 255), (progress_bar_x, progress_bar_y, int(progress_bar_width * progress), 8), border_radius=4)
    
    animation_in_progress = False
    for i in range(ROWS):
        for j in range(COLS):
            if animating[i][j]:
                animation_in_progress = True
                animation_progress[i][j] += 0.025
                if animation_progress[i][j] >= 1.0:
                    animating[i][j] = False
                    matched[i][j] = True
                    score += 10
    
    draw_grid()
    
    for particle in particles[:]:
        if not particle.update():
            particles.remove(particle)
        else:
            particle.draw(screen)
    
    if not animation_in_progress:
        all_completed = check_all_cards_completed()
        
        if all_completed and not game_won:
            game_won = True
            win_timer = pygame.time.get_ticks()
            celebration_active = True
            create_party_poppers()
    
    if celebration_active:
        if pygame.time.get_ticks() - win_timer < 5000:
            if random.random() < 0.2:
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT // 2)
                particles.append(Particle(x, y))
        else:
            celebration_active = False
    
    if game_won:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        win_text = font_large.render("YOU WIN!", True, (255, 215, 0))
        win_rect = win_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 80))
        screen.blit(win_text, win_rect)
        
        stats_text = font_medium.render(f"Score: {score}  |  Moves: {moves}", True, WHITE)
        stats_rect = stats_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 20))
        screen.blit(stats_text, stats_rect)
        
        if moves <= 8:
            perfect_text = font_medium.render("PERFECT!", True, (255, 215, 0))
            perfect_rect = perfect_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 30))
            screen.blit(perfect_text, perfect_rect)
        
        restart_text = font.render("Press SPACE to restart", True, (150, 150, 220))
        restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 80))
        screen.blit(restart_text, restart_rect)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE and game_won:
                reset_game()
        
        if event.type == pygame.MOUSEMOTION and not game_won:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            col = (mouse_x - START_X) // (TILE_SIZE + MARGIN)
            row = (mouse_y - START_Y) // (TILE_SIZE + MARGIN)
            if (0 <= row < ROWS and 0 <= col < COLS and 
                grid[row][col] is not None and
                not revealed[row][col] and not matched[row][col] and not animating[row][col]):
                hover_pos = (row, col)
            else:
                hover_pos = None
        
        if event.type == pygame.MOUSEBUTTONDOWN and not game_won and not waiting:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            col = (mouse_x - START_X) // (TILE_SIZE + MARGIN)
            row = (mouse_y - START_Y) // (TILE_SIZE + MARGIN)
            
            if (0 <= row < ROWS and 0 <= col < COLS and 
                grid[row][col] is not None and
                not revealed[row][col] and 
                not matched[row][col] and
                not animating[row][col]):
                
                if first_choice is None:
                    first_choice = (row, col)
                    revealed[row][col] = True
                elif second_choice is None and (row, col) != first_choice:
                    second_choice = (row, col)
                    revealed[row][col] = True
                    moves += 1
                    waiting = True
                    wait_timer = pygame.time.get_ticks()
    
    if waiting and second_choice is not None:
        current_time = pygame.time.get_ticks()
        if current_time - wait_timer > 500:
            row1, col1 = first_choice
            row2, col2 = second_choice
            
            if grid[row1][col1] == grid[row2][col2]:
                start_card_animation(row1, col1)
                start_card_animation(row2, col2)
                first_choice = None
                second_choice = None
                waiting = False
            else:
                revealed[row1][col1] = False
                revealed[row2][col2] = False
                first_choice = None
                second_choice = None
                waiting = False
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
