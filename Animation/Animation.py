import pygame
from pygame.locals import *
import MathBehind.FindMaxValue


class Animation:
    def __init__(self, world, entities, fps=2):
        # World object
        self.__world = world
        # EntitiesPopulation object
        self.__entities = entities
        # 游戏帧率控制
        self.__fps = fps
        self.__resolution = self.world.resolution
        self.__dimension = self.world.dimension

    @property
    def world(self):
        return self.__world

    @property
    def entities(self):
        return self.__entities

    @property
    def fps(self):
        return self.__fps

    @fps.setter
    def fps(self, num):
        assert type(num) == int, 'Wrong argument inserted.'
        self.__fps = num

    @property
    def resolution(self):
        return self.__resolution

    @property
    def dimension(self):
        return self.__dimension

    def playing(self):
        width = int(round(self.resolution / self.dimension, 0))
        pygame.init()
        screen = pygame.display.set_mode((self.resolution, self.resolution))
        clock = pygame.time.Clock()
        pygame.display.set_caption('Society')
        max_product = MathBehind.FindMaxValue.MaxFind(self.world.world_grid.matrix).find()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()

            for i in range(self.dimension):
                for j in range(self.dimension):
                    color_filled = self.world.world_grid.matrix[i][j][0] * 255 // max_product
                    pygame.draw.rect(screen, (color_filled, color_filled, color_filled),
                                     (j * width, i * width, width, width))
                    if self.world.world_grid.matrix[i][j][1] == 1:
                        coordinates = (j * width + width // 2, i * width + width // 2)
                        pygame.draw.circle(screen, (234, 103, 83), coordinates, width // 3)

            clock.tick(self.fps)
            self.entities.population_move()
            self.world.population_position_insert(self.entities)
            pygame.display.update()
