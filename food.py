import pygame
import random

class Food:
    def __init__(self, screen, block_size=20):
        self.screen = screen
        self.block = block_size
        self.position = self.spawn()

    def spawn(self):
        x = random.randrange(0, self.screen.width, self.block)
        y = random.randrange(0, self.screen.height, self.block)
        return (x, y)

    def draw(self):
        x, y = self.position
        pygame.draw.rect(
            self.screen.window,
            "red",
            pygame.Rect(x, y, self.block, self.block)
        )
