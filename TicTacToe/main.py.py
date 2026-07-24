import pygame
import sys
import random
import math

pygame.init()
pygame.mixer.init()

WIDTH = 600
HEIGHT = 750
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = 180
BOARD_OFFSET_X = (WIDTH - SQUARE_SIZE * 3) // 2
BOARD_OFFSET_Y = 80

CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

BG_COLOR = (18, 18, 30)
BG_GRADIENT_TOP = (25, 25, 45)
BG_GRADIENT_BOTTOM = (10, 10, 20)
LINE_COLOR = (50, 50, 80)
CIRCLE_COLOR = (100, 200, 255)
CROSS_COLOR = (255, 100, 100)
WIN_COLOR = (0, 255, 150)
TEXT_COLOR = (255, 255, 255)
TEXT_SECONDARY = (180, 180, 200)
BUTTON_COLOR = (40, 40, 60)
BUTTON_HOVER = (60, 60, 85)
BUTTON_ACTIVE = (80, 80, 120)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
clock = pygame.time.Clock()

try:
    font_title = pygame.font.Font(None, 64)
    font_large = pygame.font.Font(None, 72)
    font_medium = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 32)
    font_tiny = pygame.font.Font(None, 24)
except:
    font_title = pygame.font.SysFont('Arial', 64, bold=True)
    font_large = pygame.font.SysFont('Arial', 72, bold=True)
    font_medium = pygame.font.SysFont('Arial', 48, bold=True)
    font_small = pygame.font.SysFont('Arial', 32)
    font_tiny = pygame.font.SysFont('Arial', 24)

