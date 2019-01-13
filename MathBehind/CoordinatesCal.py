class CoordinateCalculation:

    def __init__(self):
        pass

    def calculation(self, pos1, pos2):
        """
        计算两个坐标之间的距离
        :param pos1: [x1, y1]
        :param pos2: [x2, y2]
        :return: 大于零的值
        """
        result = (pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2
        return result**.5



if __name__ == '__main__':
    coor = CoordinateCalculation()
    num = coor.calculation([0, 0], [3, 4])
    print(num)