import numpy as np
import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
BLOCK_SIZE = 20
SPEED = 15
WINDOW_SIZE = 400
ROWS = WINDOW_SIZE // BLOCK_SIZE

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Directions
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3


class SnakeGameAI:
    def __init__(self):
        self.display = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("AI Snake Game")
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.snake = [(ROWS // 2, ROWS // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.food = self._place_food()
        self.score = 0
        self.head = self.snake[0]  # Initialize the head attribute

    def _place_food(self):
        while True:
            food = (random.randint(0, ROWS - 1), random.randint(0, ROWS - 1))
            if food not in self.snake:
                return food

    def play_step(self, action):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self._move(action)
        self.snake.insert(0, self.head)

        reward = 0
        game_over = False
        if self.head == self.food:
            self.score += 1
            reward = 10
            self.food = self._place_food()
        else:
            self.snake.pop()

        if self._is_collision(self.head):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        self._update_ui()
        self.clock.tick(SPEED)

        return reward, game_over, self.score

    def _is_collision(self, point=None):
        if point is None:
            point = self.head
        if point[0] >= ROWS or point[0] < 0 or point[1] >= ROWS or point[1] < 0:
            return True
        if point in self.snake[1:]:
            return True
        return False

    def _move(self, action):
        clock_wise = [UP, RIGHT, DOWN, LEFT]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]  # no change
        elif np.array_equal(action, [0, 1, 0]):
            new_dir = clock_wise[(idx + 1) % 4]  # right turn r -> d -> l -> u
        else:  # [0, 0, 1]
            new_dir = clock_wise[(idx - 1) % 4]  # left turn l -> u -> r -> d

        self.direction = new_dir

        x, y = self.snake[0]
        if self.direction == UP:
            self.head = (x, y - 1)
        elif self.direction == DOWN:
            self.head = (x, y + 1)
        elif self.direction == LEFT:
            self.head = (x - 1, y)
        elif self.direction == RIGHT:
            self.head = (x + 1, y)

    def _update_ui(self):
        self.display.fill(BLACK)

        for block in self.snake:
            pygame.draw.rect(
                self.display,
                GREEN,
                pygame.Rect(
                    block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE
                ),
            )

        pygame.draw.rect(
            self.display,
            RED,
            pygame.Rect(
                self.food[0] * BLOCK_SIZE,
                self.food[1] * BLOCK_SIZE,
                BLOCK_SIZE,
                BLOCK_SIZE,
            ),
        )

        pygame.display.flip()
