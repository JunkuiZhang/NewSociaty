import pygame
from pygame.locals import *
import MathBehind.FindMaxValue
import MathBehind.GiniCal
import os


class Animation:
    def __init__(self, world, entities, fps=2, data_saving=True):
        # World object
        self.__world = world
        # EntitiesPopulation object
        self.__entities = entities
        # 游戏帧率控制
        self.__fps = fps
        # 是否保存数据
        self.__data_saving = data_saving
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
    def data_saving(self):
        return self.__data_saving

    @data_saving.setter
    def data_saving(self, indicator):
        self.__data_saving = indicator

    @property
    def resolution(self):
        return self.__resolution

    @property
    def dimension(self):
        return self.__dimension

    def data_saving_init(self):
        if self.data_saving:
            if not os.path.isdir('./Data'):
                os.mkdir('./Data')
            else:
                pass

    def playing(self):
        self.data_saving_init()

        width = int(round(self.resolution / self.dimension, 0))
        pygame.init()
        screen = pygame.display.set_mode((self.resolution, self.resolution))
        clock = pygame.time.Clock()
        pygame.display.set_caption('The Great Sugar Empire')
        max_product = MathBehind.FindMaxValue.MaxFind(self.world.world_grid.matrix).find()
        index_cal = MathBehind.GiniCal.GinCalculator()

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
            index_cal.calculate(self.entities.pool, self.world.world_grid.matrix)
            self.entities.population_move()
            self.world.population_position_insert(self.entities)
            pygame.display.update()
