import nevolution_snake.constants.constants as constants
from gym.envs.registration import register

register(
    id='nevolution-snake-v0',
    entry_point='nevolution_snake.env:SnakeEnv',
)