class TicTacToe:
    def __init__(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.win_cells = []
        self.animation_progress = 0
        self.move_history = []
        self.setup_buttons()
        
    def setup_buttons(self):
        self.reset_button = {
            'rect': pygame.Rect(WIDTH//2 - 100, HEIGHT - 65, 200, 45),
            'text': 'New Game',
            'hover': False,
            'color': BUTTON_COLOR
        }
        
        self.mode = '2 Player'
        self.mode_buttons = [
            {
                'rect': pygame.Rect(WIDTH//2 - 120, 15, 110, 35),
                'text': '2 Player',
                'hover': False,
                'active': True
            },
            {
                'rect': pygame.Rect(WIDTH//2 + 10, 15, 110, 35),
                'text': 'VS AI',
                'hover': False,
                'active': False
            }
        ]
        
        self.stats = {
            'X_wins': 0,
            'O_wins': 0,
            'ties': 0
        }
    
    def reset(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.win_cells = []
        self.animation_progress = 0
        self.move_history = []
    
    def make_move(self, row, col):
        if self.board[row][col] == '' and not self.game_over:
            self.board[row][col] = self.current_player
            self.move_history.append((row, col, self.current_player))
            
            if self.check_winner():
                self.game_over = True
                self.winner = self.current_player
                if self.winner == 'X':
                    self.stats['X_wins'] += 1
                else:
                    self.stats['O_wins'] += 1
                return True
            elif self.is_board_full():
                self.game_over = True
                self.winner = 'Tie'
                self.stats['ties'] += 1
                return True
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                return True
        return False
    
    def check_winner(self):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != '':
                self.win_cells = [(row, 0), (row, 1), (row, 2)]
                return True
        
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != '':
                self.win_cells = [(0, col), (1, col), (2, col)]
                return True
        
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            self.win_cells = [(0, 0), (1, 1), (2, 2)]
            return True
        
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            self.win_cells = [(0, 2), (1, 1), (2, 0)]
            return True
        
        return False
    
    def is_board_full(self):
        for row in self.board:
            for cell in row:
                if cell == '':
                    return False
        return True
    
    def ai_move(self):
        if self.game_over or self.current_player != 'O':
            return
        
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '':
                    self.board[row][col] = 'O'
                    if self.check_winner():
                        self.board[row][col] = ''
                        self.make_move(row, col)
                        return
                    self.board[row][col] = ''
        
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '':
                    self.board[row][col] = 'X'
                    if self.check_winner():
                        self.board[row][col] = ''
                        self.make_move(row, col)
                        return
                    self.board[row][col] = ''
        
        if self.board[1][1] == '':
            self.make_move(1, 1)
            return
        
        corners = [(0,0), (0,2), (2,0), (2,2)]
        random.shuffle(corners)
        for row, col in corners:
            if self.board[row][col] == '':
                self.make_move(row, col)
                return
        
        edges = [(0,1), (1,0), (1,2), (2,1)]
        random.shuffle(edges)
        for row, col in edges:
            if self.board[row][col] == '':
                self.make_move(row, col)
                return

class ParticleSystem:
    def __init__(self):
        self.particles = []
        self.star_particles = []
    
    def create_win_particles(self, x, y, color, count=50):
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 10)
            self.particles.append({
                'x': x,
                'y': y,
                'vx': speed * math.cos(angle),
                'vy': speed * math.sin(angle),
                'life': 1.0,
                'color': color,
                'size': random.uniform(3, 7),
                'gravity': random.uniform(0.05, 0.15),
                'type': 'sparkle' if random.random() > 0.5 else 'circle',
                'phase': random.uniform(0, 2 * math.pi)  
            })
    
    def create_star_particles(self, x, y):
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 4)
            self.star_particles.append({
                'x': x,
                'y': y,
                'vx': speed * math.cos(angle),
                'vy': speed * math.sin(angle) - 2,
                'life': 1.0,
                'size': random.uniform(2, 5),
                'phase': random.uniform(0, 2 * math.pi)
            })
    
    def update(self):
        for p in self.particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += p['gravity']
            p['life'] -= 0.015
            if p['life'] <= 0:
                self.particles.remove(p)
        
        for p in self.star_particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.02
            p['life'] -= 0.01
            p['phase'] += 0.1
            if p['life'] <= 0:
                self.star_particles.remove(p)
    
    def draw(self, surface):
        for p in self.particles:
            alpha = int(p['life'] * 255)
            size = int(p['size'] * p['life'])
            if p['type'] == 'circle':
                pygame.draw.circle(surface, (*p['color'], alpha), 
                                 (int(p['x']), int(p['y'])), size)
            else:
                # Sparkle
                for i in range(4):
                    angle = i * math.pi / 2 + p['phase']
                    x2 = p['x'] + size * math.cos(angle)
                    y2 = p['y'] + size * math.sin(angle)
                    pygame.draw.line(surface, (*p['color'], alpha), 
                                   (int(p['x']), int(p['y'])), (int(x2), int(y2)), 2)
        
        for p in self.star_particles:
            alpha = int(p['life'] * 255)
            size = int(p['size'] * p['life'])
            glow_size = size * 2
            pygame.draw.circle(surface, (255, 215, 0, alpha // 3), 
                             (int(p['x']), int(p['y'])), glow_size)
            pygame.draw.circle(surface, (255, 255, 255, alpha), 
                             (int(p['x']), int(p['y'])), size)

class Game:
    def __init__(self):
        self.game = TicTacToe()
        self.particles = ParticleSystem()
        self.running = True
        self.hover_cell = None
        self.animating = False
        self.animation_timer = 0
        self.create_background_stars()
    
    def create_background_stars(self):
        self.background_stars = []
        for _ in range(50):
            self.background_stars.append({
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT),
                'size': random.uniform(1, 3),
                'alpha': random.randint(20, 80),
                'speed': random.uniform(0.01, 0.03),
                'phase': random.uniform(0, 2 * math.pi)
            })
    
    def draw_background(self):
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            r = int(BG_GRADIENT_TOP[0] * (1 - ratio) + BG_GRADIENT_BOTTOM[0] * ratio)
            g = int(BG_GRADIENT_TOP[1] * (1 - ratio) + BG_GRADIENT_BOTTOM[1] * ratio)
            b = int(BG_GRADIENT_TOP[2] * (1 - ratio) + BG_GRADIENT_BOTTOM[2] * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))
        
        for star in self.background_stars:
            star['phase'] += star['speed']
            alpha = int(star['alpha'] * (0.5 + 0.5 * math.sin(star['phase'])))
            pygame.draw.circle(screen, (255, 255, 255, alpha), 
                             (int(star['x']), int(star['y'])), int(star['size']))
    
    def draw_board(self):
        board_rect = pygame.Rect(BOARD_OFFSET_X - 10, BOARD_OFFSET_Y - 10, 
                                 SQUARE_SIZE * 3 + 20, SQUARE_SIZE * 3 + 20)
        pygame.draw.rect(screen, (30, 30, 50), board_rect, border_radius=15)
        pygame.draw.rect(screen, (50, 50, 70), board_rect, 2, border_radius=15)
        
        for i in range(1, 3):
            x = BOARD_OFFSET_X + i * SQUARE_SIZE
            pygame.draw.line(screen, LINE_COLOR, 
                           (x, BOARD_OFFSET_Y), 
                           (x, BOARD_OFFSET_Y + SQUARE_SIZE * 3), LINE_WIDTH)
            y = BOARD_OFFSET_Y + i * SQUARE_SIZE
            pygame.draw.line(screen, LINE_COLOR, 
                           (BOARD_OFFSET_X, y), 
                           (BOARD_OFFSET_X + SQUARE_SIZE * 3, y), LINE_WIDTH)
    
    def draw_x(self, row, col, color=CROSS_COLOR, size_scale=1.0):
        x = BOARD_OFFSET_X + col * SQUARE_SIZE + SQUARE_SIZE // 2
        y = BOARD_OFFSET_Y + row * SQUARE_SIZE + SQUARE_SIZE // 2
        offset = SQUARE_SIZE // 4 * size_scale
        
        for i in range(3):
            alpha = 50 - i * 15
            glow_color = (*color, alpha)
            pygame.draw.line(screen, glow_color, 
                           (x - offset - i, y - offset - i),
                           (x + offset + i, y + offset + i), CROSS_WIDTH + i*2)
            pygame.draw.line(screen, glow_color,
                           (x + offset + i, y - offset - i),
                           (x - offset - i, y + offset + i), CROSS_WIDTH + i*2)
        
        pygame.draw.line(screen, color,
                       (x - offset, y - offset),
                       (x + offset, y + offset), CROSS_WIDTH)
        pygame.draw.line(screen, color,
                       (x + offset, y - offset),
                       (x - offset, y + offset), CROSS_WIDTH)
    
    def draw_o(self, row, col, color=CIRCLE_COLOR, size_scale=1.0):
        x = BOARD_OFFSET_X + col * SQUARE_SIZE + SQUARE_SIZE // 2
        y = BOARD_OFFSET_Y + row * SQUARE_SIZE + SQUARE_SIZE // 2
        radius = CIRCLE_RADIUS * size_scale
        
        for i in range(3):
            alpha = 50 - i * 15
            glow_color = (*color, alpha)
            pygame.draw.circle(screen, glow_color, (x, y), radius + i*3, CIRCLE_WIDTH + i*2)
        
        pygame.draw.circle(screen, color, (x, y), radius, CIRCLE_WIDTH)
    
    def draw_win_line(self):
        if self.game.win_cells:
            start = self.game.win_cells[0]
            end = self.game.win_cells[-1]
            start_x = BOARD_OFFSET_X + start[1] * SQUARE_SIZE + SQUARE_SIZE // 2
            start_y = BOARD_OFFSET_Y + start[0] * SQUARE_SIZE + SQUARE_SIZE // 2
            end_x = BOARD_OFFSET_X + end[1] * SQUARE_SIZE + SQUARE_SIZE // 2
            end_y = BOARD_OFFSET_Y + end[0] * SQUARE_SIZE + SQUARE_SIZE // 2
            
            progress = min(1.0, self.game.animation_progress + 0.02)
            self.game.animation_progress = progress
            
            current_x = start_x + (end_x - start_x) * progress
            current_y = start_y + (end_y - start_y) * progress
            
            for i in range(5):
                alpha = 50 - i * 10
                color = (0, 255, 150, alpha)
                pygame.draw.line(screen, color, (start_x, start_y), 
                               (current_x, current_y), LINE_WIDTH + i*2)
            
            pygame.draw.line(screen, WIN_COLOR, (start_x, start_y), 
                           (current_x, current_y), LINE_WIDTH + 4)
            
            if progress >= 0.9 and random.random() < 0.1:
                color = (0, 255, 150)
                self.particles.create_win_particles(
                    random.randint(0, WIDTH), 
                    random.randint(0, HEIGHT), 
                    color, 10
                )
    
    def draw_status(self):
        if self.game.game_over:
            if self.game.winner == 'Tie':
                text = "It's a Tie!"
                color = (255, 255, 100)
            elif self.game.winner == 'X':
                text = "X Wins!"
                color = CROSS_COLOR
            else:
                text = "O Wins!"
                color = CIRCLE_COLOR
        else:
            text = f"Player {self.game.current_player}'s Turn"
            color = CROSS_COLOR if self.game.current_player == 'X' else CIRCLE_COLOR
        
        status_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT - 115, 300, 45)
        pygame.draw.rect(screen, (0, 0, 0, 150), status_rect, border_radius=12)
        pygame.draw.rect(screen, (100, 100, 150, 50), status_rect, 2, border_radius=12)
        
        status_text = font_small.render(text, True, color)
        status_rect_text = status_text.get_rect(center=(WIDTH//2, HEIGHT - 92))
        screen.blit(status_text, status_rect_text)
    
    def draw_scores(self):
        score_x_rect = pygame.Rect(20, 15, 130, 50)
        pygame.draw.rect(screen, (0, 0, 0, 100), score_x_rect, border_radius=10)
        pygame.draw.rect(screen, (CROSS_COLOR[0], CROSS_COLOR[1], CROSS_COLOR[2], 50), 
                        score_x_rect, 2, border_radius=10)
        score_text = font_small.render(f"X: {self.game.stats['X_wins']}", True, CROSS_COLOR)
        screen.blit(score_text, (30, 28))
        
        score_o_rect = pygame.Rect(WIDTH - 150, 15, 130, 50)
        pygame.draw.rect(screen, (0, 0, 0, 100), score_o_rect, border_radius=10)
        pygame.draw.rect(screen, (CIRCLE_COLOR[0], CIRCLE_COLOR[1], CIRCLE_COLOR[2], 50), 
                        score_o_rect, 2, border_radius=10)
        score_text = font_small.render(f"O: {self.game.stats['O_wins']}", True, CIRCLE_COLOR)
        screen.blit(score_text, (WIDTH - 140, 28))
        
        ties_rect = pygame.Rect(WIDTH//2 - 60, 70, 120, 30)
        pygame.draw.rect(screen, (0, 0, 0, 80), ties_rect, border_radius=8)
        ties_text = font_tiny.render(f"Ties: {self.game.stats['ties']}", True, TEXT_SECONDARY)
        ties_rect_text = ties_text.get_rect(center=(WIDTH//2, 85))
        screen.blit(ties_text, ties_rect_text)
    
    def draw_buttons(self):
        for i, button in enumerate(self.game.mode_buttons):
            if button['active']:
                color = BUTTON_ACTIVE
                shadow = True
            else:
                color = BUTTON_COLOR if not button['hover'] else BUTTON_HOVER
                shadow = False
            
            if shadow:
                shadow_rect = button['rect'].copy()
                shadow_rect.x += 2
                shadow_rect.y += 2
                pygame.draw.rect(screen, (0, 0, 0, 50), shadow_rect, border_radius=8)
            
            pygame.draw.rect(screen, color, button['rect'], border_radius=8)
            
            if button['active']:
                pygame.draw.rect(screen, (255, 215, 0, 100), button['rect'], 2, border_radius=8)
            else:
                pygame.draw.rect(screen, (80, 80, 100), button['rect'], 1, border_radius=8)
            
            text_color = TEXT_COLOR if button['active'] else TEXT_SECONDARY
            text = font_tiny.render(button['text'], True, text_color)
            text_rect = text.get_rect(center=button['rect'].center)
            screen.blit(text, text_rect)
        
        button = self.game.reset_button
        color = BUTTON_ACTIVE if button['hover'] else BUTTON_COLOR
        
        shadow_rect = button['rect'].copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(screen, (0, 0, 0, 50), shadow_rect, border_radius=10)
        
        pygame.draw.rect(screen, color, button['rect'], border_radius=10)
        pygame.draw.rect(screen, (100, 100, 150, 80), button['rect'], 2, border_radius=10)
        
        text = font_small.render(button['text'], True, TEXT_COLOR)
        text_rect = text.get_rect(center=button['rect'].center)
        screen.blit(text, text_rect)
    
    def draw_hover_effect(self):
        if self.hover_cell and not self.game.game_over:
            row, col = self.hover_cell
            if self.game.board[row][col] == '':
                x = BOARD_OFFSET_X + col * SQUARE_SIZE
                y = BOARD_OFFSET_Y + row * SQUARE_SIZE
                pygame.draw.rect(screen, (255, 255, 255, 30), 
                               (x, y, SQUARE_SIZE, SQUARE_SIZE), border_radius=5)
    
    def handle_click(self, pos):
        x, y = pos
        
        for i, button in enumerate(self.game.mode_buttons):
            if button['rect'].collidepoint(pos):
                if not button['active']:
                    for b in self.game.mode_buttons:
                        b['active'] = False
                    button['active'] = True
                    self.game.mode = '2 Player' if i == 0 else 'AI'
                    self.game.reset()
                    self.particles = ParticleSystem()
                return
        
        if self.game.reset_button['rect'].collidepoint(pos):
            self.game.reset()
            self.particles = ParticleSystem()
            return
        
        if y > BOARD_OFFSET_Y and y < BOARD_OFFSET_Y + SQUARE_SIZE * 3:
            if x > BOARD_OFFSET_X and x < BOARD_OFFSET_X + SQUARE_SIZE * 3:
                row = (y - BOARD_OFFSET_Y) // SQUARE_SIZE
                col = (x - BOARD_OFFSET_X) // SQUARE_SIZE
                
                if self.game.mode == 'AI' and self.game.current_player == 'O':
                    return
                
                if self.game.make_move(row, col):
                    x_pos = BOARD_OFFSET_X + col * SQUARE_SIZE + SQUARE_SIZE // 2
                    y_pos = BOARD_OFFSET_Y + row * SQUARE_SIZE + SQUARE_SIZE // 2
                    color = CROSS_COLOR if self.game.current_player == 'X' else CIRCLE_COLOR
                    self.particles.create_win_particles(x_pos, y_pos, color, 20)
                    self.particles.create_star_particles(x_pos, y_pos)
    
    def update(self):
        self.particles.update()
        
        if self.game.mode == 'AI' and not self.game.game_over:
            self.game.ai_move()
        
        if self.game.game_over and self.game.winner and self.game.winner != 'Tie':
            if self.game.animation_progress >= 0.9 and random.random() < 0.05:
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)
                color = (0, 255, 150)
                self.particles.create_win_particles(x, y, color, 15)
    
    def draw(self):
        self.draw_background()
        self.draw_scores()
        self.draw_board()
        self.draw_hover_effect()
        
        for row in range(3):
            for col in range(3):
                if self.game.board[row][col] == 'X':
                    self.draw_x(row, col)
                elif self.game.board[row][col] == 'O':
                    self.draw_o(row, col)
        
        if self.game.game_over and self.game.winner and self.game.winner != 'Tie':
            self.draw_win_line()
        
        self.particles.draw(screen)
        self.draw_status()
        self.draw_buttons()
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                
                if event.type == pygame.MOUSEMOTION:
                    self.hover_cell = None
                    
                    x, y = event.pos
                    if y > BOARD_OFFSET_Y and y < BOARD_OFFSET_Y + SQUARE_SIZE * 3:
                        if x > BOARD_OFFSET_X and x < BOARD_OFFSET_X + SQUARE_SIZE * 3:
                            row = (y - BOARD_OFFSET_Y) // SQUARE_SIZE
                            col = (x - BOARD_OFFSET_X) // SQUARE_SIZE
                            if self.game.board[row][col] == '':
                                self.hover_cell = (row, col)
                    
                    self.game.reset_button['hover'] = self.game.reset_button['rect'].collidepoint(event.pos)
                    for button in self.game.mode_buttons:
                        button['hover'] = button['rect'].collidepoint(event.pos)
            
            self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(60)

def main():
    print("="*50)
    print("TIC TAC TOE - Enhanced Edition")
    print("="*50)
    print("Controls:")
    print("  Click on the board to place your mark")
    print("  Click 'New Game' to restart")
    print("  Click '2 Player' or 'VS AI' to change mode")
    print("="*50)
    print("Close the window to exit")
    print("="*50)
    
    game = Game()
    game.run()

if __name__ == "__main__":
    main()