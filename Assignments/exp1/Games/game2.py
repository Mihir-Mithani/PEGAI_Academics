import pygame
import random
import sys
import os
import sys

# Check if a graphical display is available
if os.environ.get("DISPLAY", "") == "":
    print("Error: No graphical display found.")
    print("Run this program in a local Python environment (IDLE, VS Code, PyCharm, Terminal, etc.).")
    sys.exit()

# ==========================================
# CONSTANTS & CONFIGURATION
# ==========================================
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Color Palette (Modern Dark Theme)
COLOR_BG = (30, 30, 46)          # Dark Slate
COLOR_GRID = (40, 40, 60)        # Subtle Grid Lines
COLOR_SNAKE_HEAD = (166, 227, 161)# Vibrant Green
COLOR_SNAKE_BODY = (144, 207, 139)# Muted Green
COLOR_FOOD = (243, 139, 168)      # Coral Red
COLOR_TEXT = (205, 214, 244)      # Off-White
COLOR_PANEL = (49, 50, 68)        # Dark Gray for UI Box
COLOR_BTN = (137, 180, 250)       # Soft Blue
COLOR_BTN_HOVER = (180, 190, 254) # Lighter Blue
COLOR_BTN_TEXT = (17, 17, 27)     # Almost Black

# Game Settings
INITIAL_SPEED = 10        # Frames per second (snake moves 1 tile per frame)
SPEED_INCREMENT = 1       # How much speed increases per milestone
SCORE_PER_FOOD = 10       # Points per food item
MILESTONE_SCORE = 30      # Increase speed every 30 points

# Direction Vectors
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    """Represents the Snake, handling movement, growth, and collision detection."""

    def __init__(self):
        self.reset()

    def reset(self):
        # Start at the center of the grid
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        self.body = [(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)]
        self.direction = RIGHT
        self.next_direction = RIGHT  # Buffer to prevent 180-degree self-collisions
        self.grow_flag = False

    def change_direction(self, new_dir):
        """Prevents reversing directly onto oneself."""
        opposite = (-self.direction[0], -self.direction[1])
        if new_dir != opposite:
            self.next_direction = new_dir

    def update(self):
        """Moves the snake forward and handles body growth."""
        self.direction = self.next_direction
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)

        # Insert new head position
        self.body.insert(0, new_head)

        # Remove tail unless growing
        if not self.grow_flag:
            self.body.pop()
        else:
            self.grow_flag = False

    def grow(self):
        """Schedules snake growth on the next movement step."""
        self.grow_flag = True

    def check_wall_collision(self):
        """Returns True if the head collides with any outer wall."""
        head_x, head_y = self.body[0]
        return not (0 <= head_x < GRID_WIDTH and 0 <= head_y < GRID_HEIGHT)

    def check_self_collision(self):
        """Returns True if the head collides with any part of its body."""
        return self.body[0] in self.body[1:]

    def draw(self, surface):
        """Draws the snake on the given Pygame surface."""
        for i, segment in enumerate(self.body):
            rect = pygame.Rect(
                segment[0] * GRID_SIZE,
                segment[1] * GRID_SIZE,
                GRID_SIZE - 1,  # -1 leaves a small space for visual separation
                GRID_SIZE - 1
            )
            color = COLOR_SNAKE_HEAD if i == 0 else COLOR_SNAKE_BODY
            pygame.draw.rect(surface, color, rect, border_radius=4)


class Food:
    """Represents the consumable food item."""

    def __init__(self):
        self.position = (0, 0)

    def spawn(self, snake_body):
        """Spawns food at a random tile that is NOT occupied by the snake."""
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in snake_body:
                self.position = pos
                break

    def draw(self, surface):
        """Draws food as a rounded circle-like rectangle."""
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE + 1,
            self.position[1] * GRID_SIZE + 1,
            GRID_SIZE - 2,
            GRID_SIZE - 2
        )
        pygame.draw.rect(surface, COLOR_FOOD, rect, border_radius=8)


