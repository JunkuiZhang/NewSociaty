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

    def generate(self):
        """
        初始化一定维度的矩阵
        :return: [[[a11, b11]. [a12, b12], ..., [a1n, b1n]],
                  [[a21, b21], [a22, b22], ..., [a2n, b2n]],
                  ...,
                  [[an1, bn1], [an2, bn2], ..., [ann, bnn]]]
                 这里a的值为格子产出（大于0的值），b的值为该格子是否存在个体（0没有，1有）
        """
        for i in range(self.dimension):
            row = []
            for j in range(self.dimension):
                row.append([0, 0])
            self.matrix.append(row)

    def insert_value(self, pos, num):
        """
        改变矩阵特定位置的值
        :param pos: 所需要改变的值的位置[x, y]
        :param num: list变量，有且仅有[0, b, c]、[1, b], [2, c]三种情况
                    [0, b, c]表示矩阵的两个值都需要改变，[1, b]表示仅改变格子的产出值，[2, c]表示仅改变格子是否被个体占据的值
        :return: None
        """
        if num[0] == 0:
            self.matrix[pos[0]][pos[1]][0], self.matrix[pos[0]][pos[1]][1] = num[1], num[2]
        elif num[0] == 1:
            self.matrix[pos[0]][pos[1]][0] = num[1]
        elif num[0] == 2:
            self.matrix[pos[0]][pos[1]][1] = num[1]
        else:
            print('Wrong num indicator.')
            raise ValueError

    def get_value(self, pos):
        """
        给出矩阵特定位置的值
        :param pos: [x, y]
        :return: [a, b]，其中，a表示格子产出，b表示各自是否有个体占据
        """
        return self.matrix[pos[0]][pos[1]]

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
