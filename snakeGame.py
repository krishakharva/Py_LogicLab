import pygame
import sys
import random
import math
from collections import deque

pygame.init()
pygame.mixer.init()

WIDTH = 600
HEIGHT = 700
FPS = 60
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = (HEIGHT - 80) // GRID_SIZE

import os
if os.name == 'nt':
    os.environ['SDL_VIDEO_WINDOW_POS'] = '50,100'
else:
    os.environ['SDL_VIDEO_WINDOW_POS'] = '50,100'

BLACK = (5, 5, 15)
NEON_GREEN = (0, 255, 100)
NEON_BLUE = (0, 150, 255)
NEON_PINK = (255, 50, 150)
NEON_PURPLE = (150, 50, 255)
NEON_YELLOW = (255, 230, 50)
NEON_ORANGE = (255, 150, 0)
NEON_RED = (255, 50, 50)
WHITE = (255, 255, 255)
GRID_LINE = (20, 20, 40)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NEON SNAKE")
clock = pygame.time.Clock()

try:
    font_large = pygame.font.Font(None, 56)
    font_medium = pygame.font.Font(None, 40)
    font_small = pygame.font.Font(None, 30)
    font_tiny = pygame.font.Font(None, 20)
except:
    font_large = pygame.font.SysFont('Arial', 56, bold=True)
    font_medium = pygame.font.SysFont('Arial', 40, bold=True)
    font_small = pygame.font.SysFont('Arial', 30, bold=True)
    font_tiny = pygame.font.SysFont('Arial', 20)

class Particle:
    def __init__(self, x, y, color, vel_x=None, vel_y=None, size=None, life=None):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1.5, 4.5)
        self.vx = vel_x if vel_x is not None else speed * math.cos(angle)
        self.vy = vel_y if vel_y is not None else speed * math.sin(angle)
        self.life = life if life is not None else random.uniform(0.5, 1.5)
        self.max_life = self.life
        self.size = size if size is not None else random.uniform(1.5, 4)
        self.color = color
        self.gravity = random.uniform(0.02, 0.08)
        self.type = random.choice(['circle', 'sparkle', 'glow'])
        self.phase = random.uniform(0, 2 * math.pi)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.life -= 0.015
        self.phase += 0.1
        return self.life > 0
    
    def draw(self, surface):
        alpha = int((self.life / self.max_life) * 255)
        size = int(self.size * (self.life / self.max_life))
        
        if size < 1:
            return
            
        if self.type == 'circle':
            if alpha < 255:
                temp_surf = pygame.Surface((size * 2 + 4, size * 2 + 4), pygame.SRCALPHA)
                pygame.draw.circle(temp_surf, (*self.color[:3], alpha), 
                                 (size + 2, size + 2), max(1, size))
                surface.blit(temp_surf, (int(self.x) - size - 2, int(self.y) - size - 2))
            else:
                pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), max(1, size))
                
        elif self.type == 'sparkle':
            for i in range(4):
                angle = i * math.pi / 2 + self.phase
                x2 = self.x + size * math.cos(angle)
                y2 = self.y + size * math.sin(angle)
                if alpha < 255:
                    temp_surf = pygame.Surface((size * 4 + 4, size * 4 + 4), pygame.SRCALPHA)
                    pygame.draw.line(temp_surf, (*self.color[:3], alpha), 
                                   (size * 2 + 2, size * 2 + 2), 
                                   (size * 2 + 2 + (x2 - self.x), size * 2 + 2 + (y2 - self.y)), 2)
                    surface.blit(temp_surf, (int(self.x) - size * 2 - 2, int(self.y) - size * 2 - 2))
                else:
                    pygame.draw.line(surface, self.color, 
                                   (int(self.x), int(self.y)), (int(x2), int(y2)), 2)
        else:  
            if alpha > 10:
                temp_surf = pygame.Surface((size * 6 + 10, size * 6 + 10), pygame.SRCALPHA)
                for i in range(3):
                    glow_size = size * (2 + i * 1.5)
                    glow_alpha = alpha // (3 + i * 2)
                    pygame.draw.circle(temp_surf, (*self.color[:3], glow_alpha), 
                                     (size * 3 + 5, size * 3 + 5), int(glow_size))
                surface.blit(temp_surf, (int(self.x) - size * 3 - 5, int(self.y) - size * 3 - 5))

