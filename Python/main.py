import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up the game window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Snake Game")

# Define colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Define game variables
SNAKE_SIZE = 10
SNAKE_SPEED = 15


# Function to draw the game objects
def draw_game_objects():
    # Clear the window
    window.fill(BLACK)

    # Draw the snake
    for segment in snake_body:
        pygame.draw.rect(
            window, GREEN, (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE)
        )

    # Draw the food
    pygame.draw.rect(window, RED, (food_x, food_y, SNAKE_SIZE, SNAKE_SIZE))

    # Update the display
    pygame.display.update()


# Initialize the snake's position and body
snake_x = WINDOW_WIDTH // 2
snake_y = WINDOW_HEIGHT // 2
snake_body = [(snake_x, snake_y)]

# Generate the food's initial position
food_x = random.randrange(SNAKE_SIZE, WINDOW_WIDTH - SNAKE_SIZE, SNAKE_SIZE)
food_y = random.randrange(SNAKE_SIZE, WINDOW_HEIGHT - SNAKE_SIZE, SNAKE_SIZE)

# Set the initial movement direction
direction = "RIGHT"

# Game loop
running = True
game_over = False
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"
            elif event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"

    # Check if the game is over
    if (
        snake_x < 0
        or snake_x >= WINDOW_WIDTH
        or snake_y < 0
        or snake_y >= WINDOW_HEIGHT
    ):
        game_over = True

    # Move the snake only if the game is not over
    if not game_over:
        if direction == "LEFT":
            snake_x -= SNAKE_SIZE
        elif direction == "RIGHT":
            snake_x += SNAKE_SIZE
        elif direction == "UP":
            snake_y -= SNAKE_SIZE
        else:
            snake_y += SNAKE_SIZE

        # Add the new head position to the snake's body
        snake_body.insert(0, (snake_x, snake_y))

        # Check if the snake has eaten the food
        if snake_x == food_x and snake_y == food_y:
            # Generate a new food position
            food_x = random.randrange(SNAKE_SIZE, WINDOW_WIDTH - SNAKE_SIZE, SNAKE_SIZE)
            food_y = random.randrange(
                SNAKE_SIZE, WINDOW_HEIGHT - SNAKE_SIZE, SNAKE_SIZE
            )
        else:
            # Remove the last segment of the snake's body
            snake_body.pop()

    # Draw the game objects
    draw_game_objects()

    # Pause for a short time to control the snake's speed
    if not game_over:
        pygame.time.delay(100)

# Pause for 2 seconds before quitting
time.sleep(2)

# Quit Pygame
pygame.quit()
