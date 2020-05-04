class Generator:

    """
    用来生成world所需要的矩阵
    """

    def __init__(self, dimension):
        # 生成的矩阵维度
        self.__dimension = dimension
        # 初始化矩阵
        self.matrix = []
        self.generate()

    @property
    def dimension(self):
        return self.__dimension

    @dimension.setter
    def dimension(self, value):
        self.__dimension = value

    def generate(self):
        """
        初始化一定维度的矩阵
        :return: [[[a11, b11]. [a12, b12], ..., [a1n, b1n]],
                  [[a21, b21], [a22, b22], ..., [a2n, b2n]],
                  ...,
                  [[an1, bn1], [an2, bn2], ..., [ann, bnn]]]
                 这里a的值为格子产出（大于0的值），b的值为该格子是否存在个体（0没有，1有）

                 2020-03 change log:
                 [{'current_prod':a, 'initial_prod':c}]: 添加cn为世界当前格子的初始产出
        """
        for i in range(self.dimension):
            row = []
            for j in range(self.dimension):
                row.append({
                'current_prod': 0,
                'initial_prod': 0
            })
            self.matrix.append(row)

    def insert_value(self, pos, key, value):
        """
        改变矩阵特定位置的值
        :param pos: 所需要改变的值的位置[x, y]
        :param key: 要更改的key
        :param value: 要改的值
        :return: None
        """
        x, y = pos
        self.matrix[x][y][key] = value

    def get_value(self, pos):
        """
        给出矩阵特定位置的值
        :param pos: [x, y]
        :return: [a, b, cn]，其中，a表示格子产出，b表示各自是否有个体占据,cn定义同上
        """
        x, y = pos
        return self.matrix[x][y]

    def print_matrix(self):
        for i in range(self.dimension):
            s = str(self.matrix[i])
            print(s[1:(len(s)-1)] + ', ')


if __name__ == '__main__':
    g = Generator(5)
    print(g.print_matrix())
    g.insert_value([0, 0], [0, 50, 1])
    print(g.print_matrix())
    print(g.get_value([0, 0]))
