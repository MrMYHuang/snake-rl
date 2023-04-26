import pygame
import snake

game = snake.Game(40, 40, 20)
while True:
    # Handle events
    action = -1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                action = 0
            elif event.key == pygame.K_RIGHT:
                action = 2
            elif event.key == pygame.K_UP:
                action = 3
            elif event.key == pygame.K_DOWN:
                action = 1

    _, __, done, ___, ____ = game.step(action)
    if done:
        break
    else:
        game.render()