import Entity
import random


class EntitiesPopulation:

    def __init__(self, world, total_num):
        self.__world = world
        self.__world_grid = world.world_grid.matrix
        self.__total_num = total_num
        self.__seed = world.random_seed
        # pool里为entity类型的object
        self.pool = []

    @property
    def world(self):
        return self.__world

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
            self.pool.append(Entity.Entity(self.world, [row_num, col_num], entity_id=(i+1), eating=10))

    def population_move(self):
        assert not self.pool == [], 'pool init first.'
        self.world.world_time += 1
        for _entity in self.pool:
            if _entity.alive == 1:
                _entity.live_one_day()
                _entity.move()
            else:
                self.world.world_grid.insert_value(_entity.position, [2, 0])


if __name__ == '__main__':
    import World.World
    p = EntitiesPopulation(World.World.World(10).world_grid.matrix, 20)
    p.population_init()
    for entity in p.pool:
        print(entity)
