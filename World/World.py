import random


class World:

    def __init__(self, dimension=50, resolution=1000, random_seed=None, mountain_factor=.6, base_product=(100, 50)):
        # n by n的世界棋盘，默认为50X50
        self.__dimension = dimension
        # 画出棋盘时所用的分辨率
        self.__resolution = resolution
        # 设置随机种子
        self.__random_seed = random_seed
        self.__mountain_factor = mountain_factor
        self.__base_product = base_product
        self.__world_matrix = None
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
    def world_matrix(self):
        return self.__world_matrix

    @world_matrix.setter
    def world_matrix(self, m):
        self.__world_matrix = m

    def generating(self):
        if not (self.random_seed is None):
            random.seed(self.random_seed)
        else:
            pass
        mountain_semi_diameter = round(self.dimension * self.mountain_factor * .5, 0)
        central_position = round(self.dimension * .5, 0)

        try:
            mountain_semi_diameter = int(mountain_semi_diameter)
            central_position = int(central_position)
        except:
            raise ValueError

