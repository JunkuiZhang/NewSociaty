class MaxFind:

    def __init__(self, world_grid):
        self.__world_grid = world_grid

    @property
    def world_grid(self):
        return self.__world_grid

    def find(self, indicator='max'):
        assert indicator == 'max' or indicator == 'min', 'Wrong indicator given.'
        res = 0
        for i in range(len(self.world_grid[0])):
            for j in range(len(self.world_grid[0])):
                if self.world_grid[i][j][0] > res:
                    res = self.world_grid[i][j][0]
                else:
                    continue
        return res