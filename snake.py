import pygame

class Snake:
    def __init__(self, screen):
        self.screen = screen
        self.x = 20
        self.y = 20
        self.size = 20

    def body(self):
        pygame.draw.rect(
            self.screen.window,
            "white",
            pygame.Rect(self.x, self.y, self.size, self.size)
        )
