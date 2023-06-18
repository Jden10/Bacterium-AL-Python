import pygame as pg
import random
from options import *


class Food(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((cell_food, cell_food))
        self.image.fill('white')
        pg.draw.circle(self.image, '#93ed83', (cell_food // 2, cell_food // 2), cell_food // 2)
        pg.draw.circle(self.image, '#7fd770', (cell_food // 2, cell_food // 2), cell_food // 2, cell_food // 6)
        self.image.set_colorkey('white')
        self.rect = self.image.get_rect(
            center=(random.randint(cell_food, width - cell_food), random.randint(cell_food, height - cell_food)))
        self.radius = cell_food // 2.5
