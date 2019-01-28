import pygame
from pygame.locals import *
import MathBehind.FindMaxValue
import MathBehind.GiniCal
import os
import csv


class Animation:
    def __init__(self, world, entities, fps=2, file_name=''):
        # World object
        self.__world = world
        # EntitiesPopulation object
        self.__entities = entities
        # 游戏帧率控制
        self.__fps = fps
        # 是否保存数据
        self.__file_name = file_name
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
    def file_name(self):
        return self.__file_name

    @file_name.setter
    def file_name(self, name_string):
        self.__file_name = name_string

    @property
    def resolution(self):
        return self.__resolution

    @property
    def dimension(self):
        return self.__dimension

    def data_saving_init(self):
        if self.file_name:
            if not os.path.isdir('./Data'):
                os.mkdir('./Data')
            elif os.path.isdir('./Data'):
                file_position = './Data/' + self.file_name + '.csv'
                if os.path.isfile(file_position):
                    os.remove(file_position)

    def playing(self):
        self.data_saving_init()

        # 保存数据部分
        if self.file_name:
            file_name = self.file_name + '.csv'
            file_position = './Data/' + file_name
            file = open(file_position, 'w', newline='')
            writer = csv.writer(file)
            writer.writerow(['Time', 'ID', 'Ability', 'Status', 'Earning', 'Eating', 'Wealth'])

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
                    if self.file_name:
                        file.close()
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

            if self.file_name:
                live_num = 0
                for ent in self.entities.pool:
                    writer.writerow([self.world.world_time, ent.entity_id, ent.intel, ent.alive,
                                     self.world.world_grid.matrix[ent.position[0]][ent.position[1]],
                                     ent.eating_plus, ent.wealth])
                    if ent.alive == 1:
                        live_num += 1
                if live_num == 0:
                    print('Game Over')
                    file.close()
                    break

            self.entities.population_move()
            self.world.population_position_insert(self.entities)
            pygame.display.update()
