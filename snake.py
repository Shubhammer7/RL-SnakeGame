import pygame

class Snake:
    def __init__(self, screen, block_size=20):
        self.screen = screen
        self.block = block_size

        self.direction = "RIGHT"
        self.positions = [(200, 200)]
        self.grow = False

    def get_head(self):
        return self.positions[0]

    def change_direction(self, direction):
        opposites = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT"
        }
        if direction != opposites.get(self.direction):
            self.direction = direction

    def move(self):
        x, y = self.get_head()

        if self.direction == "UP":
            y -= self.block
        elif self.direction == "DOWN":
            y += self.block
        elif self.direction == "LEFT":
            x -= self.block
        elif self.direction == "RIGHT":
            x += self.block

        new_head = (x, y)
        self.positions.insert(0, new_head)

        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False

    def draw(self):
        for x, y in self.positions:
            pygame.draw.rect(
                self.screen.window,
                "white",
                pygame.Rect(x, y, self.block, self.block)
            )

    def check_self_collision(self):
        return self.get_head() in self.positions[1:]

    def check_wall_collision(self):
        x, y = self.get_head()
        return (
            x < 0 or
            y < 0 or
            x >= self.screen.width or
            y >= self.screen.height
        )