class ParticleSystem:
    def __init__(self):
        self.particles = []
    
    def create_burst(self, x, y, color, count=25, speed=4):
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed_var = random.uniform(1.5, speed)
            size = random.uniform(1.5, 4)
            self.particles.append(Particle(
                x, y, color,
                speed_var * math.cos(angle),
                speed_var * math.sin(angle),
                size
            ))
    
    def create_food_particles(self, x, y, color):
        for _ in range(15):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 3)
            size = random.uniform(1.5, 3.5)
            self.particles.append(Particle(
                x, y, color,
                speed * math.cos(angle),
                speed * math.sin(angle) - 2,
                size,
                random.uniform(0.5, 1.0)
            ))
    
    def create_trail(self, x, y, color):
        for _ in range(3):
            self.particles.append(Particle(
                x + random.uniform(-4, 4),
                y + random.uniform(-4, 4),
                color,
                random.uniform(-0.5, 0.5),
                random.uniform(-1, -0.5),
                random.uniform(1, 2.5),
                random.uniform(0.3, 0.8)
            ))
    
    def update(self):
        self.particles = [p for p in self.particles if p.update()]
    
    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)

class Food:
    def __init__(self):
        self.color = None
        self.x = 0
        self.y = 0
        self.pulse = 0
        self.type = 'normal'
        self.spawn()
    
    def spawn(self):
        self.x = random.randint(0, GRID_WIDTH - 1)
        self.y = random.randint(0, GRID_HEIGHT - 1)
        self.color = random.choice([NEON_RED, NEON_PINK, NEON_ORANGE, NEON_YELLOW])
        self.type = random.choices(['normal', 'golden', 'poison'], weights=[70, 20, 10])[0]
        self.pulse = 0
    
    def draw(self, surface, snake_body):
        if (self.x, self.y) in snake_body:
            self.spawn()
            return
        
        x = self.x * GRID_SIZE + GRID_SIZE // 2
        y = self.y * GRID_SIZE + GRID_SIZE // 2 + 80
        self.pulse += 0.05

        glow_radius = GRID_SIZE // 2 + 4 * math.sin(self.pulse)
        for i in range(3):
            alpha = 50 - i * 15
            temp_surf = pygame.Surface((int(glow_radius + i * 4) * 2 + 10, 
                                       int(glow_radius + i * 4) * 2 + 10), pygame.SRCALPHA)
            pygame.draw.circle(temp_surf, (*self.color[:3], alpha), 
                             (int(glow_radius + i * 4) + 5, int(glow_radius + i * 4) + 5), 
                             int(glow_radius + i * 4))
            surface.blit(temp_surf, (x - int(glow_radius + i * 4) - 5, y - int(glow_radius + i * 4) - 5))
     
        if self.type == 'golden':
            points = []
            for i in range(10):
                angle = i * math.pi / 5 - math.pi / 2
                radius = GRID_SIZE // 2 - 2 if i % 2 == 0 else GRID_SIZE // 4
                px = x + radius * math.cos(angle + self.pulse * 0.5)
                py = y + radius * math.sin(angle + self.pulse * 0.5)
                points.append((px, py))
            pygame.draw.polygon(surface, NEON_YELLOW, points)
            pygame.draw.polygon(surface, (255, 255, 255, 100), points, 2)
        elif self.type == 'poison':
            pygame.draw.circle(surface, NEON_PURPLE, (x, y), GRID_SIZE // 2 - 2)
            pygame.draw.circle(surface, (0, 0, 0), (x - 4, y - 3), 3)
            pygame.draw.circle(surface, (0, 0, 0), (x + 4, y - 3), 3)
            pygame.draw.line(surface, WHITE, (x - 5, y + 4), (x + 5, y + 8), 2)
            pygame.draw.line(surface, WHITE, (x - 5, y + 8), (x + 5, y + 4), 2)
        else:
            radius = GRID_SIZE // 2 - 3 + 2 * math.sin(self.pulse)
            pygame.draw.circle(surface, self.color, (x, y), int(radius))
            temp_surf = pygame.Surface((radius * 2 + 10, radius * 2 + 10), pygame.SRCALPHA)
            pygame.draw.circle(temp_surf, (255, 255, 255, 100), 
                             (int(radius) + 5, int(radius) + 5), int(radius * 0.4))
            surface.blit(temp_surf, (x - int(radius) - 5, y - int(radius) - 5))

class Snake:
    def __init__(self):
        self.reset()
    
    def reset(self):
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        self.body = deque([(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)])
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.grow_count = 0
        self.score = 0
        self.high_score = 0
        self.combo = 0
        self.speed_multiplier = 1.0
        self.alive = True
        self.move_counter = 0
        self.move_delay = 6 
    
    def move(self):
        if not self.alive:
            return
        
        self.move_counter += 1
        if self.move_counter < self.move_delay:
            return
        
        self.move_counter = 0
        
        self.direction = self.next_direction
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        new_head = (new_head[0] % GRID_WIDTH, new_head[1] % GRID_HEIGHT)
        self.body.appendleft(new_head)
        
        if self.grow_count > 0:
            self.grow_count -= 1
        else:
            self.body.pop()

        if list(self.body).count(new_head) > 1:
            self.alive = False
    
    def grow(self, amount=1):
        self.grow_count += amount
    
    def change_direction(self, direction):
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.next_direction = direction
    
    def get_head(self):
        return self.body[0]
    
    def get_body(self):
        return list(self.body)

class NeonSnakeGame:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.particles = ParticleSystem()
        self.running = True
        self.paused = False
        self.game_over = False
        self.score_animation = 0
        self.combo_timer = 0
        self.speed_increase = 0
        self.bg_stars = self.create_background_stars()
        self.grid_lines = True
        self.ui_buttons = []
        self.setup_ui()
        self.move_timer = 0
    
    def create_background_stars(self):
        stars = []
        for _ in range(70):
            stars.append({
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT),
                'size': random.uniform(0.5, 2),
                'alpha': random.randint(20, 80),
                'speed': random.uniform(0.01, 0.03),
                'phase': random.uniform(0, 2 * math.pi)
            })
        return stars
    
    def setup_ui(self):
        self.ui_buttons = [
            {
                'rect': pygame.Rect(WIDTH//2 - 65, HEIGHT - 45, 130, 35),
                'text': 'New Game',
                'hover': False,
                'action': 'reset'
            },
            {
                'rect': pygame.Rect(15, 10, 32, 32),
                'text': '||',
                'hover': False,
                'action': 'pause'
            },
            {
                'rect': pygame.Rect(WIDTH - 47, 10, 32, 32),
                'text': '??',
                'hover': False,
                'action': 'settings'
            }
        ]
    
    def draw_background(self):
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            r = int(5 * (1 - ratio) + 10 * ratio)
            g = int(5 * (1 - ratio) + 15 * ratio)
            b = int(15 * (1 - ratio) + 25 * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

        for star in self.bg_stars:
            star['phase'] += star['speed']
            alpha = int(star['alpha'] * (0.5 + 0.5 * math.sin(star['phase'])))
            temp_surf = pygame.Surface((int(star['size']) * 2 + 4, int(star['size']) * 2 + 4), pygame.SRCALPHA)
            pygame.draw.circle(temp_surf, (255, 255, 255, alpha), 
                             (int(star['size']) + 2, int(star['size']) + 2), int(star['size']))
            screen.blit(temp_surf, (int(star['x']) - int(star['size']) - 2, 
                                   int(star['y']) - int(star['size']) - 2))

        if self.grid_lines:
            for x in range(0, WIDTH, GRID_SIZE):
                pygame.draw.line(screen, GRID_LINE, (x, 80), (x, HEIGHT), 1)
            for y in range(80, HEIGHT, GRID_SIZE):
                pygame.draw.line(screen, GRID_LINE, (0, y), (WIDTH, y), 1)
    
    def draw_snake(self):
        body = self.snake.get_body()
        if not body:
            return

        for i, (x, y) in enumerate(body):
            pos_x = x * GRID_SIZE + GRID_SIZE // 2
            pos_y = y * GRID_SIZE + GRID_SIZE // 2 + 80

            ratio = i / len(body)
            if i == 0: 
                color = NEON_GREEN
                size = GRID_SIZE // 2 - 1
            else:
                green = int(255 * (1 - ratio * 0.5))
                blue = int(100 * (1 - ratio * 0.3))
                color = (0, green, blue)
                size = GRID_SIZE // 2 - 1 - int(ratio * 2)

            for j in range(3):
                glow_size = size + j * 3
                glow_alpha = 30 - j * 10
                temp_surf = pygame.Surface((glow_size * 2 + 10, glow_size * 2 + 10), pygame.SRCALPHA)
                pygame.draw.circle(temp_surf, (*color[:3], glow_alpha), 
                                 (glow_size + 5, glow_size + 5), glow_size)
                screen.blit(temp_surf, (pos_x - glow_size - 5, pos_y - glow_size - 5))

            if i == 0:
                pygame.draw.circle(screen, color, (pos_x, pos_y), size + 2)
                eye_color = WHITE
                dir_x, dir_y = self.snake.direction
                if dir_x == 1:
                    eye_pos = [(pos_x + 3, pos_y - 3), (pos_x + 3, pos_y + 3)]
                elif dir_x == -1:
                    eye_pos = [(pos_x - 3, pos_y - 3), (pos_x - 3, pos_y + 3)]
                elif dir_y == -1:
                    eye_pos = [(pos_x - 3, pos_y - 3), (pos_x + 3, pos_y - 3)]
                else:
                    eye_pos = [(pos_x - 3, pos_y + 3), (pos_x + 3, pos_y + 3)]
                
                for ex, ey in eye_pos:
                    pygame.draw.circle(screen, eye_color, (ex, ey), 2)
                    pygame.draw.circle(screen, (0, 0, 0), (ex + dir_x*1, ey + dir_y*1), 1)
            else:
                pygame.draw.circle(screen, color, (pos_x, pos_y), size)
            
            if i % 2 == 0 and random.random() < 0.08:
                self.particles.create_trail(pos_x, pos_y, (0, 255, 100, 50))
    
    def draw_food(self):
        self.food.draw(screen, self.snake.get_body())
    
    def draw_ui(self):
        score_text = font_large.render(str(self.snake.score), True, NEON_GREEN)
        score_rect = score_text.get_rect(center=(WIDTH//2, 38))
        screen.blit(score_text, score_rect)
        high_score_text = font_tiny.render(f"HIGH: {self.snake.high_score}", True, NEON_YELLOW)
        high_score_rect = high_score_text.get_rect(center=(WIDTH//2, 60))
        screen.blit(high_score_text, high_score_rect)
        label_text = font_tiny.render("SCORE", True, (100, 100, 150))
        label_rect = label_text.get_rect(center=(WIDTH//2, 18))
        screen.blit(label_text, label_rect)
        if self.snake.combo > 1:
            combo_text = font_medium.render(f"x{self.snake.combo}", True, NEON_ORANGE)
            combo_rect = combo_text.get_rect(center=(WIDTH//2 + 80, 38))
            screen.blit(combo_text, combo_rect)
        speed_text = font_tiny.render(f"SPEED: {self.snake.speed_multiplier:.1f}x", True, NEON_BLUE)
        speed_rect = speed_text.get_rect(center=(WIDTH - 80, 18))
        screen.blit(speed_text, speed_rect)
        food_type_text = font_tiny.render(f"FOOD: {self.food.type.upper()}", True, self.food.color)
        food_type_rect = food_type_text.get_rect(center=(80, 18))
        screen.blit(food_type_text, food_type_rect)

        for button in self.ui_buttons:
            color = (60, 60, 80) if not button['hover'] else (80, 80, 120)
            pygame.draw.rect(screen, color, button['rect'], border_radius=8)
            pygame.draw.rect(screen, (100, 100, 150, 50), button['rect'], 2, border_radius=8)
            
            text = font_small.render(button['text'], True, WHITE)
            text_rect = text.get_rect(center=button['rect'].center)
            screen.blit(text, text_rect)
    
    def draw_game_over(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
  
        game_over_text = font_large.render("GAME OVER", True, NEON_RED)
        game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 40))
        screen.blit(game_over_text, game_over_rect)

        score_text = font_medium.render(f"Score: {self.snake.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 20))
        screen.blit(score_text, score_rect)
 
        if self.snake.score >= self.snake.high_score:
            high_text = font_small.render("NEW HIGH SCORE!", True, NEON_YELLOW)
            high_rect = high_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 60))
            screen.blit(high_text, high_rect)
  
        restart_text = font_small.render("Press SPACE or Click New Game", True, (150, 150, 200))
        restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 100))
        screen.blit(restart_text, restart_rect)
    
    def draw_pause(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        pause_text = font_large.render("PAUSED", True, NEON_BLUE)
        pause_rect = pause_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(pause_text, pause_rect)
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.snake.change_direction((0, -1))
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.snake.change_direction((0, 1))
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.snake.change_direction((-1, 0))
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.snake.change_direction((1, 0))
        
        if keys[pygame.K_SPACE]:
            if self.game_over:
                self.reset_game()
            else:
                self.paused = not self.paused
    
    def handle_click(self, pos):
        for button in self.ui_buttons:
            if button['rect'].collidepoint(pos):
                if button['action'] == 'reset':
                    self.reset_game()
                elif button['action'] == 'pause':
                    if not self.game_over:
                        self.paused = not self.paused
                return
        if self.game_over and pos[1] > 80:
            self.reset_game()
    
    def reset_game(self):
        self.snake.reset()
        self.food = Food()
        self.particles = ParticleSystem()
        self.game_over = False
        self.paused = False
        self.move_timer = 0
        self.speed_increase = 0
        self.combo_timer = 0
        self.snake.move_delay = 6
    
    def update(self):
        if self.game_over or self.paused:
            return

        self.particles.update()
        self.snake.move()

        head = self.snake.get_head()
        if head == (self.food.x, self.food.y):
            self.eat_food()

        if not self.snake.alive:
            self.game_over = True
            if self.snake.score > self.snake.high_score:
                self.snake.high_score = self.snake.score
            self.particles.create_burst(
                head[0] * GRID_SIZE + GRID_SIZE // 2,
                head[1] * GRID_SIZE + GRID_SIZE // 2 + 80,
                NEON_RED, 40, 6
            )

        self.food.pulse += 0.05
        
        if self.combo_timer > 0:
            self.combo_timer -= 1
            if self.combo_timer == 0:
                self.snake.combo = 0

        self.snake.move_delay = max(3, 6 - self.speed_increase)
        self.snake.speed_multiplier = 6 / self.snake.move_delay
    
    def eat_food(self):
        head = self.snake.get_head()
        x = head[0] * GRID_SIZE + GRID_SIZE // 2
        y = head[1] * GRID_SIZE + GRID_SIZE // 2 + 80
        
        if self.food.type == 'golden':
            points = 30
            self.snake.grow(3)
            self.speed_increase += 1
            self.particles.create_burst(x, y, NEON_YELLOW, 35, 6)
            self.snake.combo += 2
            self.combo_timer = 60
        elif self.food.type == 'poison':
            points = -15
            self.snake.grow(-1)
            self.speed_increase = max(0, self.speed_increase - 1)
            self.particles.create_burst(x, y, NEON_PURPLE, 25, 4)
            self.snake.combo = 0
        else:
            points = 10
            self.snake.grow(1)
            self.particles.create_burst(x, y, self.food.color, 15, 4)
            self.snake.combo += 1
            self.combo_timer = 30

        self.snake.score += points
        if self.snake.score > self.snake.high_score:
            self.snake.high_score = self.snake.score
        
        self.food = Food()
        self.score_animation = 20
        self.particles.create_food_particles(x, y, self.food.color)
        
        if points > 0 and self.snake.score % 50 == 0:
            self.snake.move_delay = max(3, self.snake.move_delay - 1)
            self.speed_increase += 1
    
    def draw(self):
        self.draw_background()
        self.draw_food()
        self.draw_snake()
        self.particles.draw(screen)
        self.draw_ui()

        if self.game_over:
            self.draw_game_over()
        if self.paused and not self.game_over:
            self.draw_pause()
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        pygame.quit()
                        sys.exit()
                    self.handle_input()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                
                if event.type == pygame.MOUSEMOTION:
                    for button in self.ui_buttons:
                        button['hover'] = button['rect'].collidepoint(event.pos)
            
            self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(FPS)

def main():
    print("="*50)
    print("NEON SNAKE")
    print("="*50)
    print("Controls:")
    print("  Arrow Keys / WASD - Move")
    print("  SPACE - Pause / Restart")
    print("  ESC - Exit")
    print("="*50)
    print("Features:")
    print("  Neon glow effects")
    print("  Different food types")
    print("  Golden food - Extra points & grow")
    print("  Poison food - Lose points")
    print("  Combo system")
    print("  Speed increases with score")
    print("="*50)
    
    game = NeonSnakeGame()
    game.run()

if __name__ == "__main__":
    main()