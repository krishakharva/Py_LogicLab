import pygame
import sys
import random
import copy
import math

pygame.init()

WIDTH = 600
HEIGHT = 700
FPS = 60
GRID_SIZE = 9
CELL_SIZE = (WIDTH - 40) // GRID_SIZE
GRID_OFFSET_X = 20
GRID_OFFSET_Y = 65
BUTTON_HEIGHT = 40

BG_COLOR = (18, 18, 30)
BG_GRADIENT_TOP = (25, 25, 45)
BG_GRADIENT_BOTTOM = (10, 10, 20)
CELL_BG = (30, 30, 50)
CELL_BG_SELECTED = (50, 80, 120)
CELL_BG_HIGHLIGHT = (40, 45, 70)
CELL_BG_SAME_NUMBER = (45, 50, 75)
CELL_BG_ERROR = (80, 30, 30)
CELL_BG_GIVEN = (25, 28, 45)
TEXT_COLOR = (255, 255, 255)
TEXT_GIVEN = (180, 200, 255)
TEXT_USER = (100, 200, 255)
TEXT_ERROR = (255, 80, 80)
TEXT_SOLVED = (0, 255, 100)
LINE_COLOR = (60, 60, 80)
LINE_BOLD = (100, 100, 150)
BUTTON_COLOR = (40, 40, 60)
BUTTON_HOVER = (60, 60, 85)
BUTTON_ACTIVE = (80, 80, 120)
NEON_GREEN = (0, 255, 100)
NEON_BLUE = (0, 150, 255)
NEON_RED = (255, 50, 50)
NEON_YELLOW = (255, 230, 50)
VICTORY_GOLD = (255, 215, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SUDOKU")
clock = pygame.time.Clock()

try:
    font_large = pygame.font.Font(None, 72)
    font_medium = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 32)
    font_tiny = pygame.font.Font(None, 18)
    font_number = pygame.font.Font(None, 36)
except:
    font_large = pygame.font.SysFont('Arial', 72, bold=True)
    font_medium = pygame.font.SysFont('Arial', 48, bold=True)
    font_small = pygame.font.SysFont('Arial', 32, bold=True)
    font_tiny = pygame.font.SysFont('Arial', 18)
    font_number = pygame.font.SysFont('Arial', 36)

class SudokuGenerator:
    """Generates valid Sudoku puzzles"""
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = None
        
    def generate(self, difficulty=40):
        """Generate a new puzzle with given number of clues"""
        self.board = self.generate_solution()
        self.solution = copy.deepcopy(self.board)
        
        cells_to_remove = difficulty
        positions = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(positions)
        
        for i, j in positions[:cells_to_remove]:
            self.board[i][j] = 0
            
        return self.board, self.solution
    
    def generate_solution(self):
        board = [[0 for _ in range(9)] for _ in range(9)]
        self.solve_sudoku(board)
        return board
    
    def solve_sudoku(self, board):
        empty = self.find_empty(board)
        if not empty:
            return True
        row, col = empty
        
        nums = list(range(1, 10))
        random.shuffle(nums)
        
        for num in nums:
            if self.is_valid(board, row, col, num):
                board[row][col] = num
                if self.solve_sudoku(board):
                    return True
                board[row][col] = 0
        return False
    
    def find_empty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None
    
    def is_valid(self, board, row, col, num):
        for j in range(9):
            if board[row][j] == num:
                return False
        for i in range(9):
            if board[i][col] == num:
                return False
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if board[box_row + i][box_col + j] == num:
                    return False
        return True

class SudokuSolver:
    def __init__(self):
        self.solution = None
        
    def solve(self, board):
        board_copy = copy.deepcopy(board)
        if self.solve_sudoku(board_copy):
            return board_copy
        return None
    
    def solve_sudoku(self, board):
        empty = self.find_empty(board)
        if not empty:
            return True
        row, col = empty
        
        for num in range(1, 10):
            if self.is_valid(board, row, col, num):
                board[row][col] = num
                if self.solve_sudoku(board):
                    return True
                board[row][col] = 0
        return False
    
    def find_empty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None
    
    def is_valid(self, board, row, col, num):
        for j in range(9):
            if board[row][j] == num:
                return False
        for i in range(9):
            if board[i][col] == num:
                return False
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if board[box_row + i][box_col + j] == num:
                    return False
        return True

