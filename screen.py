import pygame

class Screen:
    def __init__(self, width, height=720):
        self.window = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

    def window_fill(self):
        self.window.fill("black")

    def update(self):
        pygame.display.update()
        self.clock.tick(60)
