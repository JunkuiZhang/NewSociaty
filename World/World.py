import random
import MathBehind.Generator
import MathBehind.CoordinatesCal


class World:

    def __init__(self, dimension=50, resolution=600, num_mountain=1, random_seed=None,
                 mountain_factor=.65, base_product=(100, 50), inflation=0, reproduce_num=1):
        # n by n的世界棋盘，默认为50X50
        self.__dimension = dimension
        # 画出棋盘时所用的分辨率
        self.__resolution = resolution
        # 产糖区的数量
        self.__num_mountain = num_mountain
        # 设置随机种子
        self.__random_seed = random_seed
        # 设置糖山的大小
        self.__mountain_factor = mountain_factor
        # 设置生成糖山时的随机数的均值及标准差
        self.__base_product = base_product
        # 通胀水平，每期增加个体的eating消耗
        self.__inflation = inflation
        self.__reproduce_num = reproduce_num
        self.__world_grid = None
        self.__world_time = 0
        self.generating()

    @property
    def dimension(self):
        return self.__dimension

    @dimension.setter
    def dimension(self, dim):
        self.__dimension = dim

    @property
    def resolution(self):
        return self.__resolution

    @resolution.setter
    def resolution(self, num):
        self.__resolution = num

    @property
    def num_mountain(self):
        return self.__num_mountain

    @num_mountain.setter
    def num_mountain(self, value):
        self.__num_mountain = value

    @property
    def random_seed(self):
        return self.__random_seed

    @random_seed.setter
    def random_seed(self, seed):
        self.__random_seed = seed

    @property
    def mountain_factor(self):
        return self.__mountain_factor

    @mountain_factor.setter
    def mountain_factor(self, num):
        self.__mountain_factor = num

    @property
    def base_product(self):
        return self.__base_product

    @property
    def inflation(self):
        return self.__inflation

    @inflation.setter
    def inflation(self, num):
        assert 1 > num >= 0, 'Wrong inflation value assigned.'
        self.__inflation = num

    @property
    def reproduce_num(self):
        return self.__reproduce_num

    @reproduce_num.setter
    def reproduce_num(self, value):
        self.__reproduce_num = value

    @property
    def world_grid(self):
        return self.__world_grid

    @world_grid.setter
    def world_grid(self, m):
        self.__world_grid = m

    @property
    def world_time(self):
        return self.__world_time

    @world_time.setter
    def world_time(self, num):
        self.__world_time = num

    def world_grid_clean(self):
        for row in self.world_grid.matrix:
            for col in row:
                col[1] = 0

    def world_reproduce(self):
        for i in range(self.dimension):
            for j in range(self.dimension):
                initial_product = self.world_grid.get_value([i, j])['initial_prod']
                current_product = self.world_grid.get_value([i, j])['current_prod']
                if current_product < initial_product:
                    if initial_product != 0:
                        assert initial_product != current_product, '收割过程错误！'
                    new_product = current_product + self.reproduce_num
                    if new_product > initial_product:
                        new_product = initial_product
                    self.world_grid.insert_value([i, j], 'current_prod', new_product)

    def generating(self):
        # 检查是否设置了随机种子
        if not (self.random_seed is None):
            random.seed(self.random_seed)
        else:
            pass
        # 检测world time值
        if not self.world_time == 0:
            self.world_time = 0
        # 糖山的半径
        mountain_semi_diameter = round(self.dimension * self.mountain_factor * .5, 0)
        # central_position = [round(self.dimension * .5, 0), round(self.dimension * .5, 0)]

        try:
            mountain_semi_diameter = int(mountain_semi_diameter)
        except:
            raise ValueError

        def get_mountain_center(num):
            assert num > 0
            if num == 1:
                _y = _x = int(round(self.dimension*.5, 0))
                return [[_x, _y]]
            else:
                res_list = []
                frontier = int(round(self.dimension*.2, 0))
                for _something in range(num):
                    x = random.randint(frontier, self.dimension-frontier+1)
                    y = random.randint(frontier, self.dimension-frontier+1)
                    res_list.append([x, y])
                _calculator = MathBehind.CoordinatesCal.CoordinateCalculation()
                for _i in range(len(res_list)):
                    for _j in range(_i+1, len(res_list)):
                        pos1, pos2 = res_list[_i], res_list[_j]
                        dist = _calculator.calculation(pos1, pos2)
                        if dist > self.dimension*.45:
                            continue
                        else:
                            return get_mountain_center(num)
                return res_list

        def dist_checker(pos, cent_pos, length_required):
            _calculator = MathBehind.CoordinatesCal.CoordinateCalculation()
            if _calculator.calculation(pos, cent_pos) <= length_required:
                return True
            else:
                return False

        # 初始化
        central_position_list = get_mountain_center(self.num_mountain)
        self.world_grid = MathBehind.Generator.Generator(self.dimension)
        # calculator = MathBehind.CoordinatesCal.CoordinateCalculation()
        mount_dis_factor = 1 - .5/self.dimension
        for i in range(self.dimension):
            for j in range(self.dimension):
                for k in central_position_list:
                    if not dist_checker([i, j], k, mountain_semi_diameter):
                        continue
                    elif dist_checker([i, j], k, 2):
                        product = 4
                    elif dist_checker([i, j], k, 2+round(self.dimension*0.07*mount_dis_factor, 0)):
                        product = 3
                    elif dist_checker([i, j], k, 2+round(self.dimension*.15*mount_dis_factor, 0)):
                        product = 2
                    else:
                        product = 1
                    init_prod = self.world_grid.get_value([i, j])['current_prod']
                    if product > init_prod:
                        self.world_grid.insert_value([i, j], 'current_prod', product)
                        self.world_grid.insert_value([i, j], 'initial_prod', product)
                    else:
                        pass


if __name__ == '__main__':
    w = World(dimension=50)
    w.world_grid.print_matrix()
