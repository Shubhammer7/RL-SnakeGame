import pygame

class Screen:
    def __init__(self, width=1280, height=720):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()

    def clear(self):
        self.window.fill("black")

    def update(self, fps=60):
        pygame.display.update()
        self.clock.tick(fps)
