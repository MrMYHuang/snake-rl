from typing import Any, Tuple
import pygame
import random
import gym
from gym.spaces import Box, Discrete
import numpy as np

# Define some constants
FPS = 10

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class SnakeEnv(gym.Env):
    GRID_WIDTH = 6
    GRID_HEIGHT = 6
    def __init__(self):
        self.game = Game(SnakeEnv.GRID_WIDTH, SnakeEnv.GRID_HEIGHT, 20)
        self.action_space = Discrete(4)
        self.observation_space = Box(low=np.array([0, 0, 0]), high=np.array([self.game.GRID_WIDTH, self.game.GRID_HEIGHT, 4]))

    def reset(self, *, seed: int | None = None, options: dict | None = None) -> Tuple:
        return self.game.reset()
    
    def step(self, action: int) -> Tuple:
        return self.game.step(action=action)
    
    def render(self):
        self.game.render()

# Define the Snake class
class Game:
    def __init__(self, GRID_WIDTH, GRID_HEIGHT, BLOCK_SIZE):
        import os
        os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
        self.GRID_WIDTH = GRID_WIDTH
        self.GRID_HEIGHT = GRID_HEIGHT
        self.BLOCK_SIZE = BLOCK_SIZE
        # Set up the screen
        self.SCREEN_WIDTH = GRID_WIDTH * BLOCK_SIZE
        self.SCREEN_HEIGHT = GRID_HEIGHT * BLOCK_SIZE
        # Initialize Pygame
        pygame.init()
        pygame.display.set_caption("Snake Game")
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.snake = Snake(GRID_WIDTH, GRID_HEIGHT, BLOCK_SIZE)
        self.food = Food(GRID_WIDTH, GRID_HEIGHT, BLOCK_SIZE)
        # Set up the clock
        self.clock = pygame.time.Clock()

    def reset(self):
        self.snake.reset()
        return (self.snake.headGrid()+ (self.snake.dir(),), {})
    
    def step(self, action: int) -> Tuple:
        if action != -1:
            self.snake.change_dir(action=action)
        self.snake.move()
    
        # Check for collision with Food
        if self.snake.x == self.food.x and self.snake.y == self.food.y:
            self.snake.grow()
            self.food = Food(self.GRID_WIDTH, self.GRID_HEIGHT, self.BLOCK_SIZE)
            reward = 1
        else:
            reward = 0
        
        # Check for collision with Snake or wall
        done = self.snake.check_collision()

        if done:
            reward = -100
            head = self.snake.body[0]
            self.snake.body[0] = (head[0] - self.snake.dx,  head[1] - self.snake.dy)

        return (self.snake.headGrid() + (self.snake.dir(),), reward, done, False, {})
    
    def render(self):
        self.screen.fill(BLACK)
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        # Update the screen
        pygame.display.update()

        # Wait for the next frame
        self.clock.tick(FPS)

# Define the Snake class
class Snake:
    def __init__(self, GRID_WIDTH, GRID_HEIGHT, BLOCK_SIZE):
        self.GRID_WIDTH = GRID_WIDTH
        self.GRID_HEIGHT = GRID_HEIGHT
        self.BLOCK_SIZE = BLOCK_SIZE
        self.reset()

    def reset(self):
        self.x = self.GRID_WIDTH / 2 * self.BLOCK_SIZE
        self.y = self.GRID_HEIGHT / 2 * self.BLOCK_SIZE
        self.dx = self.BLOCK_SIZE
        self.dy = 0
        self.body = [(self.x, self.y)]

    def headGrid(self):
        head = self.body[0]
        return (int(head[0] / self.BLOCK_SIZE), int(head[1] / self.BLOCK_SIZE))
    
    def dir(self):
        if self.dx < 0 and self.dy == 0:
            return 0
        elif self.dx == 0 and self.dy > 0:
            return 1
        if self.dx > 0 and self.dy == 0:
            return 2
        else:
            return 3
        
    def change_dir(self, action: int):
        if action == 0 and self.dx == 0:
            self.dx = -self.BLOCK_SIZE
            self.dy = 0
        elif action == 2 and self.dx == 0:
            self.dx = self.BLOCK_SIZE
            self.dy = 0
        elif action == 3 and self.dy == 0:
            self.dx = 0
            self.dy = -self.BLOCK_SIZE
        elif action == 1 and self.dy == 0:
            self.dx = 0
            self.dy = self.BLOCK_SIZE
    
    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.body.insert(0, (self.x, self.y))
        self.body.pop()
    
    def grow(self):
        self.body.append((self.x - self.dx, self.y - self.dy))

    def draw(self, surface):
        for x, y in self.body:
            rect = pygame.Rect(x, y, self.BLOCK_SIZE, self.BLOCK_SIZE)
            pygame.draw.rect(surface, GREEN, rect)
    
    def check_collision(self):
        if self.x < 0 or self.x >= self.GRID_WIDTH * self.BLOCK_SIZE or self.y < 0 or self.y >= self.GRID_HEIGHT * self.BLOCK_SIZE:
            return True
        '''
        for x, y in self.body[1:]:
            if self.x == x and self.y == y:
                return False
        '''
        return False

# Define the Food class
class Food:
    def __init__(self, GRID_WIDTH, GRID_HEIGHT, BLOCK_SIZE):
        self.BLOCK_SIZE = BLOCK_SIZE
        self.x = random.randint(1, GRID_WIDTH - 2) * BLOCK_SIZE
        self.y = random.randint(1, GRID_HEIGHT - 2) * BLOCK_SIZE
    
    def draw(self, surface):
        rect = pygame.Rect(self.x, self.y, self.BLOCK_SIZE, self.BLOCK_SIZE)
        pygame.draw.rect(surface, RED, rect)
