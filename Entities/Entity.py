import random
import MathBehind.CoordinatesCal


class Entity:

    def __init__(self, world, position, eating, entity_id=-1, wealth=50, intelligence=3, alive=1, life_time=0,
                 bravery=True, intel_mode=1, delta_wealth_indicator=True):
        # “世界”地图（矩阵），详见World
        # world(n by n) = [[[product, is_occupied], ..., [product, is_occupied]],
        #          [[product, is_occupied], ..., [product, is_occupied]],
        #          ...
        #          [[product, is_occupied], ..., [product, is_occupied]]]
        #
        #     product: 大于0的float类型变量
        # is_occupied: 1表示有个体，0表示没有个体
        # world object
        self.__world = world
        # 个体的唯一id
        self.__entity_id = entity_id
        # 该个体在世界中所处的位置
        self.__position = position
        # 该个体的“能力”，本模型中为个体能看到多远的格子
        self.__intel = intelligence
        # 个体每日所消耗的基础能量
        self.__eating = eating
        # 根据wealth调整后的eating值
        self.__eating_plus = eating
        # 个体除去每日所消耗的能量后所积累的剩余
        self.__wealth = wealth
        # 个体存活时间，以“天”记
        self.__life_time = life_time
        # 个体的存货状态，1为存活，0为死亡
        self.__alive = alive
        # 是否开启随机移动，当个体周围的格子产出全部为零时，随即移动到任意一个格子（防止原地等死）
        self.__bravery = bravery
        # 个体移动时，观察十字形还是圆形格子，0表示正方形，1表示十字形，2表示圆形
        self.__intel_mode = intel_mode
        # 个体的财富增量，用以计算是否需要bravery
        # 考察3期的财富增量，[a, b, c]分别表示第1、2、3期的财富增量，当财富增量小于0时，值为0
        self.__delta_wealth = [1, 1, 1]
        self.__delta_wealth_indicator = delta_wealth_indicator

    @property
    def entity_id(self):
        return self.__entity_id

    @entity_id.setter
    def entity_id(self, num):
        self.__entity_id = num

    @property
    def world(self):
        return self.__world

    @world.setter
    def world(self, value):
        self.__world = value

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, cor):
        self.__position = cor

    @property
    def intel(self):
        return self.__intel

    @intel.setter
    def intel(self, value):
        assert value > 0, 'Invalid value set for intelligence.'
        self.__intel = value

    @property
    def eating(self):
        return self.__eating

    @eating.setter
    def eating(self, value):
        assert value > 0, 'Invalid value for property "Eating".'
        self.__eating = value

    @property
    def eating_plus(self):
        return self.__eating_plus

    @eating_plus.setter
    def eating_plus(self, num):
        self.__eating_plus = num

    @property
    def wealth(self):
        return self.__wealth

    @wealth.setter
    def wealth(self, value):
        self.__wealth = value

    @property
    def life_time(self):
        return self.__life_time

    @life_time.setter
    def life_time(self, value):
        assert value == self.__life_time + 1, 'Invalid time survived.'
        self.__life_time += value

    @property
    def alive(self):
        return self.__alive

    @alive.setter
    def alive(self, value):
        assert value == 1 or value == 0, 'Invalid alive value set for entity.'
        self.__alive = value

    @property
    def bravery(self):
        return self.__bravery

    @bravery.setter
    def bravery(self, indicator):
        assert type(indicator) == 'bool', 'Wrong assignment.'
        self.__bravery = indicator

    @property
    def intel_mode(self):
        return self.__intel_mode

    @intel_mode.setter
    def intel_mode(self, num):
        assert type(num) == 'int', 'Invalid argument.'
        self.__intel_mode = num

    @property
    def delta_wealth(self):
        return self.__delta_wealth

    @delta_wealth.setter
    def delta_wealth(self, l):
        self.__delta_wealth = l

    @property
    def delta_wealth_indicator(self):
        return self.__delta_wealth_indicator

    @delta_wealth_indicator.setter
    def delta_wealth_indicator(self, value):
        assert type(value) == 'bool', 'Wrong argument assignment.'
        self.__delta_wealth_indicator = value

    def __str__(self):
        print('Entity status:')
        print('position: {}'.format((str(self.position))))
        print('earning:{}'.format((str(self.world_grid[self.position[0]][self.position[1]][0]))))
        print('eating:{}'.format((str(self.eating))))
        print('intelligence:{}'.format((str(self.intel))))
        return '======='

    def delta_wealth_changer(self, value):
        dw0 = self.delta_wealth
        dw1 = [dw0[1], dw0[2], value]
        self.delta_wealth = dw1

    def delta_wealth_detector(self, prod):
        if prod - self.eating_plus < 0:
            return 0
        else:
            return 1

    def eating_adjustment(self):
        self.eating_plus = self.wealth * .2 + self.eating

    def live_one_day(self):
        """
        个体生存一天：
        1、收获个体所处的单元格上的能量
        2、个体消耗其一天所需要的能量
        3、生存时间+1
        4、更改delta wealth状态
        5、判断个体存活状态
        :return:
        """
        current_prod = self.world.world_grid.get_value(self.position)['current_prod']
        self.wealth += current_prod
        self.world.world_grid.insert_value(self.position, 'current_prod', 0)
        # self.wealth -= self.eating_plus
        self.wealth -= self.eating
        self.life_time += 1
        self.delta_wealth_changer(self.delta_wealth_detector(current_prod))
        # self.eating_adjustment()
        # self.eating *= (1 + self.world.inflation)
        # print('Alive: {}'.format(str(self.alive)))
        # print('Basic eating: {}'.format(str(self.eating)))
        # print('Adj eating: {}'.format(str(self.eating_plus)))
        # print('Delta wealth: {}'.format(str(self.delta_wealth)))
        # print('DW indicator: {}'.format(str(self.delta_wealth_indicator)))
        # print('=='*10)
        if self.wealth < 0:
            self.alive = 0

    def move(self, pos_occupied):
        """
        个体下一步的移动决策：
        1、根据个体的能力不同，看到的范围不同，把视野内未超出世界范围的格子坐标及格子的产出加入position_list
        2、把position_list中格子的产出按从大到小排列
        3、若产出最大的格子没有其他个体占据，则移动到此格子
        4、若产出最大的格子有其他个体占据，则考察后面的格子
        5、移动到目标格子
        :return:
        """

        def check_bond(cor, mode=self.intel_mode):
            """
            检测格子是否超出世界的范围
            :param cor: 形如[x, y]的坐标
            :param mode: 详见类变量说明
            :return: Boolean
            """
            if cor[0] < 0 or cor[0] > self.world.dimension - 1 or cor[1] < 0 or cor[1] > self.world.dimension - 1:
                return False
            else:
                if mode == 1:
                    if cor[0] == self.position[0] or cor[1] == self.position[1]:
                        return True
                    else:
                        return False
                elif mode == 2:
                    distance = MathBehind.CoordinatesCal.CoordinateCalculation().calculation(cor, self.position)
                    if distance > self.intel:
                        return False
                    else:
                        return True
                else:
                    return True

        def move_find(pl, mode='max'):
            """
            判断个体的最佳移动目标格子
            :param pl: 包含坐标、产出、是否被占据的list类型变量，形如[[z0, k0, [x0, y0]], ..., [产出, 是否被占据, [x坐标, y坐标]]]
            :param mode: 仅有“max”、“min”两种
            :return: 包含坐标的list类型，[x坐标, y坐标]
            """
            assert mode == 'max' or mode == 'min', 'Invalid mode parameter.'
            res = [pl[0][0], pl[0][1]]
            for pls in pl:
                if mode == 'max':
                    if pls[0] > res[0]:
                        # 产出大于当前最优格子，且该格子无个体占据
                        res = [pls[0], pls[1]]
                    else:
                        pass
                elif mode == 'min':
                    if pls[0] < res[0]:
                        res = [pls[0], pls[1]]
                    else:
                        pass
                else:
                    pass
            return res

        def need_of_bravery(pl, res):

            def delta_wealth_check(dw):
                if sum(dw) == 0:
                    return True
                else:
                    return False

            move = random.choice(pl)
            if res[0] == 0:
                return True, move[1]
            elif delta_wealth_check(self.delta_wealth) and self.delta_wealth_indicator:
                # 连续3期财富增量小于0，防止等死
                return True, move[1]
            else:
                return False, res[1]

        def is_considered(pos, pl):
            """
            去重函数
            :param pos: 当前考虑的位置[x, u]
            :param pl: 已经考虑过的位置list [[x0, y0], [x1, y1], ..., [xn, yn]]
            :return: Bool
            """
            if pos in pl:
                return True
            else:
                return False

        def is_occupied(pos):
            if pos in pos_occupied:
                return True
            else:
                return False

        def check_point(new_pos, pos_pool, pos_list):
            # pool用来去重
            if check_bond(new_pos) and not is_considered(new_pos, pos_pool) and not is_occupied(new_pos):
                pos_status = self.world.world_grid.get_value(new_pos)
                pos_list.append([pos_status['current_prod'], new_pos])
                pos_pool.append(new_pos)

        # 初始化position list
        position_list = []
        # position list形如[[a1, b1, [x1, y1]], ..., [an, bn, [xn, yn]]]
        # 其中a为格子产出，b为该格子是否存在其他个体，[x, y]为格子坐标
        _x, _y = self.position
        position_list.append([self.world.world_grid.get_value(self.position)['current_prod'], self.position])
        # 用来去重
        position_pool = []
        position_pool.append(self.position)
        x_start, y_start = self.position[0] - self.intel, self.position[1] - self.intel
        x_end, y_end = self.position[0] + self.intel + 1, self.position[1] + self.intel + 1
        for i in range(x_start, x_end):
            for j in range(y_start, y_end):
                check_point([i, j], position_pool, position_list)

        position_move = move_find(position_list, 'max')
        if self.bravery:
            bravery, position_move = need_of_bravery(position_list, position_move)
        else:
            bravery, position_move = False, position_move[1]
        self.position = position_move
        assert self.position != 0

        # debug
        # print(f'Eating plus: {self.eating_plus}')
        # print(f'Delta wealth: {self.delta_wealth}')

        return position_move
