import pygame
from screen import Screen
from snake import Snake
from food import Food

pygame.init()

screen = Screen()
snake = Snake(screen)
food = Food(screen)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction("UP")
            elif event.key == pygame.K_DOWN:
                snake.change_direction("DOWN")
            elif event.key == pygame.K_LEFT:
                snake.change_direction("LEFT")
            elif event.key == pygame.K_RIGHT:
                snake.change_direction("RIGHT")

    snake.move()

    if snake.get_head() == food.position:
        snake.grow = True
        food.position = food.spawn()

    if snake.check_self_collision() or snake.check_wall_collision():
        running = False

    screen.clear()
    snake.draw()
    food.draw()
    screen.update()

pygame.quit()
