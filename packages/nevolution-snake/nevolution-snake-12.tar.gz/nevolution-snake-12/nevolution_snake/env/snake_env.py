import gym
import numpy as np
from gym import spaces
from numpy import int32

from time import sleep
from random import randint

from nevolution_snake.logic.gamelogic import GameLogic
from nevolution_snake.view.snake_gui import SnakeGui
from nevolution_snake import constants as c


class SnakeEnv(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 10
    }

    def __init__(self):
        self.state = None
        self.done = False
        self.gameLogic = GameLogic(32, 32, c.SEED, c.SCORE_SEED, randint(3, 100))
        self.gui = SnakeGui(game_logic=self.gameLogic, )
        self.lastDirection = 0
        """
        action space is defined as a natural number between 0 and 3
        the number will be saved into a list witt one element
        accessible with an index [0]
        example: input = action[0]
        """
        self.action_space = spaces.Discrete(4)

        """
        observation space is defined as a 32x32 matrix of integers between 0 and 4
        the matrix is build like a matrix from numpy
        example:
        [[0,0,0]
         [1,2,3
         [4,4,4]]
        accessible through the index
        example: pixelValue = observation[1,2]
        """
        self.observation_space = spaces.Box(low=0, high=4, shape=(32, 32), dtype=int32)

    def step(self, action):
        if action is None:
            action = self.lastDirection
        if self.gameLogic.play(action) == 1:
            self.reset()
            self.done = True
        else:
            self.done = False
        self.lastDirection = action

        """
        creating observation
        0 = empty 
        1 = snake body
        2 = snake head
        3 = snake tail
        4 = collectible food
        """
        observation = np.zeros((32, 32))
        snake = self.gameLogic.get_snake()
        for body in snake:
            observation[body[0], body[1]] = 1
        head = snake[len(snake) - 1]
        tail = snake[0]
        observation[head[0], head[1]] = 2
        observation[tail[0], head[1]] = 3
        food = self.gameLogic.get_food()
        observation[food[0], food[1]] = 4

        return self.gameLogic.get_detect(), self.gameLogic.get_current_reward(), self.done, ()

    def reset(self):
        self.gameLogic = GameLogic(32, 32, c.SEED, c.SCORE_SEED, randint(3, 100))
        self.gui.game_logic = self.gameLogic
        return self.gameLogic.get_detect()

    def render(self, mode='human'):
        if mode == 'rgb_array':
            return self.gui.render(mode)
        else:
            self.gui.render(mode)
            sleep(0.1)

    def quit(self):
        self.gui.quit()
