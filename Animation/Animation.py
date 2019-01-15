import pygame
from pygame.locals import *
import MathBehind.FindMaxValue



class Animation:

    def __init__(self, world, entities):
        # World object
        self.__world = world
        self.__entities = entities
        self.__resolution = self.world.resolution
        self.__dimension = self.world.dimension

    @property
    def world(self):
        return self.__world

    @property
    def entities(self):
        return self.__entities

    @property
    def resolution(self):
        return self.__resolution

    @property
    def dimension(self):
        return self.__dimension

    def playing(self):
        pixes_per_unit = round(self.resolution/self.dimension, 0)
        pygame.init()
        screen = pygame.display.set_mode((self.resolution, self.resolution))
        pygame.display.set_caption('Society')
        max_product = MathBehind.FindMaxValue.MaxFind(self.world.world_grid.matrix)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
