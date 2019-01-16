import random
import MathBehind.Generator
import MathBehind.CoordinatesCal


class World:

    def __init__(self, dimension=50, resolution=600, random_seed=None, mountain_factor=.6, base_product=(100, 50)):
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
        self.__world_grid = None
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
    def world_grid(self):
        return self.__world_grid

    @world_grid.setter
    def world_grid(self, m):
        self.__world_grid = m

    def population_position_insert(self, pop):
        for entity in pop.pool:
            if entity.alive == 1:
                self.world_grid.insert_value(entity.position, [2, 1])
            else:
                pass

    def world_grid_clean(self):
        for row in self.world_grid.matrix:
            for col in row:
                col[1] = 0

    def generating(self):
        # 检查是否设置了随机种子
        if not (self.random_seed is None):
            random.seed(self.random_seed)
        else:
            pass
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
                else:
                    product = random.gauss(mu=self.base_product[0], sigma=self.base_product[1])
                    # 若随机的产出小于0，则初始化为0
                    if product < 0:
                        continue
                    # 距离糖山中心越近，产出越高，some factor为一个修正系数
                    some_factor = .9
                    product *= (abs(calculator.calculation([i, j], central_position)-mountain_semi_diameter)
                                * some_factor)
                    product = round(product, 2)
                    self.world_grid.insert_value([i, j], [1, product])


if __name__ == '__main__':
    w = World(20)
    w.world_grid.print_matrix()
