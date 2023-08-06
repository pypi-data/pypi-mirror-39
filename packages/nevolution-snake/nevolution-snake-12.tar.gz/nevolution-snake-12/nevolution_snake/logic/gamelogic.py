import random
import numpy as np


class GameLogic(object):

    def __init__(self, width, height, seed, score_seed, new_seed):
        self.snake = [(int(width / 2) - 1, int(height / 2) - 1)]
        self.food = (-1, -1)
        self.direction = None
        self.expand = False
        self.score = 0
        self.reward = 0
        self.height = height
        self.width = width

        self.score_seed = score_seed
        self.new_seed = new_seed
        self.seed = seed
        random.seed(seed)

        self._spawn_food()

    def _spawn_food(self):
        if len(self.snake) == (self.width * self.height):
            # you win
            return
        while self.seed != self.new_seed:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break
        if self.score == self.score_seed:
            self.seed = self.new_seed
            random.seed(self.seed)

    def _eat(self):
        self.food = (-1, -1)
        self.score += 1
        self.reward += 1
        self.expand = True

        self._spawn_food()

    def _move(self):
        if not self.expand:
            self.snake.pop(0)
        else:
            self.expand = False

        x = self.snake[len(self.snake) - 1][0]
        y = self.snake[len(self.snake) - 1][1]
        if self.direction == "up":
            self.snake.append((x, y - 1))
        if self.direction == "right":
            self.snake.append((x + 1, y))
        if self.direction == "down":
            self.snake.append((x, y + 1))
        if self.direction == "left":
            self.snake.append((x - 1, y))

        if self.snake[len(self.snake) - 1] == self.food:
            self._eat()

    def _interpret_direction(self, raw_direction):
        direct = raw_direction
        if direct == 0 and not self.direction == "down":
            self.direction = "up"
        elif direct == 1 and not self.direction == "left":
            self.direction = "right"
        elif direct == 2 and not self.direction == "up":
            self.direction = "down"
        elif direct == 3 and not self.direction == "right":
            self.direction = "left"

        self._move()

    def _detect_collision(self):
        snakebody = self.snake[:-1]
        if self.snake[len(self.snake) - 1] in snakebody:
            return 1  # gameover
        if self.snake[len(self.snake) - 1][0] < 0:
            return 1
        if self.snake[len(self.snake) - 1][0] >= self.width:
            return 1
        if self.snake[len(self.snake) - 1][1] < 0:
            return 1
        if self.snake[len(self.snake) - 1][1] >= self.height:
            return 1
        return 0

    def play(self, direct):
        if len(self.snake) == 1:
            # init snake
            start_x = int(self.width / 2) - 1
            start_y = int(self.height / 2) - 1
            if direct == 0:
                self.snake = [(start_x, start_y + 2), (start_x, start_y + 1), (start_x, start_y)]
            elif direct == 1:
                self.snake = [(start_x - 2, start_y), (start_x - 1, start_y), (start_x, start_y)]
            elif direct == 2:
                self.snake = [(start_x, start_y - 2), (start_x, start_y - 1), (start_x, start_y)]
            else:
                self.snake = [(start_x + 2, start_y), (start_x + 1, start_y), (start_x, start_y)]
        self._interpret_direction(direct)
        # print(self.get_detect())
        return self._detect_collision()

    def get_score(self):
        return self.score

    def get_current_reward(self):
        reward = self.reward
        self.reward = 0
        return reward

    def get_snake(self):
        return self.snake

    def get_food(self):
        return self.food

    def get_detect(self):

        # snakehead
        x = self.snake[len(self.snake) - 1][0]
        y = self.snake[len(self.snake) - 1][1]

        # wall --------------------------------------------------
        # north
        n = (y + 1) / self.height

        # northeast
        if y + 1 < self.width - x:
            ne = (y + 1) / self.height
        else:
            ne = (self.width - x) / self.width

        # east
        e = (self.width - x) / self.width

        # southeast
        if self.width - x < self.height - y:
            se = (self.width - x) / self.width
        else:
            se = (self.height - y) / self.height

        # south
        s = (self.height - y) / self.height

        # southwest
        if self.height - y < x + 1:
            sw = (self.height - y) / self.height
        else:
            sw = (x + 1) / self.width

        # west
        w = (x + 1) / self.width

        # northwest
        if x + 1 < y + 1:
            nw = (x + 1) / self.width
        else:
            nw = (y + 1) / self.height

        ne *= 2
        if ne > 1:
            ne = 1
        se *= 2
        if se > 1:
            se = 1
        sw *= 2
        if sw > 1:
            sw = 1
        nw *= 2
        if nw > 1:
            nw = 1

        # snake --------------------------------------------------
        body = self.get_snake()

        # init snake
        ns = 1
        nes = 1
        es = 1
        ses = 1
        ss = 1
        sws = 1
        ws = 1
        nws = 1

        # loop snake
        for i in body:
            # north -> northwest, north, northeast
            for r in reversed(range(1, y + 1)):
                if (x, y - r) == i:
                    ns = r / self.height
                if (x - r, y - r) == i:
                    nws = r / self.height
                if (x + r, y - r) == i:
                    nes = r / self.height
            # south -> southwest, south, southeast
            for r in reversed(range(1, self.height - y)):
                if (x, y + r) == i:
                    ss = r / self.height
                if (x - r, y + r) == i:
                    sws = r / self.height
                if (x + r, y + r) == i:
                    ses = r / self.height
            # west -> northwest, west, southwest
            for r in reversed(range(1, x + 1)):
                if (x - r, y) == i:
                    ws = r / self.width
                if (x - r, y - r) == i:
                    nws = r / self.width
                if (x - r, y + r) == i:
                    sws = r / self.width
            # east -> northeast, east, southeast
            for r in reversed(range(1, self.width - x)):
                if (x + r, y) == i:
                    es = r / self.width
                if (x + r, y - r) == i:
                    nes = r / self.width
                if (x + r, y + r) == i:
                    ses = r / self.width

        # food ------------------------------------------------
        food = self.get_food()

        # init food
        nf = 1
        nef = 1
        ef = 1
        sef = 1
        sf = 1
        swf = 1
        wf = 1
        nwf = 1

        # horizontal and vertical
        # north - south
        if food[0] == x:
            if food[1] < y:
                nf = (y - food[1]) / self.height  # north
            else:
                sf = (food[1] - y) / self.height  # south

        # east - west
        if food[1] == y:
            if food[0] < x:
                wf = (x - food[0]) / self.width  # west
            else:
                ef = (food[0] - x) / self.width  # east

        # diagonal
        cache = (food[0] - x, food[1] - y)

        if cache[0] == cache[1]:
            if cache[0] < 0:
                nwf = (x - food[0]) / self.width  # northwest
            else:
                sef = (food[0] - x) / self.width  # southeast

        if abs(cache[0]) == abs(cache[1]) and cache[0] != cache[1]:
            if cache[0] < 0:
                nef = (x - food[0]) / self.width  # northeast
            else:
                swf = (food[0] - x) / self.width  # southwest

        # merge all variables ------------------------------------------
        vicinity = 1 - np.array(
            [n, ns, nf, ne, nes, nef, e, es, ef, se, ses, sef, s, ss, sf, sw, sws, swf, w, ws, wf, nw, nws, nwf])
        return vicinity
