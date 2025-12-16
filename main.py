import pygame
from screen import Screen
from snake import Snake

pygame.init()

screen = Screen(width=1280)
snake = Snake(screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.window_fill()
    snake.body()
    screen.update()

pygame.quit()
