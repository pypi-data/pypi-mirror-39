from time import sleep

import pygame

from nevolution_snake.env import SnakeEnv


def human():
    env = SnakeEnv()
    running = True
    loop = False
    up = 0
    right = 0.25
    down = 0.5
    left = 0.75

    env.render()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                env.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == 273:
                    observation, reward, done, info = env.step(up)
                    env.render()
                if event.key == pygame.K_RIGHT or event.key == 275:
                    observation, reward, done, info = env.step(right)
                    env.render()
                if event.key == pygame.K_DOWN or event.key == 274:
                    observation, reward, done, info = env.step(down)
                    env.render()
                if event.key == pygame.K_LEFT or event.key == 276:
                    observation, reward, done, info = env.step(left)
                    env.render()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    loop = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    loop = False
        if loop:
            env.step(None)
            env.render()
            sleep(1 / 100)
