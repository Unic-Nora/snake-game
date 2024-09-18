import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Snake class
class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.grow_pending = False

    def move(self):
        head = (self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1])
        self.body.insert(0, head)
        if not self.grow_pending:
            self.body.pop()
        else:
            self.grow_pending = False

    def grow(self):
        self.grow_pending = True

    def check_collision(self):
        collision = (self.body[0] in self.body[1:] or
                     self.body[0][0] < 0 or self.body[0][0] >= GRID_WIDTH or
                     self.body[0][1] < 0 or self.body[0][1] >= GRID_HEIGHT)
        if collision:
            print(f"Collision detected: Head at {self.body[0]}")
        return collision

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def speed_selection_menu():
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    speeds = ["Slow", "Medium", "Fast"]
    selected = 1  # Default to Medium

    while True:
        screen.fill(BLACK)
        draw_text("Select Game Speed", font, WHITE, screen, 200, 50)

        for i, speed in enumerate(speeds):
            color = BLUE if i == selected else WHITE
            draw_text(speed, font, color, screen, 250, 150 + i * 50)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(speeds)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(speeds)
                elif event.key == pygame.K_RETURN:
                    return selected

        clock.tick(30)

# Game loop
def main():
    speed_choice = speed_selection_menu()
    if speed_choice is None:
        return  # User closed the window

    SNAKE_SPEED = [3, 7, 15][speed_choice]  # Adjusted speed values

    clock = pygame.time.Clock()
    snake = Snake()
    food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    score = 0

    running = True
    move_cooldown = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != (0, 1):
                    snake.direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                    snake.direction = (0, 1)
                elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                    snake.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                    snake.direction = (1, 0)

        move_cooldown += clock.get_time()
        if move_cooldown >= 1000 / SNAKE_SPEED:
            move_cooldown = 0
            
            # Check if the snake will eat food before moving
            next_head = (snake.body[0][0] + snake.direction[0], snake.body[0][1] + snake.direction[1])
            if next_head == food:
                snake.grow()
                food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
                score += 1
            
            snake.move()

            if snake.check_collision():
                print(f"Game Over! Final Score: {score}")
                running = False

        screen.fill(BLACK)
        for segment in snake.body:
            pygame.draw.circle(screen, GREEN, (segment[0] * GRID_SIZE + GRID_SIZE // 2, segment[1] * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 2)
        pygame.draw.rect(screen, RED, (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)  # Set a consistent frame rate

    pygame.quit()

if __name__ == "__main__":
    main()