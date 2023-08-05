import os

import numpy as np
import pygame


class SnakeGui:
    height = 32
    width = 32
    scale = 20
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    game_logic = None

    def __init__(self, game_logic):
        self.game_display = None
        self.game_logic = game_logic
        self.rendering = True

    def init(self):
        pygame.init()
        self.game_display = pygame.display.set_mode((self.width * self.scale, self.height * self.scale))
        dirname = os.path.dirname(os.path.realpath(__file__))
        logo = pygame.image.load(os.path.join(dirname, '../res', 'turkey.png'))
        pygame.display.set_icon(logo)
        pygame.display.set_caption('Sneuke')
        pygame.display.update()

    def set_logic(self, game_logic):
        self.game_logic = game_logic

    def render(self, mode):
        if self.rendering:
            if self.game_display is None:
                self.init()

            self.game_display.fill(self.white)
            snake = self.game_logic.get_snake()

            for position in snake:
                rect = [position[0] * self.scale, position[1] * self.scale, self.scale, self.scale]
                pygame.draw.rect(self.game_display, self.black, rect)
            food = self.game_logic.get_food()
            rect = [food[0] * self.scale, food[1] * self.scale, self.scale, self.scale]
            pygame.draw.rect(self.game_display, self.red, rect)
            pygame.display.update()
            self.listen_for_events()
            if mode == 'rgb_array':
                raw_pxarray = pygame.PixelArray(self.game_display)
                pxarray = []
                for row in raw_pxarray:
                    row_px = []
                    for pix in row:
                        tup = self.game_display.unmap_rgb(pix)
                        rgb = [tup[0], tup[1], tup[2]]
                        row_px.append(rgb)
                    pxarray.append(row_px)
                return np.array(pxarray).astype(np.uint8)
        return None

    def listen_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.rendering = False
                pygame.quit()

    def quit(self):
        pygame.quit()