class SudokuGame:
    def __init__(self):
        self.generator = SudokuGenerator()
        self.solver = SudokuSolver()
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = None
        self.selected_cell = None
        self.user_board = [[0 for _ in range(9)] for _ in range(9)]
        self.given_cells = [[False for _ in range(9)] for _ in range(9)]
        self.error_cells = set()
        self.highlight_cells = set()
        self.same_number_cells = set()
        self.mistakes = 0
        self.hints_used = 0
        self.solved = False
        self.difficulty = 40
        self.hint_cell = None
        self.hint_timer = 0
        self.victory_timer = 0
        self.victory_particles = []
        self.buttons = []
        self.setup_ui()
        self.new_game()
    
    def setup_ui(self):
        button_width = 115
        button_height = 35
        
        self.buttons = [
            {
                'rect': pygame.Rect(15, HEIGHT - button_height - 10, button_width, button_height),
                'text': 'New Game',
                'hover': False,
                'action': 'new_game',
                'color': BUTTON_COLOR
            },
            {
                'rect': pygame.Rect(135, HEIGHT - button_height - 10, button_width, button_height),
                'text': 'Solve',
                'hover': False,
                'action': 'solve',
                'color': BUTTON_COLOR
            },
            {
                'rect': pygame.Rect(255, HEIGHT - button_height - 10, button_width, button_height),
                'text': 'Hint',
                'hover': False,
                'action': 'hint',
                'color': BUTTON_COLOR
            },
            {
                'rect': pygame.Rect(375, HEIGHT - button_height - 10, button_width, button_height),
                'text': 'Reset',
                'hover': False,
                'action': 'reset',
                'color': BUTTON_COLOR
            }
        ]
    
    def new_game(self):
        """Start a new game"""
        self.board, self.solution = self.generator.generate(self.difficulty)
        self.user_board = copy.deepcopy(self.board)
        
        for i in range(9):
            for j in range(9):
                self.given_cells[i][j] = self.board[i][j] != 0
        
        self.selected_cell = None
        self.error_cells = set()
        self.mistakes = 0
        self.hints_used = 0
        self.solved = False
        self.hint_cell = None
        self.hint_timer = 0
        self.victory_timer = 0
        self.victory_particles = []
        self.highlight_cells = set()
        self.same_number_cells = set()
    
    def reset(self):
        """Reset to initial state"""
        self.user_board = copy.deepcopy(self.board)
        self.error_cells = set()
        self.mistakes = 0
        self.solved = False
        self.hint_cell = None
        self.hint_timer = 0
        self.victory_timer = 0
        self.victory_particles = []
        self.selected_cell = None
        self.highlight_cells = set()
        self.same_number_cells = set()
    
    def solve(self):
        """Solve the current puzzle"""
        if self.solved:
            return
        
        solution = self.solver.solve(self.user_board)
        if solution:
            self.solution = solution
            self.user_board = solution
            self.solved = True
            self.hint_cell = None
            self.victory_timer = 0
            self.create_victory_particles()
    
    def hint(self):
        """Give a hint by filling one correct cell"""
        if self.solved:
            return
        
        for i in range(9):
            for j in range(9):
                if self.user_board[i][j] == 0:
                    self.user_board[i][j] = self.solution[i][j]
                    self.hints_used += 1
                    self.hint_cell = (i, j)
                    self.hint_timer = 120
                    return
        
        self.solved = True
        self.create_victory_particles()
    
    def create_victory_particles(self):
        """Create celebration particles for victory"""
        for _ in range(100):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            self.victory_particles.append({
                'x': random.randint(50, WIDTH - 50),
                'y': random.randint(50, HEIGHT - 50),
                'vx': speed * math.cos(angle),
                'vy': speed * math.sin(angle) - 3,
                'life': 1.0,
                'color': random.choice([NEON_GREEN, NEON_BLUE, NEON_YELLOW, NEON_RED, VICTORY_GOLD]),
                'size': random.uniform(2, 6),
                'gravity': 0.1
            })
    
    def update_victory_particles(self):
        """Update victory particles"""
        for p in self.victory_particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += p['gravity']
            p['life'] -= 0.01
            if p['life'] <= 0:
                self.victory_particles.remove(p)
    
    def select_cell(self, row, col):
        """Select a cell"""
        if self.solved:
            return
        
        self.selected_cell = (row, col)
        self.update_highlights(row, col)
        if self.hint_cell:
            self.hint_cell = None
            self.hint_timer = 0
    
    def update_highlights(self, row, col):
        """Update highlighted cells"""
        self.highlight_cells = set()
        self.same_number_cells = set()
        
        if row is None or col is None:
            return
        
        for i in range(9):
            self.highlight_cells.add((row, i))
            self.highlight_cells.add((i, col))
        
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                self.highlight_cells.add((box_row + i, box_col + j))
        
        if self.user_board[row][col] != 0:
            num = self.user_board[row][col]
            for i in range(9):
                for j in range(9):
                    if self.user_board[i][j] == num and (i, j) != (row, col):
                        self.same_number_cells.add((i, j))
    
    def input_number(self, num):
        """Input a number into selected cell"""
        if self.solved or self.selected_cell is None:
            return
        
        row, col = self.selected_cell
        
        if self.given_cells[row][col]:
            return
        
        if num == 0:
            self.user_board[row][col] = 0
            self.error_cells.discard((row, col))
            return
        
        if num == self.solution[row][col]:
            self.user_board[row][col] = num
            self.error_cells.discard((row, col))
            
            solved = True
            for i in range(9):
                for j in range(9):
                    if self.user_board[i][j] != self.solution[i][j]:
                        solved = False
                        break
                if not solved:
                    break
            
            if solved:
                self.solved = True
                self.create_victory_particles()
        else:
            self.user_board[row][col] = num
            self.error_cells.add((row, col))
            self.mistakes += 1
    
    def draw_background(self):
        """Draw gradient background"""
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            r = int(BG_GRADIENT_TOP[0] * (1 - ratio) + BG_GRADIENT_BOTTOM[0] * ratio)
            g = int(BG_GRADIENT_TOP[1] * (1 - ratio) + BG_GRADIENT_BOTTOM[1] * ratio)
            b = int(BG_GRADIENT_TOP[2] * (1 - ratio) + BG_GRADIENT_BOTTOM[2] * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))
    
    def draw_grid(self):
        """Draw the Sudoku grid"""
        for i in range(9):
            for j in range(9):
                x = GRID_OFFSET_X + j * CELL_SIZE
                y = GRID_OFFSET_Y + i * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                
                if (i, j) in self.error_cells:
                    color = CELL_BG_ERROR
                elif (i, j) == self.selected_cell:
                    color = CELL_BG_SELECTED
                elif (i, j) in self.highlight_cells:
                    color = CELL_BG_HIGHLIGHT
                elif (i, j) in self.same_number_cells:
                    color = CELL_BG_SAME_NUMBER
                elif self.given_cells[i][j]:
                    color = CELL_BG_GIVEN
                else:
                    color = CELL_BG
                
                pygame.draw.rect(screen, color, rect)
        
        for i in range(10):
            y = GRID_OFFSET_Y + i * CELL_SIZE
            width = 3 if i % 3 == 0 else 1
            color = LINE_BOLD if i % 3 == 0 else LINE_COLOR
            pygame.draw.line(screen, color, (GRID_OFFSET_X, y), 
                           (GRID_OFFSET_X + 9 * CELL_SIZE, y), width)
            
            x = GRID_OFFSET_X + i * CELL_SIZE
            width = 3 if i % 3 == 0 else 1
            color = LINE_BOLD if i % 3 == 0 else LINE_COLOR
            pygame.draw.line(screen, color, (x, GRID_OFFSET_Y), 
                           (x, GRID_OFFSET_Y + 9 * CELL_SIZE), width)
    
    def draw_numbers(self):
        """Draw numbers in cells"""
        for i in range(9):
            for j in range(9):
                if self.user_board[i][j] != 0:
                    x = GRID_OFFSET_X + j * CELL_SIZE + CELL_SIZE // 2
                    y = GRID_OFFSET_Y + i * CELL_SIZE + CELL_SIZE // 2
                    
                    num = self.user_board[i][j]
                    
                    if self.given_cells[i][j]:
                        color = TEXT_GIVEN
                    elif (i, j) in self.error_cells:
                        color = TEXT_ERROR
                    elif self.solved:
                        color = TEXT_SOLVED
                    else:
                        color = TEXT_USER
                    
                    text = font_number.render(str(num), True, color)
                    text_rect = text.get_rect(center=(x, y))
                    screen.blit(text, text_rect)
        
        if self.hint_cell and self.hint_timer > 0:
            i, j = self.hint_cell
            x = GRID_OFFSET_X + j * CELL_SIZE + CELL_SIZE // 2
            y = GRID_OFFSET_Y + i * CELL_SIZE + CELL_SIZE // 2
            
            pulse = abs(math.sin(self.hint_timer * 0.1))
            for r in range(3):
                alpha = int(50 * pulse * (1 - r * 0.3))
                radius = int(CELL_SIZE // 2 + r * 5)
                pygame.draw.circle(screen, (0, 255, 100, alpha), (x, y), radius)
    
    def draw_info(self):
        """Draw game information with clear labels"""
        panel_rect = pygame.Rect(0, 0, WIDTH, 58)
        pygame.draw.rect(screen, (10, 10, 20), panel_rect)
        pygame.draw.rect(screen, (40, 40, 60), panel_rect, 1)
        
        mistakes_text = font_tiny.render(f"Mistakes: {self.mistakes}", True, NEON_RED)
        screen.blit(mistakes_text, (12, 20))

        hints_text = font_tiny.render(f"Hints: {self.hints_used}", True, NEON_BLUE)
        screen.blit(hints_text, (135, 20))

        diff_text = font_tiny.render(f"Difficulty: {self.difficulty}", True, NEON_YELLOW)
        screen.blit(diff_text, (245, 20))

        if self.solved:
            status_text = font_small.render("SOLVED!", True, NEON_GREEN)
        else:
            status_text = font_tiny.render("Click cell to select", True, (150, 150, 200))
        
        status_rect = status_text.get_rect(center=(WIDTH//2, 28))
        screen.blit(status_text, status_rect)

        if self.selected_cell and not self.solved:
            row, col = self.selected_cell
            info_text = font_tiny.render(f"Cell: ({row+1},{col+1})", True, (150, 150, 200))
            screen.blit(info_text, (WIDTH - 130, 20))
    
    def draw_victory_screen(self):
        """Draw victory celebration screen"""
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        for i in range(5):
            alpha = 50 - i * 10
            glow_text = font_large.render("VICTORY!", True, (VICTORY_GOLD[0], VICTORY_GOLD[1], VICTORY_GOLD[2], alpha))
            glow_rect = glow_text.get_rect(center=(WIDTH//2 + i, HEIGHT//2 - 80 + i))
            screen.blit(glow_text, glow_rect)
        
        victory_text = font_large.render("VICTORY!", True, VICTORY_GOLD)
        victory_rect = victory_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 80))
        screen.blit(victory_text, victory_rect)

        stats = [
            f"Mistakes: {self.mistakes}",
            f"Hints Used: {self.hints_used}",
            f"Difficulty: {self.difficulty}"
        ]
        
        for i, stat in enumerate(stats):
            stat_text = font_medium.render(stat, True, TEXT_COLOR)
            stat_rect = stat_text.get_rect(center=(WIDTH//2, HEIGHT//2 + i * 50))
            screen.blit(stat_text, stat_rect)

        restart_text = font_small.render("Press SPACE or click New Game", True, (150, 150, 200))
        restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 160))
        screen.blit(restart_text, restart_rect)

        for p in self.victory_particles:
            alpha = int(p['life'] * 255)
            pygame.draw.circle(screen, (*p['color'], alpha), 
                             (int(p['x']), int(p['y'])), int(p['size'] * p['life']))
    
    def draw_buttons(self):
        """Draw UI buttons"""
        for button in self.buttons:
            color = BUTTON_ACTIVE if button['hover'] else button['color']
            pygame.draw.rect(screen, color, button['rect'], border_radius=8)
            pygame.draw.rect(screen, (100, 100, 150, 50), button['rect'], 2, border_radius=8)
            
            text = font_tiny.render(button['text'], True, TEXT_COLOR)
            text_rect = text.get_rect(center=button['rect'].center)
            screen.blit(text, text_rect)
    
    def draw_number_pad(self):
        """Draw number pad for input"""
        if self.solved:
            return
        
        pad_y = HEIGHT - BUTTON_HEIGHT - 50
        start_x = (WIDTH - 9 * 32) // 2
        
        pad_rect = pygame.Rect(start_x - 10, pad_y - 5, 9 * 32 + 20, 38)
        pygame.draw.rect(screen, (15, 15, 30), pad_rect, border_radius=10)
        pygame.draw.rect(screen, (50, 50, 70), pad_rect, 1, border_radius=10)
        
        for i in range(1, 10):
            x = start_x + (i - 1) * 32
            rect = pygame.Rect(x, pad_y, 28, 28)
            
            color = (45, 45, 65)
            pygame.draw.rect(screen, color, rect, border_radius=5)
            pygame.draw.rect(screen, (70, 70, 90), rect, 1, border_radius=5)
            
            text = font_number.render(str(i), True, (180, 180, 200))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
    
    def handle_click(self, pos):
        """Handle mouse clicks"""
        x, y = pos
        
        for button in self.buttons:
            if button['rect'].collidepoint(pos):
                if button['action'] == 'new_game':
                    self.new_game()
                elif button['action'] == 'solve':
                    self.solve()
                elif button['action'] == 'hint':
                    self.hint()
                elif button['action'] == 'reset':
                    self.reset()
                return
        
        if self.solved:
            return
        
        grid_end_x = GRID_OFFSET_X + 9 * CELL_SIZE
        grid_end_y = GRID_OFFSET_Y + 9 * CELL_SIZE
        
        if GRID_OFFSET_X <= x <= grid_end_x and GRID_OFFSET_Y <= y <= grid_end_y:
            col = (x - GRID_OFFSET_X) // CELL_SIZE
            row = (y - GRID_OFFSET_Y) // CELL_SIZE
            if 0 <= row < 9 and 0 <= col < 9:
                self.select_cell(row, col)
                return
        
        if not self.solved:
            pad_y = HEIGHT - BUTTON_HEIGHT - 50
            start_x = (WIDTH - 9 * 32) // 2
            if pad_y <= y <= pad_y + 28:
                for i in range(1, 10):
                    num_x = start_x + (i - 1) * 32
                    if num_x <= x <= num_x + 28:
                        self.input_number(i)
                        return
        
        self.selected_cell = None
        self.highlight_cells = set()
        self.same_number_cells = set()
    
    def update(self):
        """Update game state"""
        if self.hint_timer > 0:
            self.hint_timer -= 1
            if self.hint_timer == 0:
                self.hint_cell = None
        
        if self.solved:
            self.victory_timer += 1
            self.update_victory_particles()
            if len(self.victory_particles) < 50 and self.victory_timer % 5 == 0:
                self.create_victory_particles()
    
    def run(self):
        """Main game loop"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                
                if event.type == pygame.MOUSEMOTION:
                    for button in self.buttons:
                        button['hover'] = button['rect'].collidepoint(event.pos)
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    
                    if event.key == pygame.K_SPACE and self.solved:
                        self.new_game()
                    
                    if not self.solved and self.selected_cell:
                        if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                            self.input_number(0)
                        elif pygame.K_1 <= event.key <= pygame.K_9:
                            num = event.key - pygame.K_0
                            self.input_number(num)
            
            self.update()
            self.draw_background()
            self.draw_info()
            self.draw_grid()
            self.draw_numbers()
            self.draw_number_pad()
            self.draw_buttons()
            
            if self.solved:
                self.draw_victory_screen()
            
            pygame.display.flip()
            clock.tick(FPS)

def main():
    print("="*50)
    print("SUDOKU")
    print("="*50)
    print("Controls:")
    print("  Click on a cell to select it")
    print("  Press 1-9 to enter a number")
    print("  Press BACKSPACE/DELETE to clear")
    print("  Click buttons for actions")
    print("="*50)
    print("Features:")
    print("  New Game - Start a new puzzle")
    print("  Solve - Auto-solve the puzzle")
    print("  Hint - Get a hint (green glow)")
    print("  Reset - Reset to initial state")
    print("="*50)
    print("When you complete the puzzle, a victory")
    print("  screen will appear with your stats!")
    print("="*50)
    
    game = SudokuGame()
    game.run()

if __name__ == "__main__":
    main()