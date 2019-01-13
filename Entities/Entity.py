class Entity:

    def __init__(self, world_grid, position, intelligence, eating, wealth, alive=1, life_time=0):
        self.__world_grid = world_grid
        self.__position = position
        self.__intel = intelligence
        self.__eating = eating
        self.__wealth = wealth
        self.__life_time = life_time
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
        self.wealth += self.world_grid[self.position]
        self.wealth -= self.eating
        self.life_time += 1
        if self.wealth < 0:
            self.alive = 0

    def move(self):

        def check_bond(cor):
            if cor[0] < 0 or cor[0] > len(self.world_grid[0]) - 1 or cor[1] < 0 or cor[1] > len(self.world_grid) - 1:
                return False
            else:
                return True

        def value_find(l, mode='max'):
            indicator = 0
            res = [0, [0, 0]]
            for ls in l:
                if indicator == 0:
                    res = [ls[0], ls[1]]
                    indicator = 1
                    continue
                else:
                    if mode == 'max':
                        if ls[0] > res[0]:
                            res = [ls[0], ls[1]]
                        else:
                            pass
                    elif mode == 'min':
                        if ls[0] < res[0]:
                            res = [ls[0], ls[1]]
                        else:
                            pass
            return res

        position_list = []
        for i in range(self.intel + 1):
            for j in range(self.intel + 1):
                new_position = [self.position[0] - i, self.position[1] - j]
                if check_bond(new_position):
                    position_list.append([self.world_grid[new_position], new_position])
                new_position = [self.position[0] - i, self.position[1] + j]
                if check_bond(new_position):
                    position_list.append([self.world_grid[new_position], new_position])
                new_position = [self.position[0] + i, self.position[1] - j]
                if check_bond(new_position):
                    position_list.append([self.world_grid[new_position], new_position])
                new_position = [self.position[0] + i, self.position[1] + j]
                if check_bond(new_position):
                    position_list.append([self.world_grid[new_position], new_position])

        position_move = value_find(position_list, 'max')
        self.position = position_move[1]