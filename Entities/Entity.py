class Entity:

    def __init__(self, world_grid, position, eating, wealth, intelligence=1, alive=1, life_time=0):
        # “世界”地图，详见World
        # world(n by n) = [[[product, is_occupied], ..., [product, is_occupied]],
        #          [[product, is_occupied], ..., [product, is_occupied]],
        #          ...
        #          [[product, is_occupied], ..., [product, is_occupied]]]
        #
        #     product: 大于0的float类型变量
        # is_occupied: 1表示有个体，0表示没有个体
        self.__world_grid = world_grid
        # 该个体在世界中所处的位置
        self.__position = position
        # 该个体的“能力”，本模型中为个体能看到多远的格子
        self.__intel = intelligence
        # 个体每日所消耗的能量
        self.__eating = eating
        # 个体除去每日所消耗的能量后所积累的剩余
        self.__wealth = wealth
        # 个体存活时间，以“天”记
        self.__life_time = life_time
        # 个体的存货状态，1为存活，0为死亡
        self.__alive = alive

    @property
    def world_grid(self):
        return self.__world_grid

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

    def live_one_day(self):
        """
        个体生存一天：
        1、收获个体所处的单元格上的能量
        2、个体消耗其一天所需要的能量
        3、生存时间+1
        4、判断个体存活状态
        :return:
        """
        self.wealth += self.world_grid[self.position]
        self.wealth -= self.eating
        self.life_time += 1
        if self.wealth < 0:
            self.alive = 0

    def move(self):
        """
        个体下一步的移动决策：
        1、根据个体的能力不同，看到的范围不同，把视野内未超出世界范围的格子坐标及格子的产出加入position_list
        2、把position_list中格子的产出按从大到小排列
        3、若产出最大的格子没有其他个体占据，则移动到此格子
        4、若产出最大的格子有其他个体占据，则考察后面的格子
        5、移动到目标格子
        :return:
        """

        def check_bond(cor):
            """
            检测格子是否超出世界的范围
            :param cor: 形如[x, y]的坐标
            :return: Boolean
            """
            if cor[0] < 0 or cor[0] > len(self.world_grid[0]) - 1 or cor[1] < 0 or cor[1] > len(self.world_grid[0]) - 1:
                return False
            else:
                return True

        def move_find(pl, mode='max'):
            """
            判断个体的最佳移动目标格子
            :param pl: 包含坐标、产出、是否被占据的list类型变量，形如[[z0, k0, [x0, y0]], ..., [产出, 是否被占据, [x坐标, y坐标]]]
            :param mode: 仅有“max”、“min”两种
            :return: 包含产出及坐标的list类型，[产出, [x坐标, y坐标]]
            """
            assert mode == 'max' or mode == 'min', 'Invalid mode parameter.'
            res = [pl[0], pl[2]]
            for pls in pl:
                if mode == 'max':
                    if (pls[0] > res[0] and pls[1] == 0):
                        # 产出大于当前最优格子，且该格子无个体占据
                        res = [pls[0], pls[2]]
                    else:
                        pass
                elif mode == 'min':
                    if (pls[0] < res[0] and pls[1] == 0):
                        res = [pls[0], pls[2]]
                    else:
                        pass
            return res

        # 初始化position list
        position_list = []
        position_list.append([self.world_grid[self.position[0]][self.position[1]], 0, self.position])
        for i in range(self.intel + 1):
            for j in range(self.intel + 1):
                if i == 0 and j == 0:
                    # 该情况即为初始化的格子
                    continue
                new_position = [self.position[0] - i, self.position[1] - j]
                if check_bond(new_position):
                    position_status = self.world_grid[new_position[0]][new_position[1]]
                    position_list.append([position_status[0], position_status[1], new_position])
                new_position = [self.position[0] - i, self.position[1] + j]
                if check_bond(new_position):
                    position_status = self.world_grid[new_position[0]][new_position[1]]
                    position_list.append([position_status[0], position_status[1], new_position])
                new_position = [self.position[0] + i, self.position[1] - j]
                if check_bond(new_position):
                    position_status = self.world_grid[new_position[0]][new_position[1]]
                    position_list.append([position_status[0], position_status[1], new_position])
                new_position = [self.position[0] + i, self.position[1] + j]
                if check_bond(new_position):
                    position_status = self.world_grid[new_position[0]][new_position[1]]
                    position_list.append([position_status[0], position_status[1], new_position])

        # 注意到这里不涉及对World的更改
        position_move = move_find(position_list, 'max')
        self.position = position_move[1]