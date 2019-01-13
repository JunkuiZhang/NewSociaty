from . import Entity
import random



class EntitiesPopulation:

    def __init__(self, world_grid, total_num, seed=None):
        self.__world_grid = world_grid
        self.__total_num = total_num
        self.__seed = seed
        self.pool = []

    @property
    def world_grid(self):
        return self.__world_grid

    @property
    def total_num(self):
        return self.__total_num

    @property
    def seed(self):
        return self.__seed

    def population_init(self):
        if not self.pool == []:
            self.pool = []
        pos_occupied = []
        for i in range(self.total_num):
            row_num = random.choice(range(len(self.world_grid[0])))
            col_num = random.choice(range(len(self.world_grid[0])))
            while [row_num, col_num] in pos_occupied:
                row_num = random.choice(range(len(self.world_grid[0])))
                col_num = random.choice(range(len(self.world_grid[0])))
            self.pool.append(Entity.Entity(self.world_grid, [row_num, col_num], 10, 0))

    def population_move(self):
        pass



if __name__ == '__main__':
    import World.World
    p = EntitiesPopulation(World.World.World(10), 20)
    for entity in p.pool:
        print(entity)