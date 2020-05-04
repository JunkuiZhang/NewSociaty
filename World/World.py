import random
import MathBehind.Generator
import MathBehind.CoordinatesCal


class World:

    def __init__(self, dimension=50, resolution=600, random_seed=None, mountain_factor=.7, base_product=(100, 50),
                 inflation=0, reproduce_num=1):
        # n by n的世界棋盘，默认为50X50
        self.__dimension = dimension
        # 画出棋盘时所用的分辨率
        self.__resolution = resolution
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
        assert num < 1 and num >= 0, 'Wrong inflation value assigned.'
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
        central_position = [round(self.dimension * .5, 0), round(self.dimension * .5, 0)]

        try:
            mountain_semi_diameter = int(mountain_semi_diameter)
            int(central_position[0])
        except:
            raise ValueError

        # 初始化
        self.world_grid = MathBehind.Generator.Generator(self.dimension)
        calculator = MathBehind.CoordinatesCal.CoordinateCalculation()
        for i in range(self.dimension):
            for j in range(self.dimension):
                if calculator.calculation([i, j], central_position) > mountain_semi_diameter:
                    # 不在糖山的范围内
                    continue
                elif calculator.calculation([i, j], central_position) <= 2:
                    product = 4
                elif calculator.calculation([i, j], central_position) <= 2 + round(self.dimension*.07, 0):
                    product = 3
                elif calculator.calculation([i, j], central_position) <= 2 + round(self.dimension*.17, 0):
                    product = 2
                else:
                    product = 1
                self.world_grid.insert_value([i, j], 'current_prod', product)
                self.world_grid.insert_value([i, j], 'initial_prod', product)
                # else:
                #     product = random.gauss(mu=self.base_product[0], sigma=self.base_product[1])
                #     # 若随机的产出小于0，则初始化为0
                #     if product < 0:
                #         continue
                #     # 距离糖山中心越近，产出越高，some factor为一个修正系数
                #     some_factor = .9
                #     product *= (abs(calculator.calculation([i, j], central_position) - mountain_semi_diameter)
                #                 * some_factor)
                #     product = round(product, 2)
                #     self.world_grid.insert_value([i, j], [1, product])


if __name__ == '__main__':
    w = World(dimension=50)
    w.world_grid.print_matrix()
