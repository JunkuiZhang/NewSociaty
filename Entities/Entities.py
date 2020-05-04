import Entity
import random


class EntitiesPopulation:

    def __init__(self, world, total_num, rand_intel=False, fixed_intel_num=2):
        self.__world = world
        self.__total_num = total_num
        self.__seed = world.random_seed
        self.__rand_intel = rand_intel
        self.__fixed_intel_num = fixed_intel_num
        # pool里为entity类型的object
        self.pool = []
        # self.position_pool = []
        self.pos_pool = []

    @property
    def world(self):
        return self.__world

    @world.setter
    def world(self, value):
        self.__world = value

    @property
    def total_num(self):
        return self.__total_num

    @property
    def seed(self):
        return self.__seed

    @property
    def rand_intel(self):
        return self.__rand_intel

    @property
    def fixed_intel_num(self):
        return self.__fixed_intel_num

    def population_init(self):
        if not self.pool == []:
            self.pool = []
        pos_occupied = []
        dimension = self.world.dimension
        for i in range(self.total_num):
            row_num = random.choice(range(dimension))
            col_num = random.choice(range(dimension))
            while [row_num, col_num] in pos_occupied:
                row_num = random.choice(range(dimension))
                col_num = random.choice(range(dimension))
            if self.rand_intel:
                intelligence = random.randint(3, 9)
            else:
                intelligence = self.fixed_intel_num
            initial_wealth = random.randint(20, 60)
            self.pool.append(Entity.Entity(self.world, [row_num, col_num], wealth= initial_wealth,
                                           intelligence=intelligence, entity_id=(i+1), eating=1))
            self.pos_pool.append([row_num, col_num])

    def population_live_one_day(self):
        assert not self.pool == [], 'pool init first.'
        self.world.world_time += 1
        for _entity in self.pool:
            assert _entity.alive == 1
            _entity.live_one_day()
            if _entity.alive == 0:
                self.pool.remove(_entity)
                self.pos_pool.remove(_entity.position)

    def population_move(self):
        for ent in self.pool:
            if ent.alive == 1:
                self.pos_pool.remove(ent.position)
                ent.move(self.pos_pool)
                self.pos_pool.append(ent.position)
            else:
                ent.alive = 0
                self.pool.remove(ent)



if __name__ == '__main__':
    import World.World
    p = EntitiesPopulation(World.World.World(10).world_grid.matrix, 20)
    p.population_init()
    for entity in p.pool:
        print(entity)
