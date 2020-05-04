import pygame
from pygame.locals import *
import MathBehind.FindMaxValue
import MathBehind.GiniCal
import os
import csv
import DrawWealth


class Animation:
    def __init__(self, world, entities, fps=3, file_name='', gini_cal=False):
        # World object
        self.__world = world
        # EntitiesPopulation object
        self.__entities = entities
        # 游戏帧率控制
        self.__fps = fps
        # 是否保存数据
        self.__file_name = file_name
        self.__gini_cal = gini_cal
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
    def gini_cal(self):
        return self.__gini_cal

    @gini_cal.setter
    def gini_cal(self, value):
        self.__gini_cal = value

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

    def strings_display(self, screen, gini=(-1, -1), top=-1):
        font = pygame.font.SysFont('Arial', 30)
        if self.gini_cal:
            string_render = font.render(f'World Time: {self.world.world_time}, PGini: {gini[0]},'
                                        f' WGini: {gini[1]}, Top: {top}', True, (100, 100, 100))
        else:
            string_render = font.render(f'World Time: {self.world.world_time}', True, (100, 100, 100))
        string_display = string_render.get_rect()
        string_display.topleft = (0, 0)
        screen.blit(string_render, string_display)

    def world_grid_drawing(self, max_product, screen, width):
        for i in range(self.dimension):
            for j in range(self.dimension):
                color_filled = self.world.world_grid.matrix[i][j]['current_prod'] * 255 // max_product
                color_filled = 255 - color_filled
                pygame.draw.rect(screen, (color_filled, color_filled, color_filled),
                                 (j * width, i * width, width, width))
                # if self.world.world_grid.matrix[i][j][1] == 1:
                #     coordinates = (j * width + width // 2, i * width + width // 2)
                #     pygame.draw.circle(screen, (234, 103, 83), coordinates, width // 3)

    def pop_drawing(self, screen, width):
        for pos in self.entities.pos_pool:
            i, j = pos
            coordinates = (j * width + width // 2, i * width + width // 2)
            pygame.draw.circle(screen, (230, 100, 80), coordinates, width // 3)

    def finish(self, screen):
        font = pygame.font.SysFont('Arial', 30)
        string_render = font.render(f'Simulation Finished at World Time: {self.world.world_time}',
                                    True, (200, 200, 200))
        string_display = string_render.get_rect()
        string_display.topleft = (100, 100)
        screen.blit(string_render, string_display)

    def get_top_ten(self):
        num_pop = len(self.entities.pool)
        num_top_10_percent = int(round(.1 * num_pop, 0))
        assert num_top_10_percent > 0
        wealth_list = []
        for ent in self.entities.pool:
            wealth_list.append(ent.wealth)
        wealth_list.sort(reverse=True)
        res = sum(wealth_list[0:num_top_10_percent + 1]) / sum(wealth_list)
        return round(res, 3)

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
        pygame.display.set_caption('大唐帝国 | 张峻魁')
        # max_product = MathBehind.FindMaxValue.MaxFind(self.world.world_grid.matrix).find()
        max_product = 4
        index_cal = MathBehind.GiniCal.GinCalculator()
        if self.gini_cal:
            _gini = index_cal.calculate(self.entities.pool, self.world.world_grid.matrix)
        else:
            _gini = [-1, -1]

        self.draw_wealth = DrawWealth.DrawWealth()
        self.draw_wealth.draw(self.entities)
        self.world_grid_drawing(max_product, screen, width)
        self.pop_drawing(screen, width)
        self.strings_display(screen, _gini, self.get_top_ten())
        pygame.display.update()

        is_paused = True
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    if self.file_name:
                        file.close()
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_SPACE:
                        is_paused = not is_paused

            if not is_paused:
                clock.tick(self.fps)
                if len(self.entities.pool) == 0:
                    print('结束')
                    self.finish(screen)
                    is_paused = True
                    continue

                if self.gini_cal:
                    gini = index_cal.calculate(self.entities.pool, self.world.world_grid.matrix)
                else:
                    gini = [-1, -1]

                if self.file_name:
                    live_num = 0
                    for ent in self.entities.pool:
                        writer.writerow([self.world.world_time, ent.entity_id, ent.intel, ent.alive,
                                         self.world.world_grid.matrix[ent.position[0]][ent.position[1]][0],
                                         ent.eating_plus, ent.wealth])
                        if ent.alive == 1:
                            live_num += 1
                    if live_num == 0:
                        print('Game Over')
                        file.close()
                        break

                self.entities.population_live_one_day()
                self.world.world_reproduce()
                self.entities.population_move()
                if self.world.world_time % 10 == 0:
                    self.draw_wealth.draw(self.entities, self.world.world_time)
                self.world_grid_drawing(max_product, screen, width)
                self.pop_drawing(screen, width)
                self.strings_display(screen, gini, top=self.get_top_ten())

                pygame.display.update()