class Game:
    """Main Game Manager controlling state, rendering, and logic flow."""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Python Snake Game")

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        # Fonts
        self.font_main = pygame.font.SysFont("Consolas", 24, bold=True)
        self.font_title = pygame.font.SysFont("Consolas", 48, bold=True)

        # Game Entities
        self.snake = Snake()
        self.food = Food()

        # Game State Variables
        self.score = 0
        self.high_score = 0
        self.current_speed = INITIAL_SPEED
        self.game_over = False

        # Initial food spawn
        self.food.spawn(self.snake.body)

    def reset_game(self):
        """Resets the game state back to start."""
        self.snake.reset()
        self.food.spawn(self.snake.body)
        self.score = 0
        self.current_speed = INITIAL_SPEED
        self.game_over = False

    def process_events(self):
        """Handles keyboard and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Snake Movement Controls
                if not self.game_over:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.snake.change_direction(UP)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.snake.change_direction(DOWN)
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        self.snake.change_direction(LEFT)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.snake.change_direction(RIGHT)
                else:
                    # Quick restart via Space key during Game Over
                    if event.key == pygame.K_SPACE:
                        self.reset_game()

            # Mouse Click for Restart Button
            if event.type == pygame.MOUSEBUTTONDOWN and self.game_over:
                if event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    if self.get_restart_button_rect().collidepoint(mouse_pos):
                        self.reset_game()

    def update(self):
        """Updates game state logic per frame."""
        if self.game_over:
            return

        self.snake.update()

        # Check Collisions
        if self.snake.check_wall_collision() or self.snake.check_self_collision():
            self.game_over = True
            if self.score > self.high_score:
                self.high_score = self.score
            return

        # Check Food Consumption
        if self.snake.body[0] == self.food.position:
            self.snake.grow()
            self.score += SCORE_PER_FOOD
            self.food.spawn(self.snake.body)

            # Increase Speed dynamic scaling
            if self.score % MILESTONE_SCORE == 0:
                self.current_speed += SPEED_INCREMENT

    def draw_grid(self):
        """Renders subtle background grid lines."""
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, COLOR_GRID, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, COLOR_GRID, (0, y), (SCREEN_WIDTH, y))

    def get_restart_button_rect(self):
        """Utility to compute restart button bounding box."""
        btn_w, btn_h = 200, 50
        return pygame.Rect(
            SCREEN_WIDTH // 2 - btn_w // 2,
            SCREEN_HEIGHT // 2 + 60,
            btn_w,
            btn_h
        )

    def draw_hud(self):
        """Renders score and dynamic speed display on screen."""
        score_surface = self.font_main.render(f"Score: {self.score}", True, COLOR_TEXT)
        high_score_surface = self.font_main.render(f"High Score: {self.high_score}", True, COLOR_TEXT)
        speed_surface = self.font_main.render(f"Speed: {self.current_speed} FPS", True, COLOR_TEXT)

        self.screen.blit(score_surface, (15, 10))
        self.screen.blit(high_score_surface, (200, 10))
        self.screen.blit(speed_surface, (SCREEN_WIDTH - 200, 10))

    def draw_game_over(self):
        """Renders overlay screen on game over."""
        # Semi-transparent backdrop overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((15, 15, 23))
        self.screen.blit(overlay, (0, 0))

        # Game Over Title
        title_surf = self.font_title.render("GAME OVER", True, COLOR_FOOD)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(title_surf, title_rect)

        # Final Score Text
        score_surf = self.font_main.render(f"Final Score: {self.score}", True, COLOR_TEXT)
        score_rect = score_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(score_surf, score_rect)

        # Render Interactive Button
        btn_rect = self.get_restart_button_rect()
        mouse_pos = pygame.mouse.get_pos()

        # Hover effect
        btn_color = COLOR_BTN_HOVER if btn_rect.collidepoint(mouse_pos) else COLOR_BTN

        pygame.draw.rect(self.screen, btn_color, btn_rect, border_radius=10)

        # Button Text
        btn_text_surf = self.font_main.render("RESTART", True, COLOR_BTN_TEXT)
        btn_text_rect = btn_text_surf.get_rect(center=btn_rect.center)
        self.screen.blit(btn_text_surf, btn_text_rect)

        # Prompt Info
        hint_surf = self.font_main.render("Or press SPACE to play again", True, COLOR_TEXT)
        hint_rect = hint_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 130))
        self.screen.blit(hint_surf, hint_rect)

    def draw(self):
        """Master render function."""
        self.screen.fill(COLOR_BG)
        self.draw_grid()

        # Render Game Entities
        self.food.draw(self.screen)
        self.snake.draw(self.screen)
        self.draw_hud()

        # Render Overlays
        if self.game_over:
            self.draw_game_over()

        pygame.display.flip()

    def run(self):
        """Main Loop."""
        while True:
            self.process_events()
            self.update()
            self.draw()
            # Dynamic frame rate based on game speed
            self.clock.tick(self.current_speed)


# ==========================================
# ENTRY POINT
# ==========================================
if __name__ == "__main__":
    game = Game()
    game.run()